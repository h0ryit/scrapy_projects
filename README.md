## 项目介绍

本项目包含五个爬虫，是我自己在学习scrapy框架时的练手项目

### woaidu
`www.woaidu.la`

功能：
- 爬取我爱读小说网站下的所有小说，并下载到本地
- 采用scrapy-redis实现分布式爬取
- 使用下载中间件实现动态ua头 和 代理池 以达到反反爬的效果
- 使用crwalspider模板

item：
- category   类别
- title         标题
- author     作者
- Introduction   简介
- url        小说url
- filepath   文件地址

### sina

`http://news.sina.com.cn/guide/`

爬取新浪新闻网下的每一类下的每一条新闻

item:
- parentTitle 大类标题
- parentUrls 大类的url
- subTitle 小类的标题
- subUrls 小类url
- subFilename 小类目录存储路径
- sonUrls 小类下的子链接
- head 文章标题
- content 文章内容

### doubanMovie
分别使用`Spider`模板 和`RedisCrawlSpider`模板实现`movies.py`和`movies2.py`

主要功能是爬取豆瓣电影区评分前250的电影信息

item包含电影标题，电影评分，制作信息，电影简介

### douyu_yz
功能：爬取并下载斗鱼直播颜值区主播的图片信息并下载到本地

实现json解析和翻页功能

### yangguang
`sun0769.com`

爬取阳光政务平台投诉帖子的编号、帖子的url、帖子的标题，和帖子里的内容
