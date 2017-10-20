#-*- coding: UTF-8 -*-
import zhihu_config as cfg
from tools import Sqlite_Operation

import requests
import json
from bs4 import BeautifulSoup
import re
import random
import sys
import time
import sqlite3

from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Proxy(object):

    def __init__(self):
        self._url = r'http://www.xicidaili.com/wn/'
        self.db = Sqlite_Operation(cfg.db_name)
        self.ip_list = []
        self.proxy_list = []
    
    def get_ip(self):
        rs = requests.get(self._url, headers=cfg.xc_headers)
        soup = BeautifulSoup(rs.text, 'lxml')
        #print(rs.text)
        #for r in  soup.find_all(class_='country'):
        for r in  soup.find_all(class_='odd'):
            #print('ip:%s --%s' % (r.contents[3].text, r.contents[5].text))
            #print(r.next_sibling.next_sibling.text)
            self.ip_list.append((r.contents[3].text, r.contents[5].text))

    def get_proxy(self):
        self.get_ip()
        test_url = r'http://www.qq.com'
        #html=requests.get(url,headers=headers, timeout=10，proxies=proxies).text
        #print('*testing'*30)
        proxies_a = {}
        for ip in self.ip_list:
            
            proxies_a={'https': ip[0].strip()+':'+ip[1].strip()}
            rs = requests.get(test_url, timeout=10, proxies=proxies_a)
            if rs.status_code == 200:
                self.proxy_list.append(proxies_a)
        
        pnum = len(self.proxy_list)
        
        return self.proxy_list[random.randint(1,pnum)]
        
        
    
if __name__ == '__main__':
    p = Proxy()
    p.get_proxy()
    