#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hdfs.client import Client
from IntelligentSystem.settings import hdfs_host, hdfs_uname, hdfs_port


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
