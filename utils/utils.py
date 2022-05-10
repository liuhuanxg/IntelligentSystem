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
                    if self.exit_count>=3:
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

def start_thread():
    for _ in range(1):
        parse = ParseXml()
        parse.start()

if __name__ == '__main__':
    start_thread()
