#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: conf.py
#         Desc: 配置文件
#       Author: coolws
#        Email: coolws123@gmail.com
#=============================================================================
'''

timezone=['*','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# Redis的ip
REDIS_IP = '127.0.0.1'

# Redis的port
REDIS_PORT = 6379

#选择筛选规则,全部获取选择None，关键字获取选上面一个
#KEY_WORDS = (u'百度',u'全职',u'实习')
KEY_WORDS = None

#爬取距今天天数之内的数据，如INTERVAL_DAYS=1，表示爬取今天与昨天符合条件的信息
INTERVAL_DAYS = 1

# 发件箱的smtp
SEND_MAIL_HOST = "smtp.163.com"

# 发件箱的用户名
SEND_MAIL_USER = "coolws123"

# 发件箱的密码
SEND_MAIL_PASSWORD = "ws123581347"

# 收件箱
# 选择单个邮件发送还是群发
#RECEIVE_MAIL_LIST = ["XXXXXX@XX.com","XXXXX@XX.com",]  #群发
RECEIVE_MAIL_LIST = ["coolws123@gmail.com",] #单个发送

# 发件箱邮箱
SEND_EMAIL = "coolws123@163.com"

# 
headers = {
	"X-Requested-With" : "XMLHttpRequest",

	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
}

# 目标网站
HTTP_QUERYS = [
	
		{
		'host' : 'http://bbs.seu.edu.cn', #网站的域名，'host'+'href'合成为一个每一条招聘信息的链接。
		'url'  : 'http://bbs.seu.edu.cn/nForum/board/Computer', #设置要爬取的页面，该页面包含了招聘信息的链接，一般为招聘主页
                # href: 设置匹配字符串，匹配'url'网页中<a>标签的href内容。设置本项时可以在'url'网页中找一条招聘信息的超链接<a>，将其中的href内容放入字符串，href尾部数字部分用'\d+'代替，如果链接中有'?'，需要改成'\?'进行转义。
                # href 并不一定完全匹配，可将链接前面部分内容作为href 
		'href' : r"^/nForum/article/Computer/\d+$", 
		'source' : u'东南大学',
		},

		{
		'host' : 'http://bbs.nju.edu.cn/',
		'url'  : 'http://bbs.nju.edu.cn/g/JobExpress',
		'href' : r"^bbscon",
		'source' : u'南京大学',
		},

		{
		'host' : 'http://bbs.sjtu.edu.cn/',
		'url'  : 'http://bbs.sjtu.edu.cn/bbsdoc?board=JobInfo',
		'href' : r'^bbscon,board',
		'source' : u'上海交通大学',
		},

		{
		'host' : 'http://bbs.byr.cn',
		'url'  : 'http://bbs.byr.cn/board/JobInfo',
		'href' : r"^/article/JobInfo/\d+$",
		'source' : u'北京邮电大学',
		},
		
	    ]

