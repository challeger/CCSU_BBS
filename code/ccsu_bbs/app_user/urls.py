#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能: 路由分发
每天都要开心:)
"""
from django.urls import path, include
from django.views.generic import TemplateView

from app_user import views

app_name = 'Users'

urlpatterns = [
    path('api/login', views.login, name='api_login'),
    path('api/register', views.register, name='api_register')
]
