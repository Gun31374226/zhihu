#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
import time

import zhihu_config as cfg
import requests
import sqlite3
from bs4 import BeautifulSoup
import mysql.connector

#authorId,url_token,name,type,gender,headline,followers  


class Proxy(object):

    def __init__(self):
        self._url = r'http://www.xicidaili.com/wn/'
        #self.db = Sqlite_Operation(cfg.db_name)
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
        test_url = r'http://www.baidu.com'
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

        
class Sqlite(object):
    
    def __init__(self, adb_name):
        self.db_name = adb_name
        self.conn = sqlite3.connect(self.db_name)
      
    def close(self):

        self.conn.close()
        
    def query(self, asql):
        
        cursor = self.conn.cursor()
        cursor.execute(asql)
        
        _tmp_list = cursor.fetchall()
        cursor.close()
        return _tmp_list
    '''
    def query_one(self, asql):
    
        cursor = self.conn.cursor()
        cursor.execute(asql)
        _result_list = cursor.fetchall()
        cursor.close()
        _tmp_list = []
        for x in _result_list:
            _tmp_list.append(x[0])
            
        return _tmp_list
    '''
        
    def execute_strs(self, asql_list):
    
        cursor = self.conn.cursor()
        
        for sql_str in asql_list:
            cursor.execute(sql_str)
        rows = cursor.rowcount
        cursor.close()
        self.conn.commit()
        
        return rows


    def execute_str_list(self, asql_str, avalue_list):
        cursor = self.conn.cursor()
        
        for v_tuple in avalue_list:
            #print('datatype is:',type(v_tuple))
            cursor.execute(asql_str, v_tuple)
            
        rows = cursor.rowcount
        cursor.close()
        self.conn.commit()
        return rows
        
        
class Mysql(object):
    
    def __init__(self, adb_config):    
        self.db_config = adb_config
        self.conn = mysql.connector.connect(**self.db_config)
        
    def close(self):

        self.conn.close()
        
    def query(self, asql):
        
        cursor = self.conn.cursor()
        cursor.execute(asql)
        
        _tmp_list = cursor.fetchall()
        cursor.close()
        return _tmp_list
 
        
    def execute_strs(self, asql_list):
    
        cursor = self.conn.cursor()
        
        for sql_str in asql_list:
            cursor.execute(sql_str)
        rows = cursor.rowcount
        cursor.close()
        self.conn.commit()
        
        return rows


    def execute_str_list(self, asql_str, avalue_list):
        cursor = self.conn.cursor()
        
        for v_tuple in avalue_list:
            #print('datatype is:',type(v_tuple))
            cursor.execute(asql_str, v_tuple)
            
        rows = cursor.rowcount
        cursor.close()
        self.conn.commit()
        return rows

class Tools(object):
    @classmethod
    def get_now_date(self):
        return time.strftime('%Y-%m-%d',time.localtime(time.time()))
    
    
    @classmethod
    def get_now_datetime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        

    @classmethod
    def get_date_bystamp(self, astamp):
        return time.strftime('%Y-%m-%d',time.localtime(astamp))
        
        
        
global sqlite
sqlite = Sqlite(cfg.sqlite_db_name)
global mysql
mysql = Mysql(cfg.mysql_db_config)

def x_question():
    tmp_list = sqlite.query('select distinct topicid  from question')
    for x in tmp_list:
        sql = 'select questionid,questionDesc,created,topicid,answers,monitors,readers,spiderDate,isSpidered from question where topicid=%s' % x
        
        print(sql)
        #break
        tmp = sqlite.query(sql)
        mysql.execute_str_list('insert ignore into question (questionid,questionDesc,created,topicid,answers,monitors,readers,spiderDate,isSpidered) values(%s,%s,%s,%s,%s,%s,%s,%s,%s) ', tmp)
        
def x_answer():
    tmp_list = sqlite.query('select distinct answertime  from answer')
    for x in tmp_list:
        sql = 'select answerid,authorID,questionid,voteups,comments,answertime,excerpt from answer where answertime=%s' % x
        print(sql)
        tmp = sqlite.query(sql)
        mysql.execute_str_list('insert ignore into answer (answerid,authorID,questionid,voteups,comments,answertime,excerpt) values(%s,%s,%s,%s,%s,%s,%s) ', tmp)

def x_author():
    tmp_list = sqlite.query('select distinct(substr(rowid, 1,3)) as num from author')
    for x in tmp_list:
        sql = 'select authorId,url_token,name,type,gender,headline,followers from author where substr(rowid, 1,3)="%s"' % x
        print(sql)
        tmp = sqlite.query(sql)
        mysql.execute_str_list('insert ignore into author (authorId,url_token,name,type,gender,headline,followers) values(%s,%s,%s,%s,%s,%s,%s) ', tmp)
        
if __name__ =='__main__':
    #x_answer()
    x_author()
    x_question()