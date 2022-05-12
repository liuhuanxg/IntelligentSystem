#!/usr/bin/env python
# -*- coding: utf-8 -*-

# conn = happybase.Connection(host="10.255.111.92",port=9090)
# #修改为：
# conn = happybase.Connection(host="10.255.111.92",port=9090,protocol='compact',transport='framed')

import happybase
from IntelligentSystem.settings import thrift_port, hdfs_host


class HbaseWrapper(object):
    def __init__(self):
        self.host = hdfs_host
        self.host = thrift_port
        self.client = happybase.Connection(hdfs_host, port=9097, protocol='compact', transport='framed')

    def get_table_list(self):
        # table = self.client.table('qian_cheng_wu_you')
        # ret = table.put("1004", {'info:name': "111111"})
        ret = self.client.tables()
        print(ret)

if __name__ == '__main__':
    wrapper = HbaseWrapper()
    ret = wrapper.get_table_list()
    print(ret)
