# -*- coding: utf-8 -*-
# でレースに出たことのあるhorse_id一覧をとってから使う
import scrapy
import pathlib
import pandas as pd


class HorseCrawlerSpider(scrapy.Spider):
    name = 'horse_crawler'
    allowed_domains = ['db.netkeiba.com']
    start_urls = ['http://db.netkeiba.com/?pid=race_top']
    base_url = "https://db.netkeiba.com"
    # この年以降生まれの馬だけクロールする
    date_th = "2010"

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

        horse_id_df = pd.read_csv("/opt/netkeiba-scrapy/all_horse.csv")
        horse_id_df = horse_id_df.loc[(horse_id_df["columns"] > self.date_th + "000000"), :]
        horse_id_list = horse_id_df["columns"].values.tolist()
        horse_url_list = [self.base_url + "/horse/" + x for x in horse_id_list]

        #カレンダーから各日に開催されたレースの一覧へ
        for horse_url in horse_url_list:
            if horse_url is not None:
                request = scrapy.Request(url=horse_url, callback=self.horse_parse)
                yield request

    def horse_parse(self, response):
        
        #HTMLだけとってくる。スクレイプは別で処理する。
        self.write_html(response, response.url[30:-1])

        print("CRAWLED:" ,response.url)


