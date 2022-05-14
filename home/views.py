import os
import zipfile
import time
import traceback
from django.shortcuts import render, redirect
from django.http import JsonResponse, StreamingHttpResponse
from .models import *
from django.shortcuts import HttpResponseRedirect
from home.forms import UserForm
from IntelligentSystem.common import setPassword, loginValid, send_email, set_page
from string import ascii_letters, digits
import random
from django.db.models import Q, F
import datetime
from .admin import xml_queues
from utils import utils

from IntelligentSystem.settings import (
    MEDIA_ROOT,
    img_base_path,
    des_file_base_path
)


@loginValid
def index(request):
    img_number = Image.objects.count()
    type_number = ImageType.objects.count()
    imagestation_number = ImageStation.objects.count()
    return render(request, "common/index.html", locals())


# 注册页面
def register(request):
    errors = ""
    if request.method == "POST":
        userform = UserForm(request.POST)  # 将请求的数据加入表单进行校验
        if userform.is_valid():
            username = userform.cleaned_data.get("username")  # 校验过的数据
            password = userform.cleaned_data.get("password")
            password_confirm = request.POST.get("password_confirm")
            if password == password_confirm:
                # 数据库保存用户注册信息
                user = User()
                user.username = username
                user.password = setPassword(setPassword(password))
                user.save()
            return HttpResponseRedirect("/login/")  # 如果注册成功，跳转到登陆
        else:
            errors = userform.errors
    return render(request, "common/register.html", {"errors": errors})


# 登录
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        u = User.objects.filter(username=username, password=setPassword(setPassword(password)))
        if u.exists():
            response = HttpResponseRedirect("/")
            response.set_cookie("username", username)
            request.session["username"] = username
            request.session["user_id"] = u[0].id
            request.session["image"] = u[0].image.url
            return response

    return render(request, "common/login.html")


# 退出
def logout(request):
    response = HttpResponseRedirect("/login/")
    try:
        response.delete_cookie("username")
        del request.session["username"]
        del request.session["user_id"]
        del request.session["Image"]
    except:
        pass
    return response


# 个人信息
@loginValid
def user_info(request):
    user_id = request.session.get("user_id")
    user = User.objects.filter(id=user_id)
    if user.exists():
        user = user[0]
        return render(request, "common/user_info.html", locals())
    else:
        return render(request, "common/pages-404.html")


# 修改个人信息
@loginValid
def change_userinfo(request):
    user_id = request.session.get("user_id")
    user = User.objects.filter(id=user_id)

    if not user.exists():
        return render(request, "common/pages-404.html")

    if request.method == "POST":
        data = request.POST
        nick_name = data.get("nick_name")
        gender = data.get("gender")
        phone = data.get("phone")
        email = data.get("email")
        address = data.get("address")
        image = request.FILES.get("Image")
        user.update(
            nick_name=nick_name if nick_name else F("nick_name"),
            gender=gender if gender else F("gender"),
            phone=phone if phone else F("phone"),
            email=email if email else F("email"),
            address=address if address else F("address")
        )
        if Image:
            user = user[0]
            user.image = image
            user.save()
        return redirect("home:user_info")

    return render(request, "common/change_userinfo.html", {"user": user[0]})


# 修改密码
@loginValid
def change_password(request):
    user_id = request.session.get("user_id")
    error = ""
    if request.method == "POST":
        data = request.POST
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        password_sure = data.get("password_sure")
        user = User.objects.filter(id=user_id, password=setPassword(setPassword(old_password)))
        if new_password == password_sure and user.exists():
            user.update(password=setPassword(setPassword(new_password)))
            return redirect("home:logout")
        else:
            error = "原密码错误或两次密码不一致！"
    return render(request, "common/change_password.html", {"error": error})


# 忘记密码
def forget_password(request):
    error = ""
    if request.method == "POST":
        data = request.POST
        email = data.get("email")
        code = data.get("code")
        password = data.get("password")
        alternative_code = request.session.get("code")
        alternative_email1 = request.session.get("email")
        if email == alternative_email1 and code == alternative_code:
            User.objects.filter(email=email).update(password=setPassword(setPassword(password)))
            return redirect("home:login")
        error = "邮箱或验证码不正确，请确认！"
    return render(request, "common/forget_password.html", {"error": error})


