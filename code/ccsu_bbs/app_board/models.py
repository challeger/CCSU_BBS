from os import path
from uuid import uuid4

from django.db import models


def _area_directory_path(instance, filename):
    filename = '{}.{}'.format(uuid4().hex[:12], 'jpg')  # 随机生成文件名
    return path.join('board', 'area', filename)  # 返回生成的文件名


def _board_directory_path(instance, filename):
    filename = '{}.{}'.format(uuid4().hex[:12], 'jpg')  # 随机生成文件名
    return path.join('board', 'board', filename)  # 返回生成的文件名


class Area(models.Model):
    title = models.CharField('分区名', max_length=10, unique=True, db_index=True)
    code = models.CharField('分区代码', max_length=10, unique=True, db_index=True)
    desc = models.CharField('分区简介', max_length=60)
    icon = models.ImageField('分区图标', upload_to=_area_directory_path, default='board/area/default.png')
    managers = models.ManyToManyField(
        'app_user.Member', verbose_name='区务', db_constraint=False,
        blank=True, related_name='manage_areas')

    class Meta:
        verbose_name = verbose_name_plural = '分区'
        db_table = 'area'


class Board(models.Model):
    title = models.CharField('板块名', max_length=20, unique=True, db_index=True)
    code = models.CharField('板块代码', max_length=20, unique=True, db_index=True)
    desc = models.CharField('板块简介', max_length=60)
    icon = models.ImageField('板块图标', upload_to=_board_directory_path, default='board/board/default.png')

    belong_area = models.ForeignKey(
        'Area', verbose_name='所属分区', on_delete=models.CASCADE,
        related_name='boards', db_constraint=False)
    managers = models.ManyToManyField(
        'app_user.Member', verbose_name='版务', db_constraint=False,
        blank=True, related_name='manage_boards')

    class Meta:
        verbose_name = verbose_name_plural = '板块'
        db_table = 'board'


class Topic(models.Model):
    title = models.CharField('标题', max_length=20, db_index=True)
    content = models.TextField('正文')
    desc = models.CharField('摘要', max_length=200)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    owner = models.ForeignKey('app_user.Member', verbose_name='发布者', on_delete=models.CASCADE,
                              db_constraint=False)
    board = models.ForeignKey(Board, verbose_name='所属分区', on_delete=models.CASCADE,
                              db_constraint=False)

    class Meta:
        verbose_name = verbose_name_plural = '贴子'
        ordering = ['update_time', 'created_time', 'title']

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField('回复内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='回复时间')

    owner = models.ForeignKey('app_user.Member', verbose_name='回复人', on_delete=models.CASCADE,
                              db_constraint=False, db_index=True)
    target_topic = models.ForeignKey(Topic, verbose_name='回复贴子', on_delete=models.CASCADE,
                                     db_constraint=False, db_index=True)
    target_comment = models.ForeignKey('Comment', verbose_name='回复层', null=True, on_delete=models.CASCADE,
                                       db_constraint=False)

    class Meta:
        verbose_name = verbose_name_plural = '回复'

    def __str__(self):
        return f'{self.owner}的回复'


class Announcement(models.Model):
    """公告"""
    title = models.CharField(max_length=64, verbose_name='公告标题')
    content = models.TextField(max_length=255, verbose_name='公告内容')
    owner = models.ForeignKey('app_user.Member', verbose_name='发布者', on_delete=models.CASCADE, db_constraint=False)  # 级联删除
    created_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        abstract = True


class SiteAnnouncement(Announcement):
    """站点公告"""
    class Meta:
        verbose_name = verbose_name_plural = '站点公告'


class AreaAnnouncement(Announcement):
    """分区的公告"""
    area = models.ForeignKey(Area, verbose_name='目标分区', on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        verbose_name = verbose_name_plural = '分区公告'


class BoardAnnouncement(Announcement):
    """板块的公告"""
    board = models.ForeignKey(Board, verbose_name='目标板块', on_delete=models.CASCADE, db_constraint=False)

    class Meta:
        verbose_name = verbose_name_plural = '板块公告'
