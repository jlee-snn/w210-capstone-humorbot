# -*- coding: utf-8 -*-
import scrapy
#FEED FORMAT
FEED_FORMAT = "csv"
FEED_URI = "reddit.csv"


class RedditspiderSpider(scrapy.Spider):
    name = 'redditSpider'
    allowed_domains = ['www.reddit.com']
    start_urls = ['https://www.reddit.com/r/puns/']

    custom_settings = {
        'DEPTH_LIMIT': 100
    }

    def parse(self, response):
        titles = response.xpath('//*[@class="_eYtD2XCVieq6emjKBH3m"]/text()').extract()
        body = response.xpath('//*[@class="_1qeIAgB0cPwnLhDF9XSiJM"]/text()').extract()
        datetimes = response.xpath('//*[@data-click-id="timestamp"]/text()').extract()
        for (title,body,datetime) in zip(titles,body,datetimes):
            yield {'Title': title.encode('utf-8'),'Date Time': datetime,'Body':body}

        next_page = response.xpath('//link[@rel="next"]/@href').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
