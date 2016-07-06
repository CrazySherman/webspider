import scrapy
from sample.items import YahooItem

class YahooSpider(scrapy.Spider):
    start_urls = ["http://www.yahoo.com"]
    name = "Yahoo"
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0.5}
                }
            })

    def parse(self, response):
        # response.body is a result of render.html call; it
        # contains HTML processed by a browser.
        links = response.xpath('//li[@class="js-stream-content"]//a')
        f = open('yahoopage.html', 'w+')
        f.write(response.body)
        for link in links:
            item = YahooItem()
            item['title'] = link.xpath('/text()').extract()
            item['link'] = link.xpath('/@href').extract()
            yield item
