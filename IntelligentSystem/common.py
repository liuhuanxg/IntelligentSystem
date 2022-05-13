#-*-coding:utf-8 -*-

import hashlib
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


from home.models import User
from django.http import HttpResponseRedirect

# 登录校验器
def loginValid(func):
    def inner(request, *args, **kwargs):
        # 从cookie当中获取数据
        username = request.COOKIES.get("username")
        user_id = request.session.get("user_id")
        # 判断cookie存在
        if username and user_id:
            # 通过id查询用户
            user = User.objects.filter(id=user_id).first()
            if user and user.username == username:  # 证明id时这个用户名对应的id
                return func(request, *args, **kwargs)  # 跳转页面
        return HttpResponseRedirect("/login/")
    return inner



# 发送邮件
from django.core.mail import send_mail
from IntelligentSystem import settings
def send_email(message,receiver,html_message=None):
    """
    :param message: 要发送的信息
    :param receiver: 接收人
    :param html_message: html类型内容
    :return:
    """
    try:
        if html_message:
            result = send_mail("智推图片系统",message,settings.EMAIL_HOST_USER,[receiver],html_message=html_message)
        else:
            result = send_mail("智推图片系统",message,settings.EMAIL_HOST_USER,[receiver])
    except:
        result = 0
    return result


from django.core.paginator import Paginator  #引入分页器
def set_page(data,num,page):
    """
    :param data: 所有的数据
    :param num:  每页的数据
    :param page: 当前的页码
    :return:
    """
    p = Paginator(data,num)
    number = p.num_pages
    page_range = p.page_range
    try:
        page = int(page)
        data = p.page(page)
    except:
        data = p.page(1)
    if page < 5:  # 一次只返回5个页码
        page_list = page_range[:5]
    elif page + 4 > number:
        page_list = page_range[-5:]
    else:
        page_list = page_range[page - 3:page + 2]
    return data,page_list