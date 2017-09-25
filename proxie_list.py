#!/usr/bin/python3
# _*_ coding:utf-8 _*_
__author__ = 'anyco'

import requests
import threading
import pickle
from lxml import etree
from proxies_init import Proxiesinit
import time


class Proxiesdata:
    def __init__(self):
        # self.lock = threading.Lock()
        # self.Instance = Proxiesinit(r'D:\webdrive\phantomjs\bin\phantomjs.exe')       # 实例化Proxiesinit类
        self.Instance = Proxiesinit(r'/usr/local/bin/phantomjs')
        self.header = self.Instance.get_header()    # 将Proxiesinit()的get_header方法赋值给header
        self.page_num, self.index = self.Instance.page_count()   # 将page_count方法的值赋值给page_num和index
        self.proxy_page = 'http://www.kuaidaili.com/free/inha/%s/'  # 定义proxy_page的网页url
        # self.req = requests.session()
        self.dbase = list() # 所有代理ip的存储列表
        self.failed = set()    # 请求失败的网页列表

    def proxy_url(self):
        self.pagenum = [i for i in range(1, self.page_num+1)]   # 将网页地址页码生成列表
        self.allurl = [self.pagenum[i:i+100] for i in range(0, self.page_num+1, 100)] # 每100个页码再次组成新列表
        # print(self.allurl)
        return self.allurl

    def get_ip(self, pagelist):
        self.pagelist = pagelist    # 提供页码分组组成的列表用于循环请求页面
        self.req = requests.session()   # 生成requests的session
        xpath_rule = '//*[@id="list"]/table/tbody/tr/td[1]/text() | //*[@id="list"]/table/tbody/tr/td[2]/text()'
        # 解析页面代理ip的ip地址和端口的xpath
        for num in self.pagelist:   # 对每100页的页码进行循环请求
            print('Start analyze page %d ...' %num)
            if num == 1:
                pagedate = etree.HTML(self.index.text)  # 第一页直接解析获取cookie时请求的页面
            else:
                url = self.proxy_page %num  # 非第一页则生成网页url
                try:
                    page = self.req.get(url, headers=self.header, timeout=10)
                    count = 1
                    while page.status_code != 200:  # 对url未请求成功则重新获取header再次请求
                        print('Page %d %d times request Failed! Re request!' %(num, count))
                        self.header = self.Instance.get_header()
                        page = self.req.get(url, headers=self.header, timeout=30)
                        count += 1
                        if count > 5:  # 请求失败超过10次则放弃当前页面请求并将页码添加到failed列表
                            self.failed.add(num)
                            break
                    if count > 5:
                        print('Page %d can not access!Continue request next page!' %num)
                        continue
                    else:
                        pagedate = etree.HTML(page.text)    # 解析请求到的页面
                    result = pagedate.xpath(xpath_rule)
                    for ip in range(0, len(result), 2):
                        self.dbase.append(result[ip]+':'+result[ip+1])  # 对解析到的代理ip格式化添加到dbase列表
                # sleep(3)
                except:
                    print('Network Error!Please check it!')
                    self.failed.add(num)

    def mutil_thread(self):
        urladdress = self.proxy_url()   # 实例化分组页码函数
        thread_num = []
        tnum = 1
        for i in urladdress:    # 创建多线程请求
            try:
                print('Thread %d set up!' %tnum)
                # t = threading.Thread(target=self.get_ip, args=(i,))
                thread_num.append(threading.Thread(target=self.get_ip, args=(i,)))
                # t.start()
                tnum += 1
            except:
                print('error')
        for t in thread_num:
            t.start()
        for thread in thread_num:   # 将多线程的所有线程阻塞，等待所有线程执行完毕。
            print('Thread join time is %s' %(time.strftime('%H:%M:%S',time.localtime())))
            thread.join()
            # print('Thread finished!')
        endtime = time.time()
        usetime = time.localtime(endtime - starttime)
        print('All Thread finished!Execution time %s' %(time.strftime('%M:%S',usetime)))
        with open('proxies_ip.db','wb') as f:
            pickle.dump(self.dbase,f)
            pickle.dump(self.failed,f)
        # return self.dbase

if __name__ == '__main__':
    starttime = time.time()
    print('Process started at time {}'.format(time.strftime('%H:%M:%S',time.localtime(starttime))))
    ClassInstance = Proxiesdata()
    print(ClassInstance.page_num)
    # print(ClassInstance.analyze_page())
    # ClassInstance.proxy_url()
    ClassInstance.mutil_thread()
    with open('proxies_ip.db','rb') as f:
        succed = pickle.load(f)
        print(succed)
        fail = pickle.load(f)
        print(fail)
    # print(ClassInstance.failed)
    # print(ClassInstance.dbase)