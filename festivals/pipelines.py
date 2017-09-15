# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from festivals.FestivalCsvExporter import FestivalCsvExporter


class FestivalsPipeline(object):
    fields_to_export = ['FESTIVAL_NAME', 'EVENT_ON', 'CATEGORY', 'URL', 'SOCIAL', 'EMAIL', 'ADDRESS', 'ZIP_CODE', 'CITY']

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        # nord-pas-de-calais
        self.file_nord = open('/Users/sashko/Documents/workspace/festivals/festivals-nord-pas-de-calais.csv', 'w+b')
        self.file_all = open('/Users/sashko/Documents/workspace/festivals/festivals-all.csv', 'w+b')
        self.exporter_nord = CsvItemExporter(self.file_nord)
        self.exporter_all = CsvItemExporter(self.file_all)
        self.exporter_nord.start_exporting()
        self.exporter_all.start_exporting()
        self.exporter_all.fields_to_export = self.fields_to_export
        self.exporter_nord.fields_to_export = self.fields_to_export

    def spider_closed(self, spider):
        self.exporter_nord.finish_exporting()
        self.exporter_all.finish_exporting()
        self.file_nord.close()

    def process_item(self, item, spider):
        if item['isRegion'] == True:
            self.exporter_nord.export_item(item)
        self.exporter_all.export_item(item)
        return item
