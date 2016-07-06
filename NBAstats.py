import scrapy
from scrapy.selector import Selector

class NBAItem(scrapy.Item):
    players = scrapy.Field()
    pm = scrapy.Field()


files = ["NBAdata/" + str(i) + ".html" for i in range(1,6)]
def parseHTML(files):

    for f in files:
        res = open(f, 'r')
        txt = res.read()
        res.close()
        sel = Selector(text=txt)
        trs = sel.xpath("//div[@id='app-container']/div[@id='main-container']/div[2]/div[@class='stats-league-lineups-page']/div[@class='row']/div[@class='col-sm-12']/div[@class='ng-scope']/div[@class='stats-splits league-lineups ng-scope']/div[@class='stat-table']/div[@class='ng-scope']/div[@class='table-responsive']/table[@class='table']/tbody/tr[@class='ng-scope']")
        # print trs
        for tr in trs:
                item = NBAItem()
                # print tr
                item['players'] = tr.xpath("td[@class='player ng-binding']/text()").extract()[0]
                # print item['players']
                item['pm'] = tr.xpath("td[@class='ng-binding'][8]/text()").extract()[0]
                # print item['pm']
                yield item


if __name__ == '__main__':

    generator = parseHTML(files)
    stats = open('mystats.txt', 'w+')
    for item in generator:
        stats.write(item['players'] + '\t' + item['pm'] + '\n')
    stats.close()
