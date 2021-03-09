#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@编写人: 小蓝同学
@文件功能: 
每天都要开心:)
"""
from django.urls import path, include
from django.views.generic import TemplateView


from app_html_route import views

app_name = 'app_html_route'

urlpatterns = [
    path('base/', TemplateView.as_view(template_name='base.html'), name='base'),
]
