import scrapy
from getDouban.items import Movie

START = 0
LIST_URL = ['https://movie.douban.com/top250?start={}&filter='.format(num * 25) for num in range(10)]


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse_movie(self, response):
        for item in response.css('div.item'):
            movie = Movie()
            movie['rank'] = item.css('div.pic em::text').get()
            movie['name'] = item.css('div.info>div.hd>a span.title::text').get()
            movie['link'] = item.css('div.hd>a::attr(href)').get()
            movie['score'] = item.css('div.star>span.rating_num::text').get()
            movie['quote'] = item.css('div.bd>p.quote span.inq::text').get()
            yield movie

    def parse(self, response):
        for url in LIST_URL:
            yield scrapy.Request(url, self.parse_movie)