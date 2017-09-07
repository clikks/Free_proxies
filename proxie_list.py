#!/usr/bin/python3
# _*_ coding:utf-8 _*_
__author__ = 'anyco'

import requests,time,os
from lxml import etree
from proxies_init import Proxies_init

class Proxies_data:
    def __init__(self, header=None, proxy_page=None, pagination=2, phantomjsPath=None):
        self.Instance = Proxies_init()
        self.header = self.Instance.get_header()
        self.pagination = pagination
        self.proxy_page = 'http://www.kuaidaili.com/free/inha/%s/' %(self.pagination)

    def analyze_page(self, dbase=None):
        os.system('cls')
        print("Analyze webpage's data,please wait...")
        self.dbase = list()
        req = requests.session()
        index_data = etree.HTML(self.Instance.page_count()[1].text)
        # print(self.Instance.page_count()[1].status_code)  #打印proxies_init模块的page_count方法中首页的请求返回值
        xpath_rule = '//*[@id="list"]/table/tbody/tr/td[1]/text() | //*[@id="list"]/table/tbody/tr/td[2]/text()'
        result = index_data.xpath(xpath_rule)
        length = len(result)
        for i in (n for n in range(0,length) if n%2==0):
            self.dbase.append(result[i]+':'+result[i+1])
        return self.dbase


if __name__ == '__main__':
    ClassInstance = Proxies_data()
    print(ClassInstance.analyze_page())
    input()