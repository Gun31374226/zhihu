#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
https://www.zhihu.com/topic/19552832/top-answers
主要是查询在知乎topicid(python=19667317)话题，得到话题的描述和关注人数；以及得到该topicid的热门问题列表

https://www.zhihu.com/question/20702054
进一步得到每个问题的回答数，关注人数：30357，该问题被浏览次数：2807616
更进一步每个回答的 作者，作者签名，点赞数
'''
import os
import time
import random
import itertools



import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import lxml
import logging


import zhihu_config as cfg
from  tools import mysql as db
from tools import Proxy
from tools import Tools



from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


            
    

class Question(object):
    '''
    CREATE TABLE question (
        questionid   CHAR (10)     PRIMARY KEY,
        questionDesc VARCHAR (500),
        topicid      CHAR (8),
        answers      INTEGER,
        likers       INTEGER,
        readers      INTEGER
    );
    '''
    def __init__(self, atopic_id, aheaders, aproxy=None):
        
        self.topic_id = atopic_id
        self._url = '%s%d/top-answers' % (cfg.topic_url, self.topic_id)
        
        self.proxy = aproxy
        self.headers = aheaders
                
        self.topic_info = ()
        self.question_list = [] 
        
    def go(self):

        #self.clean_env()
        for pgn in range(1, cfg.maxpages_per_topic + 1):
            print('     starting page: %d, at: %s' % (pgn, Tools.get_now_datetime()))
            #print('     topic(%s)start page %d .at %s..' % (self.topic_id, apage, Tools.get_now_datetime()))
            self.get_by_page(pgn)
        


    def get_by_page(self, apage):
        params = {'page': apage}
        try:
            rs = requests.get(self._url,proxies=self.proxy, headers = self.headers, params =params, verify=False)
        except BaseException as e:
            print('         exception happend %s' % (e))
            time.sleep(60)
            rs = requests.get(self._url,proxies=self.proxy, headers = self.headers, params =params, verify=False)
            
        if rs.status_code != 200:
            raise Exception('call server Exception: %d' % rs.status_code)
            
            
        def get_topic_followers(asoup):   #210319 人关注了该话题
            '''获取话题关注人数.
            # 无人关注时 找不到对应block，直接返回0 （感谢知乎用户 段晓晨 提出此问题）
            :return: 关注人数
            :rtype: int
            '''
            follower_num_block = asoup.find(
                'div', class_='zm-topic-side-followers-info')
        
            if follower_num_block.strong is None:
                return 0
            return int(follower_num_block.strong.text)
        
        def get_topic_desc(asoup): 
            '''获取话题描述.
            #描述:Python 是一种面向对象的解释型计算机程序设计语言
            :return: 话题描述
            :rtype: str
            '''
            return asoup.find('div', class_='zm-editable-content').text
            
        soup = BeautifulSoup(rs.text, 'lxml')
        if apage == 1:
            topic_desc = get_topic_desc(soup)
            topic_followers = get_topic_followers(soup)
            
            self.topic_info = (topic_desc, topic_followers, Tools.get_now_datetime(), 'Y', self.topic_id) # topicDesc,followers,
            
            print('     (followers: %d) %s'% (topic_followers, topic_desc))
            
            
        
        for q in soup.find_all(class_='feed-item feed-item-hook folding'):
            #q_info = q.find(class_='question_link')                            
            #q_link = q_info.get('href')
            
            q_id = int(os.path.split(q.a['href'])[1]) if os.path.split(q.a['href'])[1].isdigit() else 0  #/question/20702054
            q_desc = q.a.get_text().strip()
            
            self.question_list.append((q_id, q_desc, self.topic_id))  #问题描述  --回答数，关注人数，该问题被浏览次数。
            
            print('            (%d)%s' % (q_id, q_desc))
        return 0
        
    def result2db(self):
        '''
        CREATE TABLE question (
        questionid   CHAR (10)     PRIMARY KEY,
        questionDesc VARCHAR (500),
        topicid      CHAR (8),
        answers      INTEGER,
        likers       INTEGER,
        readers      INTEGER,
        isSpidered   CHAR (1) );
        '''
        
        db.execute_str_list('insert or ignore into question (questionid, questionDesc, topicid) values (%s, %s, %s)', self.question_list)
        db.execute_str_list('update topic set topicDesc=%s, followers=%s, spiderDate=%s, isSpidered=%s where topicid=%s', [self.topic_info])
        

   
if __name__ == '__main__':
    header = cfg.zhihu_headers_ch
    qst = Question(19552832, header)
    qst.go()
    qst.result2db()