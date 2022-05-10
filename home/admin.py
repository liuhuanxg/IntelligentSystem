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
from utils.utils import xml_queues

admin.site.site_header = '遥感数据服务平台管理后台'
admin.site.site_title = '遥感数据服务平台管理后台'


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
        print(dir(obj.img_json))
        img_json = unquote(os.path.join(static_path, obj.img_json.url))
        xml_queues.put({"id": obj.id, "xml_path": img_json})
        if path.find("change") == -1:
            t1 = Thread(target=upload_hdfs, args=(img_path,))
            t2 = Thread(target=upload_hdfs, args=(img_json,))
            t1.start()
            t2.start()
