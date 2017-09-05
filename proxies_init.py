import requests
import time
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import platform

class Proxies_init:
    def __init__(self,index=None,proxy_page=None,header={},pagination=2):
        print('{}Inital program ready!{}'.format('='*10,'='*10))
        # self.pagination = pagination
        self.index = 'http://www.kuaidaili.com/free'    #index代理主页地址
        # self.proxy_page = 'http://www.kuaidaili.com/free/inha/%s/' %(self.pagination)
        #proxy_page其余页面地址,pagination为页数
        self.header = {
                        'Accept': '*/*',
                        'Accept-Encoding' : 'gzip, deflate, sdch',
                        'Accept-Language' : 'zh-CN,zh;q=0.8',
                        'Connection' : 'keep-alive',
                        'Cookie' : '',
                        'Host' : 'www.kuaidaili.com',
                        'Referer' : 'http://www.kuaidaili.com/free',
                        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                        'X-Requested-With' : 'XMLHttpRequest',
                        }

    def get_cookie(self,phantomjsPath = None):
        params = dict(DesiredCapabilities.PHANTOMJS)
        #PhantomJS类属性，为字典类型
        params["phantomjs.page.settings.userAgent"] = (self.header['User-Agent'])
        #定义PhantomJS的UserAgent
        print('Confirm system platform type!')
        sys = platform.system()                         #获取操作系统类型
        print("Call {}'s PhantomJS path!".format(sys))
        if sys == 'Windows':
            # self.phantomjsPath = r'D:\webdrive\phantomjs\bin\phantomjs.exe'
            self.phantomjsPath = r'd:\phan.exe'
        elif sys == 'Linux':
            self.phantomjsPath = r'/usr/local/bin/phantomjs'
        else:
            self.phantomjsPath = phantomjsPath
        driver = webdriver.PhantomJS(executable_path=self.phantomjsPath,desired_capabilities=params)
        #seltnium的webdriver，提供phantomJS的路径和UserAgent.
        driver.get(self.index)     #网页请求
        time.sleep(3)                                   #等待3秒
        driver.refresh()                                #刷新页面
        cookies = driver.get_cookies()                  #获得cookie列表
        # print(cookies)
        items = []
        for value in cookies:
            # print(value)
            content = [value['name'],value['value']]    #重组获得的cookie
            items.append('='.join(content))             #格式化cookie内容
            # print(items)
        self.header['Cookie'] = '; '.join(items)        #将格式化的cookie赋值给header内
        # print(self.header['Cookie'])
        driver.close()
        return self.header

    def page_count(self):
        while True:
            req = requests.session()
            html_page = req.get(self.index, headers=self.header, timeout=5) #发起网页请求
            # print(self.header)
            # print(html_page.status_code)
            if html_page.status_code != 200:    #如果请求失败，重新获得header并发起请求
                print('Request status code is %d' % html_page.status_code)
                time.sleep(60)
                self.get_cookie()
                continue
            else:
                result = etree.HTML(html_page.text)     #解析请求到的页面
                pagecount = result.xpath('/html/body/div[@class="body"]/div[@id="content"]/div[@class="con-body"]\
                /div/div[@id="list"]/div[@id="listnav"]/ul/li[last()-1]/a/text()')
                # print(int(pagecount[0]))
                return int(pagecount[0])    #返回快代理免费代理总页数
                break