# ajax 发送验证码
def send_code(request):
    response = {"status": 0, "data": "邮箱有误，请确认邮箱"}
    email = request.GET.get("email")
    u = User.objects.filter(email=email)
    if u.exists():
        alternate_string = ascii_letters + digits
        str1 = ""
        for _ in range(6):
            str1 += random.choice(alternate_string)
        print(str1)
        result = send_email(str1, email)
        if result:
            response["status"] = 1
            response["data"] = "验证码已发送，请查收"
            request.session["code"] = str1
            request.session["email"] = email
    return JsonResponse(response)


# 图片信息
@loginValid
def image_message(request):
    type_name = request.GET.get("type_name", "")
    image_name = request.GET.get("image_name", "")
    print(type_name, image_name)
    if image_name or type_name:
        image_list = Image.objects.filter(
            Q(img_name__icontains=image_name) or Q(type__type_name__icontains=type_name), img_status=1).order_by("-id")
    else:
        image_list = Image.objects.all().order_by("-id")
    print(image_list)
    page = request.GET.get("page", 0)
    data, page_list = set_page(image_list, 20, page)
    return render(request, "common/image_message.html",
                  {"data": data, "page_list": page_list, "type_name": type_name, "image_name": image_name})


# 图片详情
@loginValid
def image_detail(request, id):
    image = Image.objects.filter(id=id)
    if not image.exists():
        return render(request, "common/pages-404.html")
    image = image[0]
    return render(request, "common/image_detail.html", {"image": image})


# 站点信息
@loginValid
def site_message(request):
    site_name = request.GET.get("site_name", "")
    if site_name:
        imagestation_list = ImageStation.objects.filter(site_name__icontains=site_name).order_by("id")
    else:
        imagestation_list = ImageStation.objects.all().order_by("id")
    page = request.GET.get("page", 0)
    data, page_list = set_page(imagestation_list, 20, page)
    return render(request, "common/station_message.html",
                  {"data": data, "page_list": page_list, "site_name": site_name})


# 站点详情
@loginValid
def site_detail(request, id):
    imagestations = ImageStation.objects.filter(id=id)
    if not imagestations.exists():
        return render(request, "common/pages-404.html")
    site = imagestations[0]
    images = Image.objects.filter(station_id=id).order_by("-add_time")
    return render(request, "common/site_detail.html", {"site": site, "images": images})


# 综合信息
@loginValid
def informations(request):
    site_name = request.GET.get("site_name", "")
    if site_name:
        imagestation_list = ImageStation.objects.filter(site_name__icontains=site_name).order_by("id")
    else:
        imagestation_list = ImageStation.objects.all().order_by("id")
    page = request.GET.get("page", 0)
    data, page_list = set_page(imagestation_list, 20, page)
    return render(request, "common/infomations.html",
                  {"data": data, "page_list": page_list, "site_name": site_name})


