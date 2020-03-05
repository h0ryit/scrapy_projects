# -*- coding: utf-8 -*-
# 爬取豆瓣电影信息并将数据保存在mongodb中
import scrapy
from doubanMovie.items import DoubanmovieItem
import re


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['douban.com']
    start = 0
    # https://movie.douban.com/top250?start=0&filter=
    url = "https://movie.douban.com/top250?start={}&filter="
    start_urls = [url.format(start)] 

    def parse(self, response):
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
        
        # 翻页
        if self.start < 225:
            self.start += 25
        nexturl = self.url.format(self.start)
        yield scrapy.Request(nexturl)
