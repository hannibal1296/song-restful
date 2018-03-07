import scrapy
from scrapy.crawler import CrawlerProcess
from pdb import set_trace


class BugsAlbumSpider(scrapy.Spider):
    name = "Bugs_album_spider"
    start_urls = ['https://music.bugs.co.kr/chart/track/day/total?_redir=n',
                  'https://music.bugs.co.kr/chart/track/realtime/pop']

    def parse(self, response):
        SET_SELECTOR = '//tr[@rowtype="track"]'
        for albumset in response.xpath(SET_SELECTOR):
            album_url = albumset.css('.album::attr(href)').extract_first()
            yield scrapy.Request(
                url=album_url,
                callback=self.parse_album
            )

    def parse_album(self, response):

        a_selector = '//td/a'
        td_selector = '//tr/td'
        # a_list = response.xpath(a_selector)
        td_list = response.xpath(td_selector)

        title = response.css('.innerContainer h1::text').extract_first()
        name = response.xpath(a_selector+"/text()").extract_first()
        release = response.css('time::text').extract_first()
        description = response.css('.albumContents span::text').extract_first()

        ttype = response.xpath(td_selector+'/text()').extract()[2]
        set_trace()
        if ttype == "싱글":
            ttype = 'Single'
        elif ttype == "정규":
            ttype = 'Studio'
        elif ttype == "컴필레이션":
            ttype = 'Compilation'
        elif ttype == "EP(미니)":
            ttype = "EP"
        elif ttype == "OST":
            ttype = "OST"
        else:
            ttype = 'Unknown'

        # set_trace()  # todo

        album = {
            'title': title,
            'artist': name,
            'release': release,
            'type': ttype,
            'description': description,
        }

        yield album

# process = CrawlerProcess()
# process.crawl(BugsSpider)
# process.crawl(BugsArtistSpider)
