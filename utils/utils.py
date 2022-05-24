#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import json
import traceback
from threading import Thread
from queue import Queue
from home.models import *
from utils.hbase_utils import HbaseWrapper
from utils.hdfs_utils import HdfsWrapper
import PIL

xml_queues = Queue()
hdfs_queues = Queue()
hbase_queuess = Queue()


class ParseXml(Thread):
    def __init__(self):
        super(ParseXml, self).__init__()
        self.exit_count = 0

    def run(self) -> None:
        while True:
            try:
                if xml_queues.empty():
                    time.sleep(0.5)
                    self.exit_count += 1
                    if self.exit_count >= 3:
                        break
                """
                {
                    "img_name": "imgname",
                    "img_source": "其他",
                    "file_size": 100kb,
                    "station": {
                        "site_name": "上海",
                        "site_description": "站点描述",
                        "longitude": 100,
                        "latitude": 200
                    },
                    "type": {
                        "type_name": "日光",
                        "type_description": "类型描述"
                    }
                }
                """
                data = xml_queues.get()
                image_id = data.get("id", 0)
                file_path = data.get("file_path", 0)
                print("img_id:{},file_path:{}".format(image_id, file_path))
                with open(file_path, "r") as fp:
                    file_content = fp.read()
                    content = json.loads(file_content)
                    # print("content:{}".format(content))
                    station = content.get("station", {})
                    img_type = content.get("type", {})
                    site_name = station.get("site_name", "")
                    type_name = img_type.get("type_name", "")
                    print(site_name, type_name)
                    site = ImageStation.objects.filter(site_name=site_name)
                    if site.exists():
                        station_id = site[0].id
                    else:
                        station_obj = ImageStation()
                        station_obj.site_name = site_name
                        station_obj.site_description = station.get("site_description", "")
                        station_obj.longitude = station.get("longitude", 0)
                        station_obj.latitude = station.get("latitude", 0)
                        station_obj.save()
                        station_id = station_obj.id
                    t_type = ImageType.objects.filter(type_name=type_name)
                    if t_type.exists():
                        type_id = t_type[0].id
                    else:
                        type_obj = ImageType()
                        type_obj.type_name = type_name
                        type_obj.type_description = img_type.get("type_description", 0)
                        type_obj.save()
                        type_id = type_obj.id
                    res = Image.objects.filter(id=image_id).update(
                        img_name=content.get("img_name", ""),
                        img_source=content.get("img_source", ""),
                        img_status=1 if content.get("img_status", True) else 0,
                        station=station_id,
                        type=type_id,
                        img_des=file_content,
                    )
                    print("res:{}".format(res))
            except:
                print(traceback.format_exc())
                time.sleep(1)


class UploadHbaseData(Thread):
    def __init__(self):
        super(UploadHbaseData, self).__init__()
        self.exit_count = 0

    def run(self) -> None:
        while True:
            try:
                if hbase_queuess.empty():
                    time.sleep(0.5)
                    self.exit_count += 1
                    if self.exit_count >= 3:
                        break
                data = hbase_queuess.get()
                image_id = data.get("id", 0)
                file_path = data.get("file_path", "")
                row_key = "".join(str(time.time()).split("."))
                images_table_name = "images"
                chunck = open(file_path, "rb").read()
                # picture是列族名，value是可以自定义的列名 同一个表中的不同数据都可以任意添加
                attribs = {}
                image_name = file_path.split(".")[-1]
                attribs[b'picture:chunck'] = chunck
                # #info是第二个列名 这个必须是str type
                attribs[b'info:image_name'] = (str(row_key) + image_name).encode("utf-8")
                wrapper = HbaseWrapper()
                ret = wrapper.save(images_table_name, row_key, attribs)
                res = Image.objects.filter(id=image_id).update(
                    hbase_row_key=row_key,
                    file_size=filesize(os.path.getsize(file_path)),
                )
                print("image save to hbase row_key:{}, image_id:{},ret:{},res:{}".format(row_key, image_id, ret, res))
            except:
                print(traceback.format_exc())
                time.sleep(1)


def filesize(value):
    x = value
    y = 512000
    if x < y:
        value = round(x / 1024, 2)
        ext = ' KB'
    elif x < y * 1024:
        value = round(x / (1024 * 1024), 2)
        ext = ' MB'
    else:
        value = round(x / (1024 * 1024 * 1024), 2)
        ext = ' GB'
    return str(value) + ext


class UploadHdfsData(Thread):
    def __init__(self):
        super(UploadHdfsData, self).__init__()
        self.exit_count = 0

    def run(self) -> None:
        while True:
            try:
                if hdfs_queues.empty():
                    time.sleep(0.5)
                    self.exit_count += 1
                    if self.exit_count >= 3:
                        break
                data = hdfs_queues.get()
                image_id = data.get("id", 0)
                file_path = data.get("file_path", "")
                print("image_id:{},file_path:{}".format(image_id, file_path))
                wrapper = HdfsWrapper()
                ret = wrapper.upload_hdfs(file_path)
                print("image save to hdfs ret:{}".format(ret))
            except:
                print(traceback.format_exc())
                time.sleep(1)


def start_parse_xml_thread():
    for _ in range(1):
        parse = ParseXml()
        parse.start()


def start_other_thread(thread_name, number=1):
    for _ in range(number):
        if thread_name == "hdfs":
            t = UploadHdfsData()
        elif thread_name == "hbase":
            t = UploadHbaseData()
        else:
            t = ParseXml()
        t.start()


if __name__ == '__main__':
    start_parse_xml_thread()
