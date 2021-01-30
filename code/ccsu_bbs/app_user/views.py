from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET

from utils.permission import is_login
from .models import (
    Member, Student, Teacher
)
from ..utils.resp import *


@require_POST
def login(request):
    """
    用户登录
    :param request:
    :return:
    """
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
        member = Member.objects.get(username=username)
    except Member.DoesNotExist:
        return AuthFailedResponse({
            'msg': '用户未注册!'
        })

    # 检查用户名密码是否正确
    if not member.check_password(password):
        return AuthFailedResponse({
            'msg': '用户名或密码错误!'
        })

    # 正确则登录成功
    resp = SuccessResponse({
        'msg': '登录成功!'
    })
    # 设置cookie,登录成功
    resp.set_cookie('Token', member.token, 60 * 60 * 24)
    return resp


@require_POST
def register(request):
    """
    注册接口
    :param request:
    :return:
    """
    pass


@require_POST
@is_login
def modify_user_info(request):
    """
    修改用户个人信息接口
    :param request:
    :return:
    """
    pass


@require_POST
@is_login
def modify_password(request):
    """
    修改用户密码
    :param request:
    :return:
    """
    pass
