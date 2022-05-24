#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hdfs.client import Client
import os

hdfs_host = 'http://43.138.217.253'
hdfs_port = 61001
hdfs_uname = "root"


class HdfsWrapper():
    def __init__(self):
        self.client = Client("{}:{}".format(hdfs_host, hdfs_port), root=hdfs_uname, timeout=10)
        self.input_base_path = "/input"

    def upload_hdfs(self, file_path):
        print("upload_hdfs file_path:{}".format(file_path))
        ret = self.client.upload(self.input_base_path, file_path)
        print(ret)

    def down_load(self, file_name, file_path):
        ret = self.client.download('{}/{}'.format(self.input_base_path, file_name), file_path)
        print(ret)


if __name__ == '__main__':
    pwd = os.path.abspath(".")
    # print(pwd)
    wrapper = HdfsWrapper()
    file_name = "test.txt"
    path = os.path.join(pwd, "test.txt")
    wrapper.upload_hdfs(path)
    # file_path = os.path.join(pwd, "tmp", file_name)
    # wrapper.down_load(file_name, file_path)
