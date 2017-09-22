#!/usr/bin/python3
# _*_ coding:utf-8 _*_
__author__ = 'anyco'

import requests
import sys
import threading
from lxml import etree
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Proxiesinit:
    def __init__(self, phantomjsPath):
        self.phantomjsPath = phantomjsPath
        self.count = 1
        print('{}Inital program ready!{}'.format('=' * 10, '=' * 10))
        self.index = 'http://www.kuaidaili.com/free/'  # index代理主页地址
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': '',
            'Host': 'www.kuaidaili.com',
            'Referer': 'http://www.kuaidaili.com/free',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.params = dict(DesiredCapabilities.PHANTOMJS)  # PhantomJS类属性，为字典类型
        self.params["phantomjs.page.settings.userAgent"] = (self.header['User-Agent'])
        self.params["phantomjs.page.settings.loadImages"] = False  # 定义PhantomJS的UserAgent及关闭图片加载
        self.lock = threading.Lock()
    def get_header(self):
        self.lock.acquire()  # 线程锁
        driver = webdriver.PhantomJS(executable_path=self.phantomjsPath, desired_capabilities=self.params)
        # seltnium的webdriver，提供phantomJS的路径和UserAgent.
        driver.get(self.index)  # 网页请求
        sleep(3)
        if self.count == 1:
            print("Calling PhantomJS to analyze webpage...".format(sys))
        else:
            print('Get new header!')
        cookies = driver.get_cookies()  # 获得cookie列表
        items = [value['name'] + '=' + value['value'] for value in cookies]  # 格式化cookie内容
        # print(items)
        self.header['Cookie'] = '; '.join(items)  # 将格式化的cookie赋值给header内
        # print(self.header['Cookie'])
        driver.quit()
        self.count += 1
        self.lock.release()
        return self.header

    def page_count(self):
        self.required = requests.session()
        try:
            html_page = self.required.get(self.index, headers=self.header, timeout=10)  # 发起网页请求
            # print(self.header)
            # print(html_page.status_code)
            status = html_page.status_code
            while status != 200:    # 请求失败则重新获取header并再次发起请求
                print('Status code is %d.' % status)
                sleep(15)
                self.get_header()
                html_page = self.required.get(self.index, headers=self.header, timeout=30)
                status = html_page.status_code
            else:
                print('Analyze index page complete!')
                result = etree.HTML(html_page.text) # 解析首页，获取总页码数
                pagecount = result.xpath('/html/body/div[@class="body"]/div[@id="content"]/div[@class="con-body"]\
                                    /div/div[@id="list"]/div[@id="listnav"]/ul/li[last()-1]/a/text()')
                return int(pagecount[0]), html_page # 返回总页码数和首页源码

        except:
            input('Error：please check network!Press any key to exit!')
            sys.exit()


if __name__ == '__main__':
    c1 = Proxiesinit(r'D:\webdrive\phantomjs\bin\phantomjs.exe')
    print(c1.get_header())
    X = c1.page_count()
    print(X[0])
