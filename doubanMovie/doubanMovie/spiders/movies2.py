# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
import re
from doubanMovie.items import DoubanmovieItem


class Movies2Spider(RedisCrawlSpider):
    name = 'movies2'
    allowed_domains = ['movie.douban.com']
    # start_urls = ['http://movie.douban.com/']
    redis_key = "doubanMovies"

    rules = (
        Rule(LinkExtractor(restrict_css="span.next a"), callback='parse_start_url', follow=True),
    )

    def parse_start_url(self, response):
        # 分组
        movies = response.css("ol.grid_view li")
        
        # 提取数据
        for movie in movies:
            item = DoubanmovieItem()
            item['title'] = movie.css(".hd span::text").extract_first()
            score = movie.css(".bd p::text").extract()
            
            for i in range(0, len(score)):
                score[i] = re.sub(r' |\xa0', '', score[i])
            item['score'] = movie.css(".star span.rating_num::text").extract_first()
            item['content'] = ''.join(score).strip('\n')
            item['info'] = movie.css(".quote span::text").extract_first()
        
            yield item

    # def parse_item(self, response):
    #     yield self.parse_start_url(response)
        
