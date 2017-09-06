#!/usr/bin/python3
# _*_ coding:utf-8 _*_
__author__ = 'anyco'

import requests,time
from lxml import etree
from proxies_init import Proxies_init

class Proxies_data:
    def __init__(self,header=None,proxy_page=None,pagination=2,phantomjsPath=None):
        self.Instance = Proxies_init()
        self.header = self.Instance.get_header()
        self.pagination = pagination
        self.proxy_page = 'http://www.kuaidaili.com/free/inha/%s/' %(self.pagination)

    def analyze_page(self,dbase=None):
        self.dbase = list()
        req = requests.session()
        index_data = etree.HTML(self.Instance.page_count()[1].text)
        print(self.Instance.page_count()[1].status_code)
        result = index_data.xpath('//*[@id="list"]/table/tbody/tr[1]/td[1]/text()')
        return result[0]


if __name__ == '__main__':
    ClassInstance = Proxies_data()
    print(ClassInstance.analyze_page())
