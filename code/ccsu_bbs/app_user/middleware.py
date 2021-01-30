#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能: 
每天都要开心:)
"""
from time import time

import jwt
from django.utils.deprecation import MiddlewareMixin

from app_user.models import Member
from ccsu_bbs.settings import JWT_KEY


class LoginMiddleware(MiddlewareMixin):
    """
    登录验证中间件
    """
    def process_request(self, request):
        token = request.COOKIES.get('Token')
        if token:
            try:
                content = jwt.decode(token, key=JWT_KEY)
                # 判断是否已经过期
                if time() < content['exp']:
                    request.user = Member.objects.get(username=content['data']['username'])
            except (KeyError, jwt.exceptions.DecodeError):
                # TODO 后期考虑加上日志
                pass
            except Member.DoesNotExist:
                # TODO 后期考虑加上日志
                pass
