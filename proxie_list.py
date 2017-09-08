#!/usr/bin/python3
# _*_ coding:utf-8 _*_
__author__ = 'anyco'

import requests
import time
import os
from lxml import etree
from proxies_init import Proxies_init


class Proxiesdata:
    def __init__(self):
        self.Instance = Proxies_init()
        self.header = self.Instance.get_header()
        self.page_num = self.Instance.page_count()[0]
        self.proxy_page = 'http://www.kuaidaili.com/free/inha/%s/'

    def analyze_page(self):
        os.system('cls')
        print("Analyze webpage's data,please wait...")
        self.dbase = list()
        req = requests.session()
        # index_data = etree.HTML(self.Instance.page_count()[1].text)
        # print(self.Instance.page_count()[1].status_code)  #打印proxies_init模块的page_count方法中首页的请求返回值
        # xpath_rule = '//*[@id="list"]/table/tbody/tr/td[1]/text() | //*[@id="list"]/table/tbody/tr/td[2]/text()'
        # result = index_data.xpath(xpath_rule)
        # for i in range(0,len(result),2):
        #     self.dbase.append(result[i]+':'+result[i+1])
        # return self.dbase,self.page_num

        for num in range(1, self.page_num):
            # time.
            ctl = True
            xpath_rule = '//*[@id="list"]/table/tbody/tr/td[1]/text() | //*[@id="list"]/table/tbody/tr/td[2]/text()'
            if num == 1:
                index_data = etree.HTML(self.Instance.page_count()[1].text)
                # result = index_data.xpath(xpath_rule)
            else:
                url = self.proxy_page % num
                index_data = requests.get(url, headers=self.header, timeout=5)
                count = 1
                while index_data.status_code != 200:
                    print('Request Failed! RESTART...')
                    self.header = self.Instance.get_header()
                    index_data = req.get(url, headers=self.header, timeout=5)
                    count += 1
                    if count > 10:
                        print('Content page number is %d,can not request correct page source!')
                        ctl = False
                        break
            if ctl is False:
                break
            result = index_data.xpath(xpath_rule)
            for ip in range(0, len(result), 2):
                self.dbase.append(result[ip] + ':' + result[ip + 1])
            time.sleep()


if __name__ == '__main__':
    ClassInstance = Proxiesdata()
    print(ClassInstance.analyze_page())
    input()
