# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class VipPipeline(object):
#     def process_item(self, item, spider):
#         return item
#


from openpyxl import Workbook
from pymysql import cursors

import pymysql

# twisted: 用于异步写入(包含数据库)的框架，cursor.execute()是同步写入
from twisted.enterprise import adbapi

#
# class VipPipeline(object):
    # def __init__(self):
    #     self.wb=Workbook()
    #     self.ws=self.wb.active
    #     self.ws.append(['phone','coupon_name','fav','buy','create_time','city','province'])
    #
    # def process_item(self, item, spider):
    #     try:
    #         line=[item['phone'],item['coupon_name'],item['fav'],item['buy'],item['create_time'],item['city'],item['province']]
    #         self.ws.append(line)
    #         self.wb.save(r'/root/vip/vip/1.xlsx')
    #         #self.wb.save(r'E:\VUE\vip\vip\1.xlsx')
    #
    #     except Exception as e:
    #         print(e)
    #     return item

import pymysql
from twisted.enterprise import adbapi

class DoubanbookPipeline(object):


    def __init__(self,host,user,password,port,db):
        params=dict(
            host = host,
            user = user,
            password = password,
            db = db,
            port=port,
            charset = 'utf8',  # 不能用utf-8

            cursorclass = pymysql.cursors.DictCursor
        )
        # 使用Twisted中的adbapi获取数据库连接池对象
        self.dbpool=adbapi.ConnectionPool('pymysql',**params)

    @classmethod
    def from_crawler(cls,crawler):
        # 获取settings文件中的配置
        host=crawler.settings.get('HOST')
        user=crawler.settings.get('USER')
        password=crawler.settings.get('PASSWORD')
        port =crawler.settings.get('PROT')
        db=crawler.settings.get('DB')
        return cls(host,user,password,port,db)

    def process_item(self,item,spider):
        # 使用数据库连接池对象进行数据库操作,自动传递cursor对象到第一个参数
        query=self.dbpool.runInteraction(self.do_insert,item)
        # 设置出错时的回调方法,自动传递出错消息对象failure到第一个参数
        query.addErrback(self.on_error,spider)
        return item

    def do_insert(self,cursor,item):
        print('1111111111111100000')
        sql= "INSERT INTO vip(phone, buy, create_time, city, province) VALUES ( '%s', '%s', '%s', '%s', '%s');" % (item['phone'],item['buy'], item['create_time'], item['city'], item['province'])
        cursor.execute(sql)

        print('正在写入数据！***********************')

    def on_error(self,failure,spider):
        try:
            spider.logger.error(failure)
        except Exception as e:
            print(e)
            pass


