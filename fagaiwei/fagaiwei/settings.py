# -*- coding: utf-8 -*-

# Scrapy settings for fagaiwei project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'fagaiwei'

SPIDER_MODULES = ['fagaiwei.spiders']
NEWSPIDER_MODULE = 'fagaiwei.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'fagaiwei (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

from datetime import datetime
from sqlalchemy import Column, String, create_engine, Integer, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 数据库连接信息
db_host = '127.0.0.1'
# db_host = '192.168.0.147'
db_user = 'root'
# db_user = 'admin'
db_pawd = 'root'
# db_pawd = 'adminpassword'
db_name = 'shares'
db_port = 3306
# 创建对象的基类:
Base = declarative_base()

engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'
                       .format(db_user, db_pawd, db_host, db_port, db_name), max_overflow=500)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()


class NewsItemInfo(Base):
    __tablename__ = "shares_newsdetail33"
    # 表结构
    id = Column(Integer, unique=True, primary_key=True)
    web_id = Column(Integer)
    web_name_t = Column(String(256))  # 网站名称
    web_url_t = Column(String(256))
    categoryid = Column(String(100))
    tagid = Column(String(100))
    title = Column(String(1024))  # 标题
    pub_time = Column(DateTime)  # 网站发布时间
    content = Column(Text)  # 中文内容
    keyword = Column(String(256))  # 关键字
    url = Column(String(256))  # 来源地址 原来链接,unique=True,nullable=False
    target = Column(String(10))
    # 增加一个md5字段 判断url 出现重复的 不插入
    add_time = Column(DateTime, default=datetime.now)  # 入库时间


# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 5000

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
import random

try:
    from .UserAgent import user_agent
except:
    from fagaiwei.UserAgent import user_agent
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    "User-Agent": random.choice(user_agent)
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'fagaiwei.middlewares.FagaiweiSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #    'fagaiwei.middlewares.FagaiweiDownloaderMiddleware': 543,
    # 'fagaiwei.middlewares.ProxyMiddleware': 543,
    # 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'fagaiwei.pipelines.FagaiweiPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
