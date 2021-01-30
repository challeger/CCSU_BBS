#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能: 权限认证装饰器
每天都要开心:)
"""
from app_user.models import Member, Student, Teacher


def is_login(func):
    """
    判断是否登录
    :param func:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        if isinstance(request.user, Member):
            return func(request, *args, **kwargs)
        # TODO 之后改为重定向到登录页面
        pass
    return wrapper


def is_student(func):
    """
    判断是否是学生
    :param func:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        pass
    return wrapper


def is_teacher(func):
    """
    判断是否是教师
    :param func:
    :return:
    """
    def wrapper(request, *args, **kwargs):
        pass
    return wrapper
