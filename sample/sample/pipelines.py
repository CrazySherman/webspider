# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
class JsonWriterPipeline(object):
   
    def __init__(self):
        print '[Debugging]:: file opened for appending...'
        self.file = open('players.jl', 'ab')

    def process_item(self, item, spider):
        # self.playerfile.write(item['name'] + '    ')
        # for data in item['stats']:
        #     self.playerfile.write(data + '    ')
        # self.playerfile.write('\n')
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
