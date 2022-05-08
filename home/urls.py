#-*-coding:utf-8 -*-

from django.urls import path, include, re_path
from .views import *
from django.contrib import admin


urlpatterns = [
    re_path('^$', index),
    path('index/', index),
    path('register/', register, name="register"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),

    # 个人中心
    path('user_info/', user_info, name="user_info"),
    path('change_userinfo/', change_userinfo, name="change_userinfo"),
    path('change_password/', change_password, name="change_password"),
    path('forget_password/', forget_password, name="forget_password"),
    path('send_code/', send_code, name="send_code"),

    # 信息管理
    path('image_message/', image_message, name="image_message"),
    path('image_detail/<int:id>', image_detail, name="image_detail"),
    path('site_message/', site_message, name="site_message"),
    path('site_detail/<int:id>', site_detail, name="site_detail"),
    path('informations/', informations, name="informations"),
    path('get_images_count/', get_images_count, name="get_images_count"),
]

app_name = "home"