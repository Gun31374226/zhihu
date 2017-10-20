#!/usr/bin/python3
# -*-coding: utf-8-*-
'''
'''
__author__ = 'gun.jiang@qq.com'
'testing for github 2017-10-21'

import json
import random
import sys
import time


import zhihu_config as cfg
from  tools import mysql as db
from tools import Proxy
from tools import Tools
from answer import Answer
from question import Question

class Zhihu(object):     

    def __init__(self, aheader_type):
        self._header_type = aheader_type
        if self._header_type == 'qq':
            self._header = cfg.zhihu_headers_qq
        else:
            self._header = cfg.zhihu_headers_ch
     
    def start_topic(self):
        tmp_sql = 'select topicid from topic where hasSub="Y" and isGetSub="N"  limit 1'
        
        proxy = None
        while len(db.query_one(tmp_sql)) > 0:
            topic_id = db.query_one(tmp_sql)[0]
            
            #proxy = Proxy().get_proxy()
            #print('using proxy: %s' % (proxy))
        
            print('starting to get subtopics %d  at (%s)' % (topic_id, Tools.get_now_datetime()))
            
            try:
                tpc = Topic(topicid, self._header)
                tpc.go()
                tpc.result2db()
            except BaseException as e:
                print(e)
                db.execute_str_list('update topic set isGetSub="X" where topicid=%s', [(topic_id,)])
                time.sleep(60)
                
                continue
            
            n = n + 1
        print('Great, topic, we made it Done!!!')
        
    def start_question(self):
        tmp_sql = 'select topicid from topic where isSpidered="N" limit 1'
        
        proxy = None
        while len(db.query_one(tmp_sql)) > 0:
            topic_id = db.query_one(tmp_sql)[0]
            
            #proxy = Proxy().get_proxy()
            #print('using proxy: %s' % (proxy))
        
            print('starting to spider %s  at (%s)' % (topic_id, Tools.get_now_datetime()))
            
            try:
                qst = Question(topic_id, self._header)
                qst.go()
                qst.result2db()
            except BaseException as e:
                print(e)
                db.execute_str_list('update topic set isSpidered="X" where topicid=%s', [(topic_id,)])
                time.sleep(60)
                
                continue
            
            n = n + 1
        print('Great, question, we made it Done!!!')

    def start_answer(self):
        if self._header_type == 'qq':
            tmp_sql = 'select questionid from question where isSpidered="N" and questionid>35000000 limit 1'
        else:
            tmp_sql = 'select questionid from question where isSpidered="N" and questionid<=35000000 limit 1'
        
        
        proxy = None
        
        while len(db.query(tmp_sql)) > 0:
            quest_id = db.query(tmp_sql)[0][0]
            
            #proxy = Proxy().get_proxy()
            #print('using proxy: %s' % (proxy))
            
            print('starting to spider the question: %d  at (%s)' % (quest_id, Tools.get_now_datetime()))
            try:
                answer = Answer(quest_id, self._header)
                answer.go()
                answer.result2db()
                #time.sleep(5)
            except BaseException as e:
                print(e)
                db.execute_str_list('update question set isSpidered="X" where questionId=%s', [(quest_id,)])
                time.sleep(60)
                
                continue
        print('Great, answer, we made it Done!!!')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('pls input which explorer (qq/ch)!')
        sys.exit(0)
        
    head_type = sys.argv[1]    
        
    zh = Zhihu(head_type)
    #zh.start_topic()
    #zh.start_question()
    zh.start_answer()