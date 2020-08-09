# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class IledPipeline:
    def process_item(self, item, spider):
        item['url'] = 'https://iledebeaute.ru' + item['url'].strip()
        return item
