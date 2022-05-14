#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hdfs.client import Client

try:
    from IntelligentSystem.settings import hdfs_host, hdfs_uname, hdfs_port
except:
    hdfs_host = 'http://43.138.217.253'
    hdfs_port = 61001
    hdfs_uname = "root"


class HdfsWrapper():
    def __init__(self):
        self.client = Client("{}:{}".format(hdfs_host, hdfs_port), root=hdfs_uname, timeout=10)

    def upload_hdfs(self, file_path):
        print("upload_hdfs file_path:{}".format(file_path))
        ret = self.client.upload('/input', file_path)
        print(ret)

    def down_load(self, file_path):
        ret = self.client.download('/input/{}'.format(file_path), file_path)
        print(ret)


if __name__ == '__main__':
    wrapper = HdfsWrapper()
    wrapper.upload_hdfs(
        "/Users/liuhuan/workspace/PythonSpace/py3projects/IntelligentSystem/static/upload/img_des/1652185727713582test.json")
