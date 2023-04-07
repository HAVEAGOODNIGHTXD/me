import scrapy


class Movie(scrapy.Item):
    rank = scrapy.Field()  # 排名
    name = scrapy.Field()  # 影名
    link = scrapy.Field()  # 链接
    score = scrapy.Field()  # 评分
    quote = scrapy.Field()  # 简介