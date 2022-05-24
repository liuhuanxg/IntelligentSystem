#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
from IntelligentSystem.settings import hdfs_host, hdfs_uname, hdfs_port, thrift_port
from IntelligentSystem.settings import img_base_path, des_file_base_path


def upload_path_handler(file_type="img"):
    now = datetime.datetime.now()
    if file_type == "img":
        base_path = img_base_path
    else:
        base_path = des_file_base_path
    file_path = os.path.join(base_path, str(now.year), str(now.month), str(now.day))
    return file_path
