#!/usr/bin/python3
# _*_ coding:utf-8 _*_
__author__ = 'anyco'

import requests
import time
import os
from lxml import etree
from proxies_init import Proxiesinit


class Proxiesdata:
    def __init__(self):
        self.Instance = Proxiesinit()       # 实例化Proxiesinit类
        self.header = self.Instance.get_header()    # 将Proxiesinit()的get_header方法赋值给header
        self.page_num, self.index = self.Instance.page_count()   # 将page_count方法的值赋值给page_num和index
        self.proxy_page = 'http://www.kuaidaili.com/free/inha/%s/'  # 定义proxy_page的网页url

    def proxy_url(self):
        self.pagenum = [i for i in range(1,self.page_num+1)]
        s = int(self.page_num/100) + 1
        self.allurl = list()
        for i in range(s):
            self.allurl.append(self.pagenum[0:100])
            del self.pagenum[0:100]
        print(self.allurl)

    def analyze_page(self):     # 代理页面解析方法
        os.system('cls')        # 清屏
        print("Analyze webpage's data,please wait...")
        self.dbase = list()
        req = requests.session()
        for num in range(1, self.page_num):
            print(num)
            ctl = True
            xpath_rule = '//*[@id="list"]/table/tbody/tr/td[1]/text() | //*[@id="list"]/table/tbody/tr/td[2]/text()'
            if num == 1:
                print(self.index.text)
                page_data = etree.HTML(self.index.text)
            else:
                url = self.proxy_page %num
                page = req.get(url, headers=self.header, timeout=5)
                page_data = etree.HTML(page.text)
                count = 1
                while page.status_code != 200:
                    print('Request Failed! RESTART...')
                    self.header = self.Instance.get_header()
                    page_data = etree.HTML(req.get(url, headers=self.header, timeout=5).text)
                    count += 1
                    if count > 10:
                        print('Content page number is %d,can not request correct page source!')
                        ctl = False
                        break
            if ctl is False:
                break
            result = page_data.xpath(xpath_rule)
            for ip in range(0, len(result), 2):
                self.dbase.append(result[ip] + ':' + result[ip + 1])
            time.sleep(3)
        return self.dbase

if __name__ == '__main__':
    ClassInstance = Proxiesdata()
    print(ClassInstance.page_num)
    # print(ClassInstance.analyze_page())
    ClassInstance.proxy_url()
