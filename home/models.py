from django.db import models
from utils.date_utils import upload_path_handler


# 用户数据表
class User(models.Model):
    class Meta:
        verbose_name = "普通用户"
        verbose_name_plural = "普通用户"

    username = models.CharField(max_length=32, unique=True, verbose_name="用户名")  # 不可以重复
    password = models.CharField(max_length=32, verbose_name="密码")
    nick_name = models.CharField(max_length=32, blank=True, null=True)
    gender = models.BooleanField(default=1, verbose_name="性别")
    phone = models.CharField(max_length=32, blank=True, null=True, unique=True, verbose_name="手机号")
    email = models.EmailField(blank=True, null=True, unique=True, verbose_name="邮箱")
    address = models.TextField(blank=True, null=True, verbose_name="地质")
    image = models.ImageField(upload_to='upload/user', default='upload/user/!happy-face.png', verbose_name="用户头像")


# 图像站点
class ImageStation(models.Model):
    class Meta:
        verbose_name = "图像站点"
        verbose_name_plural = "图像站点"

    site_name = models.CharField(verbose_name="站点名称", max_length=30, unique=True)
    site_description = models.TextField(verbose_name="站点描述")
    site_status = models.BooleanField(verbose_name="站点状态", default=1)
    add_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)
    modify_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    longitude = models.FloatField(verbose_name="经度", null=False, default=0, blank=True)
    latitude = models.FloatField(verbose_name="纬度", null=False, default=0, blank=True)
    height = models.FloatField(verbose_name="高度", null=False, default=0, blank=True)

    def __str__(self):
        return self.site_name


# 图像类型表
class ImageType(models.Model):
    class Meta:
        verbose_name = "图像类型表"
        verbose_name_plural = "图像类型表"

    type_name = models.CharField(verbose_name="类型名称", max_length=30, unique=True)
    type_description = models.TextField(verbose_name="类型描述")
    type_status = models.BooleanField(verbose_name="类型状态", default=1)
    add_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)
    modify_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    def __str__(self):
        return self.type_name


# 图片表
class Image(models.Model):
    class Meta:
        verbose_name = "图片"
        verbose_name_plural = "图片"

    img_name = models.CharField("图片名称", max_length=100)
    img_path = models.ImageField(upload_to=upload_path_handler(), verbose_name="图片路径", width_field="img_width",
                                 height_field="img_height")
    img_json = models.FileField(upload_to=upload_path_handler("des_file"), verbose_name="图像json")
    img_source = models.CharField(verbose_name="图像来源", max_length=30, null=True, blank=True)
    file_size = models.CharField(verbose_name="图片大小", max_length=30, null=True, blank=True)
    img_width = models.CharField(verbose_name="图像宽度", max_length=30, null=True, blank=True)
    img_height = models.CharField(verbose_name="图像高度", max_length=30, null=True, blank=True)
    img_status = models.BooleanField(verbose_name="图像状态", default=1)
    img_des = models.TextField(verbose_name="图像描述", null=True, blank=True)
    station = models.ForeignKey("ImageStation", on_delete=models.DO_NOTHING, verbose_name="图像站点", null=True, blank=True)
    type = models.ForeignKey("ImageType", on_delete=models.DO_NOTHING, verbose_name="图像类型", null=True, blank=True)
    add_time = models.DateTimeField(verbose_name="创建时间", auto_now=True)
    modify_time = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    hbase_row_key = models.CharField(verbose_name="hbase中的row_key", default="", max_length=100)

    def __str__(self):
        return self.img_name
