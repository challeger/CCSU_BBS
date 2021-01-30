from datetime import datetime, timedelta
from os import path
from uuid import uuid4

import jwt
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from shortuuidfield import ShortUUIDField

from ccsu_bbs.settings import JWT_KEY


def _user_directory_path(instance, filename):
    now_date = datetime.now().strftime('%Y%m%d')  # 当天日期
    filename = '{}.{}'.format(uuid4().hex[:12], 'jpg')  # 随机生成文件名
    return path.join('user', 'head', now_date, filename)  # 返回生成的文件名


class MemberManager(BaseUserManager):
    """
    用户模型的自定义管理类
    """
    def _create_user(self, username, password, nickname, email, **kwargs):
        user = self.model(username=username, password=password,
                          nickname=nickname, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, nickname, email, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username, password, nickname, email, **kwargs)

    def create_superuser(self, username, password, nickname, email, **kwargs):
        kwargs['is_superuser'] = True
        return self._create_user(username, password, nickname, email, **kwargs)


class MemberGender(models.IntegerChoices):
    MAN = 0, '男'
    WOMAN = 1, '女'
    SECRET = 2, '保密'


class Member(AbstractBaseUser, PermissionsMixin):
    """
    自定义用户类
    """
    uid = ShortUUIDField(primary_key=True)
    username = models.CharField('用户名', max_length=16, unique=True)
    email = models.EmailField('邮箱', blank=True)
    mobile = models.CharField('手机号', max_length=11, blank=True)
    nickname = models.CharField('昵称', max_length=20, unique=True, db_index=True)
    real_name = models.CharField('真实姓名', max_length=20, db_index=True)
    gender = models.SmallIntegerField('性别', choices=MemberGender.choices, default=MemberGender.SECRET)
    avatar = models.ImageField('头像', upload_to=_user_directory_path, default='user/head/default.png')
    sign = models.CharField('个性签名', max_length=60, default='我们的征途是星辰大海!')
    date_joined = models.DateTimeField('注册时间', auto_now_add=True)
    exp = models.IntegerField('经验值', default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname']
    EMAIL_FIELD = 'email'

    objects = MemberManager()

    class Meta:
        verbose_name = verbose_name_plural = '用户'
        db_table = 'member'

    def __str__(self):
        return self.nickname

    get_full_name = __str__
    get_short_name = __str__

    @property
    def token(self):
        """
        使用jwt加密生成一个token,返回
        :return:
        """
        token = jwt.encode({
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'data': {
                'username': self.username
            }
        }, JWT_KEY, algorithm='HS256')
        return token.decode('utf-8')


class Clazz(models.Model):
    """
    班级模型
    学生与班级为一对多关系
    一个班级只能有一个班长
    """
    name = models.CharField('班名', max_length=15)
    monitor = models.OneToOneField(
        'Student', verbose_name='班长', on_delete=models.SET_NULL,
        null=True, db_constraint=False, related_name='manage_clazz')

    class Meta:
        verbose_name = verbose_name_plural = '班级'
        db_table = 'clazz'


class League(models.Model):
    """
    社团模型
    用户与社团为多对多关系
    一个社团只能有一个社长
    """
    name = models.CharField('社团名称', max_length=15, unique=True)
    code = models.CharField('社团代码', max_length=10, unique=True)
    desc = models.CharField('社团宣言', max_length=60)
    president = models.OneToOneField(
        'Member', verbose_name='社长', on_delete=models.SET_NULL,
        null=True, db_constraint=False, related_name='my_manage_league')
    members = models.ManyToManyField('Member', through='MemberWithLeagueShip',
                                     related_name='leagues')

    class Meta:
        verbose_name = verbose_name_plural = '社团'
        db_table = 'league'


class MemberWithLeagueShip(models.Model):
    """
    用户与社团的多对多关系模型
    """
    date_joined = models.DateTimeField('加入时间', auto_now_add=True)
    member = models.ForeignKey(
        'Member', verbose_name='社团成员', on_delete=models.CASCADE,
        db_constraint=False, related_name='league_ship')
    league = models.ForeignKey(
        'League', verbose_name='所属社团', on_delete=models.CASCADE,
        db_constraint=False, related_name='member_ship')

    class Meta:
        verbose_name = verbose_name_plural = '用户&社团多对多表'


class Student(models.Model):
    """
    学生模型, 用户模型的扩展身份
    """
    stu_id = models.CharField('学号', max_length=12, primary_key=True)
    member = models.OneToOneField('Member', on_delete=models.CASCADE, db_constraint=False)
    clazz = models.ForeignKey('Clazz', on_delete=models.SET_NULL, null=True, db_constraint=False,
                              related_name='students')

    class Meta:
        verbose_name = verbose_name_plural = '学生'
        db_table = 'student'


class Course(models.Model):
    """
    课程模型, 与老师为多对多关系
    这里就简单和老师联系,不和学生联系了.
    """
    name = models.CharField('课程名称', max_length=20, unique=True)
    code = models.CharField('课程代码', max_length=15, unique=True)
    desc = models.CharField('课程简介', max_length=60)

    class Meta:
        verbose_name = verbose_name_plural = '课程'
        db_table = 'course'


class Teacher(models.Model):
    """
    老师模型, 用户模型的扩展身份
    """
    teacher_id = models.CharField('教职工号', max_length=12, primary_key=True)
    title = models.CharField('职称', max_length=20, blank=True)
    member = models.OneToOneField('Member', on_delete=models.CASCADE, db_constraint=False)
    teach_courses = models.ManyToManyField('Course', verbose_name='所教课程', db_constraint=False,
                                           null=True, related_name='teachers')

    class Meta:
        verbose_name = verbose_name_plural = '老师'
        db_table = 'teacher'
