from datetime import datetime
from os import path
from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from shortuuidfield import ShortUUIDField


class MemberManager(BaseUserManager):
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


def _user_directory_path(instance, filename):
    now_date = datetime.now().strftime('%Y%m%d')  # 当天日期
    filename = '{}.{}'.format(uuid4().hex[:12], 'jpg')  # 随机生成文件名
    return path.join('user', 'head', now_date, filename)  # 返回生成的文件名


class Member(AbstractBaseUser, PermissionsMixin):
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

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.nickname


class Student(models.Model):
    member = models.OneToOneField('Member', on_delete=models.CASCADE, db_constraint=False)
    # TODO 此处应有学生的班级, 社团等外键

    class Meta:
        verbose_name = verbose_name_plural = '学生'
        db_table = 'student'


class Teacher(models.Model):
    member = models.OneToOneField('Member', on_delete=models.CASCADE, db_constraint=False)
    # TODO 此处应有老师的教学科目, 任职等

    class Meta:
        verbose_name = verbose_name_plural = '老师'
        db_table = 'teacher'