# 获取图片数量
def get_images_count(request):
    ret = {"status": 1, "data": {}}
    seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    imags = Image.objects.filter(add_time__gt=seven_days_ago)
    dates = []
    images_group_by_site = {}
    label2_data = {}
    label3_data = {}

    # 柱状图
    for i in range(0, 7):
        date = datetime.datetime.now() - datetime.timedelta(days=i)
        date = "{:%Y-%m-%d}".format(date)
        print(date)
        if date not in dates:
            dates.append(date)
    for image in imags:
        date = "{:%Y-%m-%d}".format(image.add_time)
        if not image.station:
            station = "default"
        else:
            station = image.station.site_name

        if not image.type:
            type_name = "default"
        else:
            type_name = image.type.type_name

        if station not in images_group_by_site:
            images_group_by_site[station] = {date: 0 for date in dates}

        label2_data[station] = label2_data.get(station, 0) + 1
        label3_data[type_name] = label3_data.get(type_name, 0) + 1
        images_group_by_site[station][date] = images_group_by_site[station].get(date, 0) + 1
    laebl1_series = []
    for station, count in images_group_by_site.items():
        laebl1_series.append(
            {
                "name": station,
                "type": 'bar',
                "stack": 'total',
                "label": {
                    "show": True
                },
                "emphasis": {
                    "focus": 'series'
                },
                "data": list(count.values())
            }
        )

    option = {
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
                "type": 'shadow'
            }
        },
        "legend": {},
        "grid": {
            "left": '3%',
            "right": '4%',
            "bottom": '3%',
            "containLabel": True
        },
        "xAxis": {
            "type": 'value'
        },
        "yAxis": {
            "type": 'category',
            "data": dates
        },
        "series": laebl1_series
    }

    label2_options = {
        "title": {
            "text": '各地点数据占比',
            "subtext": 'real data',
            "left": 'center'
        },
        "tooltip": {
            "trigger": 'item'
        },
        "legend": {
            "orient": 'vertical',
            "left": 'left'
        },
        "series": [
            {
                "name": 'Access From',
                "type": 'pie',
                "radius": '50%',
                "data": [{"value": value, "name": station} for station, value in label2_data.items()],
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": 'rgba(255, 255, 255, 1)'
                    }
                }
            }
        ]
    }
    label3_options = {
        "title": {
            "text": '各类型数据占比',
            "subtext": 'real data',
            "left": 'center'
        },
        "tooltip": {
            "trigger": 'item'
        },
        "legend": {
            "orient": 'vertical',
            "left": 'left'
        },
        "series": [
            {
                "name": 'Access From',
                "type": 'pie',
                "radius": '50%',
                "data": [{"value": value, "name": type_name} for type_name, value in label3_data.items()],
                "emphasis": {
                    "itemStyle": {
                        "shadowBlur": 10,
                        "shadowOffsetX": 0,
                        "shadowColor": 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    }
    ret["data"]["label1"] = option
    ret["data"]["label2_options"] = label2_options
    ret["data"]["label3_options"] = label3_options
    return JsonResponse(ret)


# 保存图片
def save_file(received_file, filename):
    print("received_file:{},filename:{}".format(received_file, filename))
    with open(filename, 'wb')as f:
        f.write(received_file.read())


# 批量上传
def batch_upload(request):
    data = request.FILES
    count = 1
    print(list(data.items()))
    while True:
        img_name = data.get("img_name" + str(count))
        img_json = data.get("img_json" + str(count))

        if not img_name or not img_json:
            break
        image = Image()
        img_name_path = "".join(str(time.time()).split(".")) + img_name.name
        img_path = os.path.join(MEDIA_ROOT, img_base_path, img_name_path)
        save_file(img_name, img_path)
        img_json_name = "".join(str(time.time()).split(".")) + img_json.name
        xml_path = os.path.join(MEDIA_ROOT, des_file_base_path, img_json_name)
        save_file(img_json, xml_path)
        image.img_name = "this is name"
        image.img_path = os.path.join(img_base_path, img_name_path)
        image.img_json = os.path.join(des_file_base_path, img_json_name)
        image.save()
        count += 1
        xml_queues.put({"id": image.id, "xml_path": xml_path})
        utils.start_thread()
    return render(request, "common/batch_upload.html")


# 下载文件
def filestream(filepath, chunk_size=512):
    file = open(filepath, "rb")
    while True:
        stream = file.read(chunk_size)
        if stream:
            yield stream
        else:
            break


# 批量下载
def batch_download(request):
    data = request.GET
    if data.get("download"):
        images = Image.objects.all()
        startdir = MEDIA_ROOT
        ret_file_name = "all" + '.zip'
        file_news = os.path.join(MEDIA_ROOT, ret_file_name)
        z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
        paths = [os.path.join(startdir, img_base_path), os.path.join(startdir, des_file_base_path)]
        for path in paths:
            for dirpath, dirnames, filenames in os.walk(path):
                fpath = dirpath.replace(startdir, '')
                fpath = fpath and fpath + os.sep or ''
                for filename in filenames:
                    z.write(os.path.join(dirpath, filename), fpath + filename)
        z.close()
        resp = StreamingHttpResponse(filestream(file_news))
        resp['content_type'] = "application/octet-stream"
        resp['Content-Disposition'] = 'attachment; filename=' + os.path.basename(ret_file_name)
        return resp
    return render(request, "common/batch_download.html")


def load_stations(request):
    resp = {"status": 1, "data": {"degrees": []}}
    try:
        stations = ImageStation.objects.filter(site_status=1).order_by("-modify_time")
        for station in stations:
            images = Image.objects.filter(station_id=station.id).order_by("-add_time")
            images_message = """"""
            for image in images:
                images_message += """
                <p>图像名称：{}；上传时间：{}</p>\n
                <img width=\"450\" height=\"200\" src=\"/static/{}\"></img>\n  
                """.format(image.img_name, image.add_time, image.img_path.url)
            resp["data"]["degrees"].append({
                "latitude": station.latitude,
                "longitude": station.longitude,
                "name": station.site_name,
                "images": images_message
            })
    except:
        resp["status"] = 0
        print(traceback.format_exc())
    return JsonResponse(resp)
