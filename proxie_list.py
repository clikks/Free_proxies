#!/usr/bin/python3
# _*_ coding:utf-8 _*_
__author__ = 'anyco'

import requests
import threading
from lxml import etree
from proxies_init import Proxiesinit
from time import sleep


class Proxiesdata:
    def __init__(self):
        # self.lock = threading.Lock()
        self.Instance = Proxiesinit(r'D:\webdrive\phantomjs\bin\phantomjs.exe')       # 实例化Proxiesinit类
        self.header = self.Instance.get_header()    # 将Proxiesinit()的get_header方法赋值给header
        self.page_num, self.index = self.Instance.page_count()   # 将page_count方法的值赋值给page_num和index
        self.proxy_page = 'http://www.kuaidaili.com/free/inha/%s/'  # 定义proxy_page的网页url
        # self.req = requests.session()
        self.dbase = list()
        self.failed = list()

    def proxy_url(self):
        self.pagenum = [i for i in range(1, self.page_num+1)]
        self.allurl = [self.pagenum[i:i+100] for i in range(0, self.page_num+1, 100)]
        # print(self.allurl)
        return self.allurl

    def get_ip(self, pagelist):
        self.pagelist = pagelist
        self.req = requests.session()
        xpath_rule = '//*[@id="list"]/table/tbody/tr/td[1]/text() | //*[@id="list"]/table/tbody/tr/td[2]/text()'
        # count = 0
        for num in self.pagelist:
            print('Start analyze page %d ...' %num)
            if num == 1:
                pagedate = etree.HTML(self.index.text)
            else:
                url = self.proxy_page %num
                try:
                    page = self.req.get(url, headers=self.header, timeout=10)
                    count = 1
                    while page.status_code != 200:
                        print('Page %d %d times request Failed! Re request!' %(num, count))
                        self.header = self.Instance.get_header()
                        page = self.req.get(url, headers=self.header, timeout=30)
                        count += 1
                        if count > 10:
                            self.failed.append(num)
                            break
                    if count > 10:
                        print('Page %d can not access!Continue request next page!' %num)
                        continue
                    else:
                        pagedate = etree.HTML(page.text)
                    result = pagedate.xpath(xpath_rule)
                    for ip in range(0, len(result), 2):
                        self.dbase.append(result[ip]+':'+result[ip+1])
                # sleep(3)
                except:
                    print('Network Error!Please check it!')

    def mutil_thread(self):
        urladdress = self.proxy_url()
        thread_num = []
        tnum = 1
        for i in urladdress:
            try:
                print('Thread %d set up!' %tnum)
                t = threading.Thread(target=self.get_ip, args=(i,))
                thread_num.append(t)
                t.start()
                tnum += 1
            except:
                print('error')
        for thread in thread_num:
            thread.join()
            print('Thread finished!')

        print('All Thread finished!')
        return self.dbase

if __name__ == '__main__':
    ClassInstance = Proxiesdata()
    print(ClassInstance.page_num)
    # print(ClassInstance.analyze_page())
    # ClassInstance.proxy_url()
    ClassInstance.mutil_thread()
    print(ClassInstance.failed)
    print(ClassInstance.dbase)