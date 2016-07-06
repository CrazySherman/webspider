import scrapy
from sample.items import PlayerItem
import time
import json
# from scrapy_splash import SplashRequest
# 3 key parameters to tune during scraping...
first_wait = 1
second_wait = 1
req_limit = 100
splash_wait = 3
class PlayerSpider(scrapy.Spider):
    '''
        crawl player stats and write each player per line to json file "players.jl"
    '''
    name = "players"
    # allowed_domains = ["dmoz.org"]
    start_urls = []
    player_names = {}

    def __init__(self):
        
        # collect all player names
        self.read_my_stats('../mystats.txt')
        print '[Debugging]:: number of players in total: ', len(self.player_names)
        # tickout the already downloaded players
        self.tickout_downloaded_players('players.jl')
        
        print "[Debugging]:: number of players to scrape: ", len(self.player_names)
        # read the one that has already scraped

        for val in self.player_names.itervalues():
            self.start_urls.append('http://www.nba.com/playerfile/' + '_'.join(val))
            # break
        # only send limited number of request each time
        if req_limit < len(self.start_urls):
            self.start_urls = self.start_urls[:req_limit]
        print '[Debugging]:: req limit: ', req_limit, ' -- wait time: ', splash_wait

        # print '[Debugging]:: ', self.start_urls

    def read_my_stats(self, filename):
        '''
            Read mystats.txt
        '''
        f = open(filename, 'r')
        for line in f:
            parts = line.split('\t')
            names = parts[0].split(' - ')
            for n in names:
                name = n.split(',')
                n = [name[1].lower(), name[0].lower()]
                if '_'.join(n) in self.player_names:
                    continue
                else:
                    self.player_names['_'.join(n)] = (n[0], n[1])

    def tickout_downloaded_players(self, filename):
        '''
            Read players.jl
        '''
        f = open(filename, 'r')
        for line in f:

            player = json.loads(line)

            name = '_'.join([s.lower() for s in player['name']])
            # print '[Debugging]:: ', name

            if name in self.player_names:
                del self.player_names[name]

    def start_requests(self):
        # print '[Debugging]::', self.start_urls
        for url in self.start_urls:
            # post_url = "http://173.255.210.201:8050/render.html"
            # body = json.dumps({
            #     "url": url, 
            #     })
            # headers = {'Content-Type': 'application/json'}
            # # url = "http://stats.nba.com/player/#!/2594/stats/"
            # yield scrapy.Request(post_url, self.parse, method='POST',
            #                          body=body, headers=headers)
            time.sleep(first_wait)
            yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': splash_wait,
                            # 'js_source': "playerPaginate('next')"
                    }
                }
            })

    def parse(self, response):
        
        # if response.status != 200:
        #     raise NameError('Scraping failed')
        stats = response.xpath("/html/body[@id='nbaTheme']/div[@id='nbaPage']/div[@id='nbaContent']/div[@id='nbaMainSection container']/div[@id='player-profile-pages']/div[@class='span6']/div[@id='profileButtons']/ul[@class='nav_main nav']/li[3]/a[@id='tab-stats']/@href") 
        if not stats:
            # raise NameError('first page not rendered')
            print response.request.body, " first page not rendered, recrawling..."
            return response.request

        url = stats.extract()[0]
        req_url = json.loads(response.request.body)
        name = req_url['url'].split('/')[-1].split('_')
        post_url = "http://173.255.210.201:8050/render.html"
        body = json.dumps({
            "url": url, 
            'wait': splash_wait,
            'name': name
            })
        headers = {'Content-Type': 'application/json'}
        # url = "http://stats.nba.com/player/#!/2594/stats/"
        time.sleep(second_wait)
        return scrapy.Request(post_url, self.parse_player_stats, method='POST',
                                 body=body, headers=headers)

    def parse_player_stats(self, response):
        
        # f = open('test2.html', 'w+')
        # f.write(response.body)
        # f.close()

        stat = response.xpath("/html/body/div[@id='app-container']/div[@id='main-container']/div[2]/div[@class='stats-player-page']/div[@class='ng-scope']/div[@class='row'][2]/div[@class='col-sm-12']/div[@class='ng-scope']/div[@class='stats-splits ng-scope']/div[@class='stat-table']/div[@class='ng-scope'][1]/div[@class='table-responsive']/table[@class='table']/tbody/tr[@class='ng-scope']/td/text()")
        player = PlayerItem()
        # name = response.xpath("/html/body/div[@id='app-container']/div[@id='main-container']/div[2]/div[@class='stats-player-page']/div[@class='ng-scope']/div[@class='row'][1]/div[@class='col-sm-12 ng-scope']/div[@class='summary']/div[@class='row'][2]/div[@class='col-xs-12']/div[@class='summary__info player-summary__info']/h2[@class='ng-binding']/text()")
        # # print '[Debugging]::', name, stat
        
        # player['name'] = name.extract()
        # player['name'][0], player['name'][1] = player['name'][0].lower(), player['name'][1].lower()
        # # player name fix
        # if player['name'][0] == 'manu' and player['name'][1] == 'ginobili' :
        #     player['name'][0] = 'emanuel'
        # if player['name'][0] == 'danny' and player['name'][1] == 'green' :
        #     player['name'][0] = 'daniel'
        # if player['name'][0] == 'tim' and player['name'][1] == 'hardaway jr.' :
        #     player['name'][0], player['name'][1] = 'timothy', 'hardaway'
        # if player['name'][0] == 'patty' and player['name'][1] == 'mills' :
        #     player['name'][0] = 'patrick'
        # if player['name'][0] == 'luc' and player['name'][1] == 'mbah a moute' :
        #     player['name'][1] = 'mbah_a_moute'
        # if player['name'][0] == 'j.j.' and player['name'][1] == 'barea' :
        #     player['name'][0] = 'jose'
        # if player['name'][0] == 'mo' and player['name'][1] == 'williams' :
        #     player['name'][0] = 'maurice'
        # if player['name'][0] == 'amar\'e' and player['name'][1] == 'stoudemire' :
        #     player['name'][0] = 'amare'
        # if player['name'][0] == 'tristan' and player['name'][1] == 'thompson' :
        #     player['name'][0] = 'tristan_t'
        # if player['name'][0] == 'j.r.' and player['name'][1] == 'smith' :
        #     player['name'][0] = 'jr'
        req_url = json.loads(response.request.body)
        player['name'] = req_url['name']
        player['stats'] = []
        stat = stat.extract() 
        if not stat or len(stat) < 22:
            # raise NameError('second page not rendered')
            print response.request.body, " second page not rendered, recrawling..."
            return response.request

        for i in [3,4,5,6,7,8,9,14,15,16,17,18,22]:
            player['stats'].append(stat[i])
        return player







