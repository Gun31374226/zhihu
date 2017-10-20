#!/usr/bin/python3
# -*-coding: utf-8-*-
'''
'''

import json
import random
import time


import zhihu_config as cfg
from tools import mysql as db
from tools import Proxy
from tools import Tools
from answer import Answer
from question import Question

class Zhihu(object):     

    def __init__(self):
        pass
     
    def start_topic(self):
        tmp_sql = 'select topicid from topic where hasSub="Y" and isGetSub="N" limit 1'
        
        proxy = None
        header = cfg.zhihu_headers_qq
        while len(db.query_one(tmp_sql)) > 0:
            topic_id = db.query_one(tmp_sql)[0]
            
            #proxy = Proxy().get_proxy()
            #print('using proxy: %s' % (proxy))
        
            print('starting to get subtopics %s  at (%s)' % (topic_id, Tools.get_now_datetime()))
            
            try:
                tpc = Topic(topicid, header)
                tpc.go()
                tpc.result2db()
            except BaseException as e:
                print(e)
                db.execute_str_list('update topic set isGetSub="X" where topicid=?', [(topic_id,)])
                time.sleep(60)
                
                continue
            
            n = n + 1
        print('Great, topic, we made it Done!!!')
        
    def start_question(self):
        tmp_sql = 'select topicid from topic where isSpidered="N" limit 1'
        
        proxy = None
        header = cfg.zhihu_headers_qq
        while len(db.query_one(tmp_sql)) > 0:
            topic_id = db.query_one(tmp_sql)[0]
            
            #proxy = Proxy().get_proxy()
            #print('using proxy: %s' % (proxy))
        
            print('starting to spider %s  at (%s)' % (topic_id, Tools.get_now_datetime()))
            
            try:
                qst = Question(topic_id, header)
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
        tmp_sql = 'select questionid from question where isSpidered="N" and questionid>35000000 limit 1'
        n = 0
        isqq_header = True
        proxy = None
        
        while len(db.query(tmp_sql)) > 0:
            quest_id = db.query(tmp_sql)[0][0]
            
            if str(n)[-1]  in ['0', '5']:
                #proxy = Proxy().get_proxy()
                #print('using proxy: %s' % (proxy))
                if isqq_header :
                    header = cfg.zhihu_headers_qq
                    isqq_header = False
                else:
                    header = cfg.zhihu_headers_qq
                    isqq_header = True
        
            
            print('starting to spider the question: %s  at (%s)' % (quest_id, Tools.get_now_datetime()))
            try:
                answer = Answer(quest_id, header)
                answer.go()
                answer.result2db()
                #time.sleep(5)
            except BaseException as e:
                print(e)
                db.execute_str_list('update question set isSpidered="X" where questionId=%s', [(quest_id,)])
                time.sleep(60)
                
                continue
            
            n = n + 1
        print('Great, answer, we made it Done!!!')


if __name__ == '__main__':
    zh = Zhihu()
    #zh.start_topic()
    #zh.start_question()
    zh.start_answer()