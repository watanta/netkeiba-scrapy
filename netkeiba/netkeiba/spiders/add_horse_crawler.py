
# -*- coding: utf-8 -*-

# 2回目以降のクロウラー
# race_idのリストを受け取ってそれに出場した馬ページのHTMLを取得
import scrapy
import pathlib
import pandas as pd


class AddHorseCrawlerSpider(scrapy.Spider):
    name = 'add_horse_crawler'
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
            pathlib.Path('horse_html').mkdir()
        except:
            pass

        path = 'horse_html/' + url

        html_file = open(path, 'w')
        html_file.write(response.text)
        html_file.close()

    def parse(self, response):
        
        race_id_list = pd.read_csv("add_race_id_list.csv")
        race_url_list = [self.base_url + "/race/" + str(x) + "/" for x in race_id_list["race_id"].values.tolist()]
        print("race_url_list", race_url_list)
        #各レースページヘ
        for race_url in race_url_list:
            if race_url is not None:
                request = scrapy.Request(url=race_url, callback=self.race_parse)
                yield request

    def race_parse(self, response):

        # 各競走馬のページへ飛ぶ
        race_id = response.url[29:-1]
        horse_list = response.xpath('//*[@id="umalink_'+ race_id +'"]/@href').extract()
        horse_url_list = ["https://db.netkeiba.com" + x for x in horse_list]
        for horse_url in horse_url_list:
            if horse_url is not None:
                request = scrapy.Request(url=horse_url, callback=self.horse_parse)
                yield request


    def horse_parse(self, response):

        #HTMLだけとってくる。スクレイプは別で処理する。
        self.write_html(response, response.url[30:-1])

        print("CRAWLED:" ,response.url)



