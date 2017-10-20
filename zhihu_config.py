#!/usr/bin/python3
#-*- coding: UTF-8 -*-
# 临时数据文件名


sqlite_db_name = r'D:\99-py\zhihu\zhihu.db'
mysql_db_config ={'host':'127.0.0.1', 'user':'root', 'password':'admin123', 'port':3306, 'database':'zhihu', 'charset':'utf8'}

'''
#root topic --> https://www.zhihu.com/topic/19776749/organize/entire
#if has sub topic --> https://www.zhihu.com/topic/19561087/organize/entire?child=19606598&parent=19561087

seed_topic = {'19776749':'根话题'}19930358
'''
        

topic_url = 'https://www.zhihu.com/topic/'    #top_answer_url = 'https://www.zhihu.com/topic/19552832/top-answers'
maxpages_per_topic = 50

question_url_a = r'https://www.zhihu.com/api/v4/questions/'
question_url_b = r'/answers?include=data%5B*%5D.comment_count%2Cvoteup_count%2Ccreated_time%2Cupdated_time%2Cquestion%2Cexcerpt%3Bdata%5B*%5D.author.follower_count%5B%3F(type%3Dbest_answerer)%5D.topics&sort_by=default&limit=20'
question_url_c = r'&offset='

maxanswers_per_question = 100


sleeptime = 1  #sleep, if too hurry, will be spamed

timeout = 15

# 话题页面header
pageheaders = {}

# 子话题数据POST接口参数 #QQ browse for ribgun
post_data = {
    '_xsrf':'a41c5054-5ffd-4c1e-9ac1-dd0122fa98f6'
}
# 自话题数据接口Header
subtopic_headers = {
}
#QQ browse for ribgun
zhihu_headers_qq = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'authorization':'Bearer 2|1:0|10:1508026367|4:z_c0|80:MS4xcVBzbUJRQUFBQUFtQUFBQVlBSlZUZjgwQ2xydE95b00zTUVpVEVGNm5BVTJUeTJENnI4N193PT0=|491ff72a6045391827612c24f4387202243d6d51a1760c7674d77ab662c01ccb',
    'Cookie':'aliyungf_tc=AQAAAIOPTG9E4wAAqcsWdOdUMDiKzjtX; q_c1=1e227cadd6c242f8a6c9423782373371|1508026326000|1508026326000; _zap=bb865e3b-2de3-45ec-a2c0-be40bb0ba1df; capsion_ticket="2|1:0|10:1508026361|14:capsion_ticket|44:ZDUwNGU1NjMwMDQzNGZhNGEwMDNlMThjMDQ4Mjk1Yzk=|26690f70258a640750965e673a495ff8b75b2d86991392dfdba019867a6e9735"; z_c0="2|1:0|10:1508026367|4:z_c0|80:MS4xcVBzbUJRQUFBQUFtQUFBQVlBSlZUZjgwQ2xydE95b00zTUVpVEVGNm5BVTJUeTJENnI4N193PT0=|491ff72a6045391827612c24f4387202243d6d51a1760c7674d77ab662c01ccb"; _xsrf=c362160d-dfa8-4898-9c38-156baf13897f',
    
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com/explore',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
}

#chrome for gun.jiang@qq.com
zhihu_headers_ch = {
    'accept':'application/json, text/plain, */*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'en-US,en;q=0.8',
    'authorization':'Bearer 2|1:0|10:1508025955|4:z_c0|80:MS4xdmtZQ0FBQUFBQUFtQUFBQVlBSlZUV016Q2xxalJaY3pDODhYWEY3UDZHUFlidHE5SVBxVnlRPT0=|b68d24c0921d344244a237a42d331be2183858d22eeaaa8e59bb7dc0425892a3',
    'Connection':'keep-alive',
    'Cookie':'aliyungf_tc=AQAAAN8VqmZIBwgAqcsWdCXE2y4cP1xY; _zap=addb84b0-1345-479a-993a-197ee10d68ba; q_c1=64b239716ed047c4a677afd11ccd7b07|1508025938000|1508025938000; capsion_ticket="2|1:0|10:1508025944|14:capsion_ticket|44:OTJjZTllZDFjNTEzNGYzYTg5ZDJlMzVmMmZmNzhhYjk=|e9cf09f68bbd838eff9ee34c2329509cdcd42f437ed6b2985ddf2f3fcfcac2c5"; z_c0="2|1:0|10:1508025955|4:z_c0|80:MS4xdmtZQ0FBQUFBQUFtQUFBQVlBSlZUV016Q2xxalJaY3pDODhYWEY3UDZHUFlidHE5SVBxVnlRPT0=|b68d24c0921d344244a237a42d331be2183858d22eeaaa8e59bb7dc0425892a3"; anc_cap_id=9b70baebd37f4364959a27469df48894; _xsrf=a41c5054-5ffd-4c1e-9ac1-dd0122fa98f6',
    'Host':'www.zhihu.com',
    'Referer':'https://www.zhihu.com/',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
    'X-UDID':'ADBCUaLpaQyPTiXcprQgCZfI5X-zeLM17sI='
}


zhihu_headers_chxx = {
    'Host': 'messaging.zhihu.com',
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'Origin': 'https://www.zhihu.com',
    'x-udid': 'ADBCUaLpaQyPTiXcprQgCZfI5X-zeLM17sI=',
    'x-xsrftoken': 'efe96169242d599064b3d0673a4c3851',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://www.zhihu.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cookie': 'q_c1=fa9e9d9bb2c846f0b50bf3bab9387d53|1504925164000|1504925164000; _zap=0927ebe9-423e-41c7-9e61-ca0dfafba918; d_c0="ADBCUaLpaQyPTiXcprQgCZfI5X-zeLM17sI=|1506046106"; r_cap_id="MGQ3ZDEwNzUxM2Q2NGI4OWE3NDg3YzI2ZjU1ZDBhZGQ=|1506508330|da2201a29f7acfa1c9163787544ab62372941249"; cap_id="YzhkMjA0MGNiZTY0NDBhMGJjZjdlMmIyMDYwMWMyNDM=|1506508330|93a19cbd5d8c9ab6d2fb9173a1f8f22f1e5f30c3"; __utma=51854390.1542726437.1506046094.1506046094.1506508332.2; __utmc=51854390; __utmz=51854390.1506046094.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.000--|3=entry_date=20170909=1; z_c0=Mi4xcVBzbUJRQUFBQUFBTUVKUm91bHBEQmNBQUFCaEFsVk5QZ3Z6V1FEcEZWM09VeHl5TkJxbmpzZXp3S2NLdDBKUWt3|1506508350|2626963ffac2f9cc9588925428eef0b97feb79bc; _xsrf=efe96169242d599064b3d0673a4c3851'
}

#for create proxy from www.xici.com
xc_headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWNmMzE4ODcxMGRmYTUxNDJlOTVhMjE3MTMzMDM4ZjY2BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMVYvdU90bEszNk4vd21tNkpwLzUwR3JxeWNxeTg3cTkxcjFLQ3ZCOEhiQmc9BjsARg%3D%3D--476ac43e699a547f5ea993c2b55060a27761c049; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1506825261; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1506827583',
    'Host':'www.xicidaili.com',
    'If-None-Match':'W/"aeb774de7bca33dc2f3cc6af53c479c9"',
    'Referer':'http://www.xicidaili.com/wn/',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3427.400 QQBrowser/9.6.12201.400'
}



