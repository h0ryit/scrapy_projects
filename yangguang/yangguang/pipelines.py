# -*- coding: utf-8 -*-
import codecs
import json


# class JsonWriterPipeline(object):
#     def __init__(self):
#         # 创建一个只写文件，指定文本编码格式为utf-8
#         self.filename = codecs.open("sunwz.json", 'w', encoding='utf-8')

#     def process_item(self, item, spider):
#         content = json.dumps(dict(item), ensure_ascii=False) + '\n'
#         self.filename.write(content)
#         return item

#     def spider_closed(self, spider):
#         self.filename.close()

class YangguangPipeline(object):
    def __init__(self):
        # 创建一个只写文件，指定文本编码格式为utf-8
        self.filename = codecs.open("sunwz.json", 'w', encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.filename.write(content)
        return item

    def spider_closed(self, spider):
        self.filename.close()
