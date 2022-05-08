#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hdfs.client import Client
from IntelligentSystem.settings import hdfs_host, hdfs_uname

client = Client(hdfs_host, root=hdfs_uname, timeout=10)


def upload_hdfs(file_path):
    print(file_path)
    ret = client.upload('/input', file_path)

    print(ret)


def down_load(file_path):
    ret = client.download('/input/{}'.format(file_path), file_path)
    print(ret)
