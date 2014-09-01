jobhunter
=========

##概述

简易的爬虫程序，主要抓取在指定天数内若干bbs上的工作和实习链接，然后发送至目标邮箱中。


##功能概述

* conf.py 文件为配置文件

* main.py 文件为主功能文件

* beautifulsoup.py 文件为beautifulsoup功能文件

1. 爬取距今天天数之内的数据(在conf.py中修改INTERVAL_DAYS)

     比如"INTERVAL_DAYS = 2"表示抓取今天，昨天，前天的数据

2. 根据关键词抓取信息(在conf.py中修改KEY_WORDS)

     2.1. KEY_WORDS = (u'百度',u'全职',u'实习') 表示抓取含有"百度"，"全职","实习"任何一个关键字的信息

     2.2. KEY_WORDS = None 表示抓取所有信息

3. 邮件发送(在conf.py中修改RECEIVE_MAIL_LIST)

     3.1. RECEIVE_MAIL_LIST = ["XXXXXX@XX.com","XXXXX@XX.com",]  表示群发邮件

     3.2. RECEIVE_MAIL_LIST = ["coolws123@gmail.com",]           表示发送至指定邮箱

4. 目标网站(在conf.py中添加，更改HTTP_QUERYS)

   
   
      
     {     
        
        'host' : 'http://bbs.seu.edu.cn/', #网站的域名，'host'+'href'合成为一个每一条招聘信息的链接。
        
        'url'  : 'http://bbs.seu.edu.cn/nForum/board/Computer',       #设置要爬取的主页面，即从该首页进行爬取，一般为招聘主页。该页面包含了招聘信息的链接。
        
        'href' : r"^/nForum/article/Computer/\d+$",#每条招聘信息的链接
        #设置匹配字符串，匹配'url'网页中<a>标签的href内容。设置本项时可以在'url'网页中找一条招聘信息的超链接<a>，将其中的href内容放入字符串，href尾部数字部分用'\d+'代替，如果链接中有'?'，需要改成'\?'进行转义。
        #可根据<a>中的href前面链接一部分作为填写内容
        
        'source' :u'东南大学',  #信息所在来源
        
     },
        
  


##安装

1. 运行本程序前请先安装[redis](http://www.redis.io/)

     1.1. windows[下载链接](https://github.com/dmajkic/redis/downloads),如下载redis-2.4.5-win32-win64.zip,选中相应版本，双击redis-server.exe运行

     1.2. mac/linux[下载链接](http://www.redis.io/download)。可下载2.8.13 stable版。编译见下载页面Installation。运行$ src/redis-server

2. 安装python依赖包

     2.1. 依赖包包含requests,redis

     2.2. Mac OS X/Linux安装
   
           pip install requests
   
           pip install redis
   
     2.3. windows用户可先安装[pip](https://pip.pypa.io/en/latest/installing.html)，在利用pip安装或者下载依赖包相应的windows文件


##运行

    直接运行main.py文件

##TIPS

1. 运行程序之前，请确保redis已启动，依赖包已安装

2. 邮件发送至指定邮箱中，若没收到，可能是延迟，也可能已送入垃圾箱中，可在垃圾箱中查看（绝大多数为后者）
   
