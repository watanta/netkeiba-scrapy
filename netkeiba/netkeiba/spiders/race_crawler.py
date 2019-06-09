# -*- coding: utf-8 -*-
import scrapy
import pathlib


class RaceCrawlerSpider(scrapy.Spider):
    name = 'race_crawler'
    allowed_domains = ['db.netkeiba.com']
    start_urls = ['http://db.netkeiba.com/?pid=race_top']
    base_url = "https://db.netkeiba.com"

    def write_html(self, response, url):
        """

        Parameters
        ----------
        path

        Returns
        -------


        """
        try:
            pathlib.Path('race_html').mkdir()
        except:
            pass

        path = 'race_html/' + url

        html_file = open(path, 'w')
        html_file.write(response.text)
        html_file.close()

    def parse(self, response):


        race_list = response.xpath('//td[contains(@class,"sat") or contains(@class,"sun") or contains(@class,"selected")]/a/@href').extract()

        race_list = [self.base_url + x for x in race_list]


        #カレンダーから各日に開催されたレースの一覧へ
        for race_url in race_list:
            if race_url is not None:
                request = scrapy.Request(url=race_url, callback=self.racelist_parse)
                yield request

        #カレンダーの前の月へ
        prev_month_url = response.xpath('//li[@class="rev"]/a[2]/@href').get()
        if prev_month_url is not None:
            prev_month_url = self.base_url + prev_month_url
            request = scrapy.Request(url=prev_month_url, callback=self.parse)

            yield request

    def racelist_parse(self, response):


        race_url_list = response.xpath('//dl[@class="race_top_data_info fc"]/dd/a/@href').extract()
        race_url_list = [self.base_url + x for x in race_url_list]

        #各レースページヘ
        for race_url in race_url_list:
            if race_url is not None:
                request = scrapy.Request(url=race_url, callback=self.race_parse)
                yield request


    def race_parse(self, response):

        #HTMLだけとってくる。スクレイプは別で処理する。
        self.write_html(response, response.url[29:-1])

        print("CRAWLED:" ,response.url)


