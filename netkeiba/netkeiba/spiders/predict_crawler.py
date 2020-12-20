# -*- coding: utf-8 -*-
import scrapy
import pathlib


class PredictCrawlerSpider(scrapy.Spider):
    name = 'predict_crawler'
    allowed_domains = ['race.netkeiba.com']
    start_urls = ['http://db.netkeiba.com/?pid=race_top']
    base_url = "https://race.netkeiba.com/race/shutuba.html?race_id="

    def write_html(self, response, url):
        """

        Parameters
        ----------
        path

        Returns
        -------


        """
        try:
            pathlib.Path('predict_html').mkdir()
        except:
            pass

        path = 'predict_html/' + url

        html_file = open(path, 'w')
        html_file.write(response.text)
        html_file.close()

    def parse(self, response):


        race_list = [self.race_id]

        race_list = [self.base_url + x for x in race_list]


        for race_url in race_list:
            if race_url is not None:
                request = scrapy.Request(url=race_url, callback=self.race_parse)
                yield request

    def race_parse(self, response):

        #HTMLだけとってくる。スクレイプは別で処理する。
        self.write_html(response, response.url[52:])

        print("CRAWLED:" ,response.url)


