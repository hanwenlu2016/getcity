# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from ..items import VipItem


# 读取出xlsl的表格数据
def read_xlsc():
    lista = []
    try:
        # 打开表格
        #df = pd.read_excel(r'/home/vip/vip/spiders/5.xlsx')
        df = pd.read_excel(r'E:\VUE\vip\vip\spiders\1.xlsx')
        num = len(df)
        for i in range(num):
            data = {}
            data['phone'] = df.xs(i).tolist()[0]
            data['buy'] = df.xs(i).tolist()[3]
            data['create_tim'] = df.xs(i).tolist()[4]
            lista.append(data)

    except Exception as e:
        print(e)
        pass
    return lista


class VipsSpider(scrapy.Spider):
    name = 'vips'
    # allowed_domains = ['http://mobsec-dianhua.baidu.com']

    url = 'http://mobsec-dianhua.baidu.com/dianhua_api/open/location?tel='

    lista = read_xlsc()

    # 请求网站的列表
    start_urls = []

    # 拼接 url和请求号码
    for i in lista:
        phone = i.get('phone')
        start_urls.append(url + str(phone))

    def parse(self, response):
        item = VipItem()
        try:
            # 获取请求反会参数
            response_data = response.body

            # 转为字典
            str_to_dict = eval(response_data)

            # 处理数据存储
            item['phone'] = str(str_to_dict.get("response").keys())[12:23]
            item['city'] = str_to_dict.get("response").get(item['phone']).get('detail').get('area')[0].get('city')
            item['province'] = str_to_dict.get("response").get(item['phone']).get('detail').get('province')

            # 读取表格数据存储
            for j in self.lista:
                item['coupon_name'] = j.get('coupon_name')
                item['create_time'] = j.get('create_tim')
        except Exception as e:
            print(e)

        yield item
