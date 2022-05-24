import os
import json
from django.contrib import admin
from home.models import *
from utils.hdfs_utils import HdfsWrapper
from utils.hbase_utils import HbaseWrapper
from threading import Thread
from IntelligentSystem.settings import BASE_DIR, MEDIA_ROOT
from queue import Queue
import time
from urllib.parse import quote, unquote
from django.utils.html import format_html
import traceback
from utils.utils import xml_queues, hdfs_queues, hbase_queuess, start_other_thread
import PIL

admin.site.site_header = '遥感数据服务平台管理后台'
admin.site.site_title = '遥感数据服务平台管理后台'


# 类型管理
@admin.register(ImageType)
class TypeAdmin(admin.ModelAdmin):
    list_display = ["type_name", "type_status", "add_time", "modify_time"]
    search_fields = ["type_name", "type_status"]
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
    list_display = ["img_name", "file_size", "img_width", "img_height", "img_source", "station", "type", "operator"]
    actions = ['delete_selected']
    search_fields = ["img_name"]
    list_per_page = 50
    list_filter = ["img_name"]
    readonly_fields = ["hbase_row_key"]

    def operator(self, obj):
        return format_html(
            '<a href="/batch_upload/" target="_blank">批量导入<a/>'
        )

    operator.short_description = '批量导入'

    def save_model(self, request, obj, form, change):
        super(ImageAdmin, self).save_model(request, obj, form, change)
        print("form.changed_data:{}".format(form.changed_data))
        # 图片有更新
        if "img_path" in form.changed_data:
            img_path = unquote(os.path.join(MEDIA_ROOT, obj.img_path.path), "utf-8")
            if obj.img_path.path.endswith(".tif") or obj.img_path.path.endswith(".tiff"):
                img = PIL.Image.open(obj.img_path)  # image.tiff from request.FILES
                img.save(obj.img_path.path, "JPEG")
            hdfs_queues.put({"id": obj.id, "file_path": img_path})
            hbase_queuess.put({"id": obj.id, "file_path": img_path})
            start_other_thread("hdfs", 1)
            start_other_thread("hbase", 1)
        # json文件有更新
        if "img_json" in form.changed_data:
            img_json = unquote(os.path.join(MEDIA_ROOT, obj.img_json.path))
            xml_queues.put({"id": obj.id, "file_path": img_json})
            start_other_thread("parse_file", 1)
            hdfs_queues.put({"id": obj.id, "file_path": obj.img_json.path})
            start_other_thread("hdfs", 1)
            print("obj.img_json.path:{}".format(obj.img_json.path))
