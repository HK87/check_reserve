# -*- coding: utf-8 -*-

BOT_NAME = 'check_reserve'

SPIDER_MODULES = ['check_reserve.spiders']
NEWSPIDER_MODULE = 'check_reserve.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# アクセス先に負荷をかけないように。 単位は秒
DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {
    #'check_reserve.pipelines.ValidationPipeline': 300,
    'check_reserve.pipelines.MySQLPipeline': 800,
}

# MySQL
MYSQL_USER = 'scraper'
MYSQL_PASSWORD = 'xxxxxxxx'
