# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ReviewItem
from scrapy_redis.spiders import RedisCrawlSpider


class DbreviewSpider(RedisCrawlSpider):
    name = 'dbreview'
    allowed_domains = ['douban.com']
    # start_urls = ['http://douban.com/']
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    redis_key = 'dbreview:start_urls'
    #  lpush dbreview:start_urls https://movie.douban.com/subject/26636712/comments?start=0&limit=20

    rules = (
        Rule(LinkExtractor(allow=r'start=\d+'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        print('-' * 30)
        comment = '//div[@class="comment-item"]//span[@class="short"]/text()'
        reviews = response.xpath(comment).extract()

        for review in reviews:
            item = ReviewItem()
            item['review'] = review.strip()
            print(111111, item)
            yield item
