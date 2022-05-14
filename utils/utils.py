#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import json
import traceback
from threading import Thread
from IntelligentSystem.settings import BASE_DIR
from queue import Queue
from home.models import *

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
                    # print("content:{}".format(content))
                    station = content.get("station", {})
                    img_type = content.get("type", {})
                    site_name = station.get("site_name", "")
                    type_name = img_type.get("type_name", "")
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
                print("img_id:{}".format(image_id))
                row_key = time.time()

                res = Image.objects.filter(id=image_id).update(row_key=row_key)
                print("res:{}".format(res))
            except:
                print(traceback.format_exc())
                time.sleep(1)


def start_parse_xml_thread():
    for _ in range(1):
        parse = ParseXml()
        parse.start()





if __name__ == '__main__':
    start_parse_xml_thread()
