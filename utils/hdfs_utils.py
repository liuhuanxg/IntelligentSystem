#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File Name: hdfs_utils.py
Author: devinhliu
Mail: devinhliu@tencent.com
Created Time: 2022/5/8 14:20
"""
from hdfs.client import Client

client = Client('http://43.138.217.253:61001', root="root", timeout=10)


def upload_hdfs(data):
    client.write("/input/records.jsonl", data=data, encoding="utf-8")


def checksum():
    ret = client.list('/input')
    print(ret)
    # ret = client.upload('/input', "/Users/liuhuan/workspace/PythonSpace/py3projects/IntelligentSystem/test")
    ret = client.download('/input/test.txt', "/Users/liuhuan/workspace/PythonSpace/py3projects/IntelligentSystem/test")
    print(ret)


# with open("../static/upload/image/3D960620-D398-4D9E-AB30-ED9C39BAFF42.jpeg", "rb") as fp:
#     upload_hdfs(fp)
checksum()
