BOT_NAME = 'getDouban'

SPIDER_MODULES = ['getDouban.spiders']
NEWSPIDER_MODULE = 'getDouban.spiders'

ROBOTSTXT_OBEY = True

FEED_URI = 'douban.csv'
FEED_FORMAT = 'csv'
FEED_EXPORT_ENCODING = 'utf-8'
DEFAULT_REQUEST_HEADERS = {
    'authority': 'movie.douban.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 \
Safari/537.36 Core/1.94.169.400 QQBrowser/11.0.5130.400'
}
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 10