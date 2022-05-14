#!/usr/bin/env python
# -*- coding: utf-8 -*-

import happybase
import time
import traceback

try:
    from IntelligentSystem.settings import thrift_port, hdfs_host
except:
    hdfs_host = '43.138.217.253'
    hdfs_port = 61001
    hdfs_uname = 'root'
    hbase_port = 16010
    thrift_port = 9095


class HbaseWrapper(object):
    def __init__(self):
        self.host = hdfs_host
        self.image_table_name = "images"
        self.client = happybase.Connection(hdfs_host, port=9097, protocol='compact', transport='framed')
        self.client.open()

    def get_table_list(self):
        """获取所有的表"""
        ret = self.client.tables()
        return ret

    def create_table(self, table_name, colums):
        """创建数据表"""
        try:
            ret = self.client.create_table(
                table_name,
                colums,
            )
            return ret
        except:
            print(traceback.format_exc())

    def save(self, table_name, row_key, data):
        """ 保存数据 """
        try:
            table = self.client.table(table_name)
            ret = table.put(row_key, data)
            return ret
        except:
            print(traceback.format_exc())

    def load_data(self, table_name, row_key):
        """ 加载数据 """
        try:
            table = self.client.table(table_name)
            data = table.row(row_key)
            return data
        except:
            print(traceback.format_exc())


if __name__ == '__main__':
    wrapper = HbaseWrapper()
    ret = wrapper.get_table_list()
    print(ret)
    # with open("../static/upload/image/1652185565920823D960620-D398-4D9E-AB30-ED9C39BAFF42.jpeg", "rb") as fp:
    #     ret = wrapper.upload_file("1652185565920823D960620-D398-4D9E-AB30-ED9C39BAFF42.jpeg", fp)
    #     print(ret)

    colums = {
        'cf1': dict(max_versions=10),
        'cf2': dict(max_versions=1, block_cache_enabled=False),
        'cf3': dict()
    }
    table_name = "test_table_name"
    # res = wrapper.create_table(table_name, colums)
    # print(res)

    row_key = "".join(str(time.time()).split("."))
    print(row_key)
    # ret = wrapper.save(
    #     table_name, row_key,
    #     {b'cf1:col1': b'value1', b'cf2:col2': b'value2'}
    # )

    # colums = {
    #     'picture': dict(max_versions=10),
    #     'info': dict(max_versions=1, block_cache_enabled=False),
    # }
    images_table_name = "images"
    # res = wrapper.create_table(images_table_name, colums)
    # ret = wrapper.get_table_list()
    # chunck = open("../static/upload/image/1652185565920823D960620-D398-4D9E-AB30-ED9C39BAFF42.jpeg", "rb").read()
    #
    # # picture是列族名，value是可以自定义的列名 同一个表中的不同数据都可以任意添加
    # attribs = {}
    # image_name = "1652185565920823D960620-D398-4D9E-AB30-ED9C39BAFF42.jpeg"
    # attribs[b'picture:chunck'] = chunck
    # # #info是第二个列名 这个必须是str type
    # attribs[b'info:image_name'] = image_name.encode("utf-8")
    # ret = wrapper.save(images_table_name, row_key, attribs)

    # print(res)
    print(wrapper.load_data(table_name, "1652532346762613"))
