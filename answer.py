#!/usr/bin/python3
# -*-coding: utf-8 -*-
'''
CREATE TABLE question (
    questionid   CHAR (10)     PRIMARY KEY,
    questionDesc VARCHAR (500),
    *created      DATE,
    topicid      CHAR (8),
    *answers      INTEGER       DEFAULT (0),
    --*monitors     INTEGER       DEFAULT (0),
    --*readers      INTEGER       DEFAULT (0),
    *spiderDate   DATE,
    *isSpidered   CHAR (1)      DEFAULT N
);


CREATE TABLE answer (
    answerid   CHAR (10) PRIMARY KEY,
    authorID   VARCHAR,
    questionid CHAR (10),
    voteups    INTEGER,
    comments   INTEGER,
    answertime DATE,
    excerpt    VARCHAR
);
        CREATE TABLE author (
        authorId          PRIMARY KEY,
        url_token VARCHAR,
        name      VARCHAR,
        type      VARCHAR,
        gender    INTEGER,
        headline  VARCHAR,
        followers  INTEGER
        );

'''

import json
import random
import requests
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning

import zhihu_config as cfg
from  tools import mysql as db
from tools import Proxy
from tools import Tools

from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Answer(object):

    def __init__(self, aquest_id, aheaders, aproxy=None):
        
        self.quest_id = aquest_id
        
        self.proxy = aproxy
        self.headers = aheaders
        
        self.quest_info = tuple()
        self.answer_list = []
        self.author_list = []
        
        self.question_answers = 1
        
    def go(self):
    
        tmp_offset = 0
        while min(cfg.maxanswers_per_question, self.question_answers) > tmp_offset:
        
            print('     starting offset: %d, at: %s' % (tmp_offset, Tools.get_now_datetime()))
            
            self.get_by_offset(tmp_offset)
            tmp_offset = tmp_offset + 20
            time.sleep(1)

        

        
    def get_by_offset(self, aoffset):
        
        tmp_url = '%s%s%s%s%d' % (cfg.question_url_a, self.quest_id, cfg.question_url_b, cfg.question_url_c, aoffset)
        try:
            rs = requests.get(tmp_url, proxies=self.proxy, headers = self.headers, verify=False)
        except BaseException as e:
            print('         exception happend %s' % (e))
            time.sleep(60)
            rs = requests.get(tmp_url, proxies=self.proxy, headers = self.headers, verify=False)
            
        if rs.status_code != 200:
            raise Exception('call server Exception: %d' % rs.status_code)
            
        jdict = json.loads(rs.text)        
        #print(jdict)
        
        if aoffset == 0:
            self.question_answers = int(jdict['paging']['totals']) 
        #self._is_end = jdict['paging']['is_end']
        
        for ans in jdict['data']:            
            '''
            'question': {
                'question_type': 'normal',
                'title': '有哪些是读书学不来，却很重要的素质？',
                'url': 'http: //www.zhihu.com/api/v4/questions/28626263',
                'created': 1425878416,
                'type': 'question',
                'id': 28626263,
                'updated_time': 1504246235
            },
            '''
            if aoffset == 0:
                self.quest_info = ( Tools.get_date_bystamp(ans['question']['created']),self.question_answers, 
                                    Tools.get_now_date(), 'Y', self.quest_id)

            '''
                    'author': {
                    'avatar_url_template': 'https: //pic3.zhimg.com/50/3b8679a01c5bd61f0e28974e98d6ca6e_hd.jpg',
                    'badge': [],
                    'name': '肥肥猫',
                    'headline': '公众号搜：肥肥猫的小酒馆',
                    'gender': 1,
                    'user_type': 'people',
                    'is_advertiser': False,
                    'avatar_url': 'https: //pic3.zhimg.com/50/3b8679a01c5bd61f0e28974e98d6ca6e_hd.jpg',
                    'is_org': False,
                    'type': 'people',
                    'url': 'http: //www.zhihu.com/api/v4/people/342d47c5da88fb45217f0685d261ce64',
                    'follower_count': 449095,
                    'url_token': 'feifeimao',
                    'id': '342d47c5da88fb45217f0685d261ce64'
                    },
                    
                    CREATE TABLE author (
                    authorId          PRIMARY KEY,
                    url_token VARCHAR,
                    name      VARCHAR,
                    type      VARCHAR,
                    gender    INTEGER,
                    headline  VARCHAR,
                    follower  INTEGER
                    );
            '''

            author_id = ans['author']['id']
            url_token = ans['author']['url_token']
            name = ans['author']['name']
            type = ans['author']['type']
            gender = ans['author']['gender']
            headline = ans['author']['headline']
            followers = int(ans['author']['follower_count'])
            self.author_list.append((author_id, url_token, name, type, gender, headline, followers))

            '''
            'excerpt': '（本文所有文字皆为原创，<b>除注明引用外未参考任何文献</b>，谢绝转载，）书上找不到，也很少有人讨论的个人素质，我认为有以下三种：１．人际交往中的期望值管理能力２．阈值自控意识３．应对主观时空扭曲的能力１.先说第一个，期望值管理能力。影视剧中…',
            'updated_time': 1464680986,
            'thumbnail': 'https: //pic2.zhimg.com/df2fde24bbdddfb2f8e7e88628175719_200x112.jpg',
            'comment_count': 5262,
            'extras': '',
            'created_time': 1426330123,
            'is_copyable': False,
            'type': 'answer',
            'id': 41992632,
            'voteup_count': 169123
            '''
            
            ans_id = int(ans['id'])
            ans_excerpt = ans['excerpt']
            ans_time = Tools.get_date_bystamp(ans['created_time'])
            ans_voteups = int(ans['voteup_count'])
            ans_comments = int(ans['comment_count'])
            self.answer_list.append((ans_id,self.quest_id, author_id, ans_excerpt, ans_time, ans_voteups, ans_comments))
        return 0
        
        
    def result2db(self):
        #self.answer_list.append((ans_id,self.quest_id, author_id, ans_excerpt, ans_time, ans_voteups, ans_comments))
        db.execute_str_list('insert ignore into answer (answerid, questionid, authorID, excerpt, answertime, voteups, comments) '
                            'values (%s,%s,%s,%s,%s,%s,%s)', self.answer_list)
                            
        # self.author_list.append((author_id, url_token, name, type, gender, headline, followers))
        db.execute_str_list('insert ignore into author (authorId, url_token, name, type, gender, headline, followers)'
                            'values (%s,%s,%s,%s,%s,%s,%s)', self.author_list)
        
        db.execute_str_list('update question set created=%s, answers=%s, spiderDate=%s, isSpidered=%s where questionid=%s', [self.quest_info])
        
if __name__ == '__main__':
    header = cfg.zhihu_headers_qq
    answer = Answer(28626263, header)
    answer.go()
    answer.result2db()