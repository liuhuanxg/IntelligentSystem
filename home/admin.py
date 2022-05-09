import os
import json
from django.contrib import admin
from home.models import *
from utils.hdfs_utils import upload_hdfs, down_load
from threading import Thread
from IntelligentSystem.settings import BASE_DIR
from queue import Queue
import time
from urllib.parse import quote, unquote
from django.utils.html import format_html
import traceback

admin.site.site_header = '遥感数据服务平台管理后台'
admin.site.site_title = '遥感数据服务平台管理后台'

xml_queues = Queue()


class ParseXml(Thread):
    def __init__(self):
        super(ParseXml, self).__init__()

    def run(self) -> None:
        while True:
            try:
                if xml_queues.empty():
                    time.sleep(1)
                    print(1111)
                    continue
                # {"id=obj.id, "xml_path=img_xml}
                """
                {
                    "img_name=100,
                    "img_source=100,
                    "img_length=100,
                    "img_width=100,
                    "img_height=100,
                    "station=100,
                    "type=100,
                }
                """
                data = xml_queues.get()
                image_id = data.get("id", 0)
                print("img_if:{}".format(image_id))
                with open(data["xml_path"], "r") as fp:
                    file_content = fp.read()
                    content = json.loads(file_content)
                    print("content:{}".format(content))
                    station = content.get("station", "")
                    img_type = content.get("type", "")
                    site = ImageStation.objects.filter(site_name=station)
                    if site.exists():
                        station_id = site[0].id
                    else:
                        station_obj = ImageStation()
                        station_obj.site_name = station
                        station_obj.save()
                        station_id = station_obj.id
                    t_type = ImageType.objects.filter(type_name=img_type)
                    if t_type.exists():
                        type_id = t_type[0].id
                    else:
                        type_obj = ImageType()
                        type_obj.type_name = img_type
                        type_obj.save()
                        type_id = type_obj.id
                    res = Image.objects.filter(id=image_id).update(
                        img_name=content.get("img_name", ""),
                        img_source=content.get("img_source", ""),
                        img_length=content.get("img_length", ""),
                        img_width=content.get("img_width", ""),
                        img_height=content.get("img_height", ""),
                        station=station_id,
                        type=type_id,
                        img_des=file_content
                    )
                    print("res:{}".format(res))
            except:
                print(traceback.format_exc())
                time.sleep(1)


for _ in range(1):
    parse = ParseXml()
    parse.start()


# 类型管理
@admin.register(ImageType)
class TypeAdmin(admin.ModelAdmin):
    list_display = ["type_name", "type_status", "add_time", "modify_time"]
    search_fields = ["type_name"]
    list_per_page = 30


# 站点管理
@admin.register(ImageStation)
class StationAdmin(admin.ModelAdmin):
    list_display = ["site_name", "site_status", "add_time", "modify_time"]
    search_fields = ["site_name"]
    list_per_page = 50


# 图片管理
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["img_name", "img_length", "img_width", "img_height", "img_source", "station", "type", "operator"]
    actions = ['delete_selected']
    search_fields = ["img_name", "make_published"]
    list_per_page = 50
    list_filter = ["img_name"]

    def operator(self, obj):
        return format_html(
            '<a href="/batch_upload/">批量导入<a/>'
        )

    operator.short_description = '批量导入'

    def save_model(self, request, obj, form, change):
        path = request.path

        super(ImageAdmin, self).save_model(request, obj, form, change)
        print(path)
        static_path = os.path.join(BASE_DIR, "static")
        img_path = unquote(os.path.join(static_path, obj.img_path.url), "utf-8")
        print(dir(obj.img_xml))
        img_xml = unquote(os.path.join(static_path, obj.img_xml.url))
        xml_queues.put({"id": obj.id, "xml_path": img_xml})
        if path.find("change") == -1:
            t1 = Thread(target=upload_hdfs, args=(img_path,))
            t2 = Thread(target=upload_hdfs, args=(img_xml,))
            t1.start()
            t2.start()
