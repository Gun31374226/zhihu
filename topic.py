#!/usr/bin/python3
#-*- coding: UTF-8 -*-


import requests
import json
import random 
import sys
import time


import zhihu_config as cfg
from  tools import mysql as db
from tools import Tools

from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)




#根话题  19550374
#https://www.zhihu.com/topic/19776749/organize/entire
#加载更多
#https://www.zhihu.com/topic/19561087/organize/entire?child=19606598&parent=19561087
#https://www.zhihu.com/topic/19776751/organize/entire

''' sample of getting result
[['topic', 'CBD建筑', '20040114'], []]
[['topic', '微商户', '19961838'], []]
[['topic', '血缘关系', '19607306'], []]
[['topic', '晚育', '20034935'], []]
[['topic', '铿锵三人行', '20010885'], []]
[['topic', '颜色空间', '19794669'], []]
[['topic', 'Stephen Moyer', '20082368'], []]
[['topic', '个人定制', '20002612'], []]
[['topic', '策划营销', '19814104'], []]
[['topic', '海边', '19648422'], []]
[['load', '加载更多', '19648422', '19776751'], []]
'''

 #TODO (Gun): how about the topic has sub topic now, but No in previous version. vise viza
 #TODO (Gun): multi threading
 #TODO (Gun): change request header to avoid spam

class Topic(object):

    def __init__(self, atopic_id, aheaders, aproxy=None):
        
        self.topic_id = atopic_id
        
        self.id_pid_list = []
        self.sub_topic_list = []
        
        self._has_more = True
        self._brother_id = ''

    def go(self):
        while self._has_more:
            print('     starting page: %d, at: %s' % (pgn, Tools.get_now_datetime()))
            self._has_more = get_sub_topics()
        

        
    def get_sub_topics(self):
    
        if abrother_id == '':
            tmp_url = '%s%d/organize/entire' % (cfg.topic_url, self.topic_id)   #https://www.zhihu.com/topic/19776749/organize/entire
        else:
            #tmp_url = cfg.topic_url + _pid + '/organize/entire?child=' + _id + '&parent=' + _pid
            tmp_url = '%s%d/organize/entire?child=%d&parent=%d' % (cfg.topic_url, self.topic_id, self._brother_id, self.topic_id)  
        
        try:
            rs = requests.post(tmp_url, headers = cfg.zhihu_headers_qq, data = cfg.post_data, verify=False)
        except BaseException as e:
            print('         exception happend %s' % (e))
            time.sleep(60)
            rs = requests.post(tmp_url, headers = cfg.zhihu_headers_qq, data = cfg.post_data, verify=False)
            
        if rs.status_code != 200:
            raise Exception('call server Exception: %d' % rs.status_code)
        
        jdata = json.loads(rs.text)
        tpc = jdata['msg']
         
        for sub in tpc[1]:
            if sub[0][1] == '加载更多':
                tmp_has_more = True
                self._brother_id = sub[0][2]
                break
            else:
                tmp_has_more = False
                
            if len(sub[1]) > 0:
                _has_sub = 'Y'
            else:
                _has_sub = 'N'
            tmp_id = int(sub[0][2]) if sub[0][2].isdigit() else 0
            self.sub_topic_list.append((tmp_id,sub[0][1], _has_sub,'N', Tools.get_now_datetime(),'N'))  #topicid, toipicname,hasSub, isGetSub,updateDate,isSpidered            
            self.id_pid_list.append((tmp_id, self.topic_id))
        return tmp_has_more


    def result2db(self):
        #result sub topics into table topic  如果之前没有子话题，现在有，反之亦然，咋办？
        tmp_sql = 'insert or ignore into topic (topicid, topicname, hasSub, isGetSub, updateDate, isSpidered) values (%s,%s,%s,%s,%s,%s)'
        
        self.db.execute_str_list(tmp_sql, sub_topic_list)
        
        #into table topicPid            
        tmp_sql = 'replace into topicPid (topicid, topicpid) values (%s,%s)'
        self.db.execute_str_list(tmpstr, self.id_pid_list)  
        
        #update isGetSub='Y' to  table topic       
        db.execute_str_list('update topic set isGetSub="Y" where topicid=%s', [(self.topic_id,)])

if __name__ == '__main__':
    topic = Topic()
    topic.go()
    topic.result2db()


