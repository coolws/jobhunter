#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
#=============================================================================
#     FileName: main.py
#         Tips: 运行程序之前,确保redis-server已运行
#       Author: coolws
#        Email: coolws123@gmail.com
#=============================================================================
'''

from BeautifulSoup import BeautifulSoup
from conf import *
import smtplib
from email.mime.text import MIMEText
import re
import redis
import requests
import datetime
from apscheduler.scheduler import Scheduler

class Crawler:
    def __init__(self):
        self.rs = redis.Redis(host=REDIS_IP, port=REDIS_PORT)
        self.http_querys = HTTP_QUERYS
		
	#获取目标HTML中的招聘信息
    def _parseHtmlToUrls(self, **http_query):
        flag = True
        mode = 0
        host = http_query['host']
        url = http_query['url']
        href = http_query['href']
        source = http_query['source']

        r = requests.get(url, headers=headers)
        r.encoding = 'GBK'

        #print "********"
        #print r.text
        #print "********"

        soup = BeautifulSoup(r.text)
        attrs = {
        'href' : re.compile(href),
        'title' : None,
        }

        results = soup.findAll('a', attrs=attrs)
        urls = []
        for res in results:
            if res.parent.parent.get('class') != 'top':
                res['href'] = host + res['href']
                #print res['href']

                if res.string == None:
                    continue
                else:
                    res.string += u" 来源:"+ source

                    if res.parent.previousSibling.string == None:
                        mode = 1
                        time = res.parent.nextSibling.string # seu
                        #print "previousSibling"+time

                        if(time.find('-')<0):
                            times = time.split('&')[0].split(':')
                            urls.append(res)
                        else:
                            times = time.split("-")
                
                            if Crawler.isWithinDays(times[0],times[1],times[2]):
                                urls.append(res)
                            else:
                                flag = False
                    else:
                        mode = 2
                        time = res.parent.previousSibling.string #sjtu
                        match = re.compile('\s+')
                        times = match.split(time)
                        #print times 
			monthIndex = Crawler.isMonth(times[0])
                        if Crawler.isWithinDays(2015,monthIndex,times[1]):#time要修改下
                            urls.append(res)
                        else:
                            flag = False

        if mode==1 and flag == True:
            attrs = {
            'class' : "page-select",
            'target' : None,
            }
            results = soup.findAll('li', attrs=attrs)
            nextUrl = {}
            nextUrl['host'] = host
            nextUrl['url'] = host + results[0].nextSibling.next['href']
            nextUrl['href'] = href
            nextUrl['source'] = source
            #print "@@@@@@@1@@@@@@@@@@@@@"    
            self.http_querys.append(nextUrl)

        if mode==2 and flag == True:
            results = soup.findAll(text=u"上一页")
            nextUrl = {}
            nextUrl['host'] = host
            nextUrl['url'] = host + results[0].parent['href']
            nextUrl['href'] = href
            nextUrl['source'] = source
            #print "@@@@@@@2@@@@@@@@@@@@@"
            self.http_querys.append(nextUrl)


        return urls
	
	#判断是否包括标记感兴趣的信息
    @staticmethod
    def isContainElements(str, tup):
        if filter(lambda x: x in str, tup):
            return True
        return False
	
	#判断是否在感兴趣的时间内
    @staticmethod
    def isMonth(str):
        return timezone.index(str)
	
	#判断是否在感兴趣的时间内
    @staticmethod
    def isWithinDays(year,month,day):
        today = datetime.date.today()
        day = datetime.date(int(year),int(month),int(day))
        delta = today - day
        days = delta.days
        if days <= INTERVAL_DAYS :
            return True
        else:
            return False

	
	#将获取到的页面数据根据关键词处理后保存在redis中
    def _putMessageUrlIntoRedis(self, url):
        
        title = url.string
        title_remove_source = title.rsplit(u'来源')[0] 
	#print "###"+title

        if FILETER_WORDS == None:
            if KEY_WORDS == None:
                self.rs.sadd('message_urls',url)
                #print title_remove_source
            else:
                if Crawler.isContainElements(title_remove_source, KEY_WORDS):
                    self.rs.sadd('message_urls',url)
                    #print title_remove_source
        else:
            if not Crawler.isContainElements(title_remove_source, FILETER_WORDS):
                if KEY_WORDS == None:
                    self.rs.sadd('message_urls',url)
                    #print title_remove_source
                else:
                    if Crawler.isContainElements(title_remove_source, KEY_WORDS):  
                         self.rs.sadd('message_urls',url)
			 #print title_remove_source
	
	#将感兴趣的页面数据保存在redis中
    def _putUrlsIntoRedis(self, urls):
        for url in urls:
            self._putMessageUrlIntoRedis(url)

	#从redis中获取页面的信息
    def _getMessageUrlsFromRedis(self):
        ret = self.rs.smembers('message_urls')
        urls = ""
        for herf in ret:
            urls += herf + "<br>"
        return len(ret), urls
	
	#发送招聘信息
    def sendMessage(self):
        msg_num, content = self._getMessageUrlsFromRedis()
        if msg_num <= 0 :
            print "none messages to send..."
            return
        sub = "[找工作，找实习] 共有%d条信息" % msg_num
		#print sub
        msg = MIMEText(content, 'html', 'utf-8')
        msg["Accept-Language"]="zh-CN"
        msg["Accept-Charset"]="ISO-8859-1, utf-8"
        msg['Subject'] = sub
        msg['From'] = SEND_EMAIL
        msg['to'] = ",".join(RECEIVE_MAIL_LIST)
        try:
            smtp = smtplib.SMTP()
            smtp.connect(SEND_MAIL_HOST)
            smtp.starttls()
            smtp.login(SEND_MAIL_USER, SEND_MAIL_PASSWORD)
            smtp.sendmail(SEND_EMAIL,RECEIVE_MAIL_LIST,msg.as_string())    
            print "send message sucessfully..."
        except Exception, e:
            print "fail to send message: "+ str(e)
        finally:
            smtp.quit()


    def run(self):
        print "crawler is going to start..."
        print "it may take several seconds,please wait..."
        self.rs.delete('message_urls')
        for http_query in self.http_querys :
            urls = self._parseHtmlToUrls(**http_query)
            self._putUrlsIntoRedis(urls)
        print "crawler has finished..."

if __name__ == '__main__':


    crawler = Crawler()
    crawler.run()
    crawler.sendMessage()
    #设置爬取招聘信息的间隔时间 #单位/小时
    sched = Scheduler()
    sched.daemonic = False 
    sched.add_interval_job(crawler.run, hours=48)
    sched.add_interval_job(crawler.sendMessage, hours=48)
    sched.start()
                         
