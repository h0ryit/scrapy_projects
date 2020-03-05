# -*- coding: utf-8 -*-

# Scrapy settings for doubanMovie project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'doubanMovie'

SPIDER_MODULES = ['doubanMovie.spiders']
NEWSPIDER_MODULE = 'doubanMovie.spiders'

# LOG_LEVEL = "WARNING"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'doubanMovie (+http://www.yourdomain.com)'
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0"
# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# MONGODB 主机环回地址127.0.0.1
MONGODB_HOST = '127.0.0.1'
# 端口号，默认是27017
MONGODB_PORT = 27017
# 设置数据库名称
MONGODB_DBNAME = 'DouBan'
# 存放本次数据的表名称
MONGODB_DOCNAME = 'DouBanMovies'


ITEM_PIPELINES = {
   'doubanMovie.pipelines.DoubanmoviePipeline': 300,
   'scrapy_redis.pipelines.RedisPipeline': 400,
}

# Scrapy_Redis配置信息

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True

# Redis数据库配置
REDIS_URL = "redis://127.0.0.1:6379"