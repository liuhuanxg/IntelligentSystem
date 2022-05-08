from django.contrib import admin
from .models import *

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
    list_display = ["img_name", "img_path", "img_source", "station", "type"]
    search_fields = ["img_name"]
    list_per_page = 50
    list_filter = ["img_name"]
