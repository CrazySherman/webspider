import scrapy
from sample.items import NBAItem

class NBASpider(scrapy.Spider):
    
    start_urls = []
    name = "NBA"
    def __init__(self):
        beg = 2015
        for i in range(1):
            tmp = beg - i
            self.start_urls.append("http://stats.nba.com/league/lineups/#!/?Season=" + str(tmp) \
                 + "-" + str((tmp + 1) % 100) + "&SeasonType=Playoffs") 
    def start_requests(self):
        print '[Debugging]::', self.start_urls
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0.5,
                            'js_source': "playerPaginate('next')"
                    }
                }
            })

    def parse(self, response):

        trs = response.xpath("/html[@class='ng-scope']/body/div[@id='app-container']/div[@id='main-container']/div[2]/div[@class='stats-league-lineups-page']/div[@class='row']/div[@class='col-sm-12']/div[@class='ng-scope']/div[@class='stats-splits league-lineups ng-scope']/div[@class='stat-table']/div[@class='ng-scope']/div[@class='table-responsive']/table[@class='table']/tbody/tr[@class='ng-scope']")
        # f = open('NBAstats.html', 'w+')
        # f.write(response.body)
        # print trs
        for tr in trs:
            item = NBAItem()
            # print tr
            item['players'] = tr.xpath("td[@class='player ng-binding']/text()").extract()
            item['pm'] = tr.xpath("td[@class='ng-binding'][8]/text()").extract()
            yield item
