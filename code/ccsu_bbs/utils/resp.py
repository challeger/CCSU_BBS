#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能: 自定义的一些response类
每天都要开心:)
"""
from django.http import JsonResponse


class SuccessResponse(JsonResponse):
    """
    成功时的响应
    """
    def __init__(self, data, **kwargs):
        # 成功时响应的code为1
        data['code'] = 1
        super().__init__(data, **kwargs)


class AuthFailedResponse(JsonResponse):
    """
    认证错误的响应
    """
    def __init__(self, data, **kwargs):
        # 认证失败时code为-1
        data['code'] = -1
        super().__init__(data, status=400, **kwargs)


class ValueErrorResponse(JsonResponse):
    def __init__(self, data, **kwargs):
        # 参数错误时code为-2
        data['code'] = -2
        super().__init__(data, status=400, **kwargs)
