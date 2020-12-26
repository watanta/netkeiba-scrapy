# -*- coding: utf-8 -*-
import scrapy
import pathlib
import pandas as pd 

class ConditionCrawlerSpider(scrapy.Spider):
    name = 'condition_crawler'
    allowed_domains = ['db.netkeiba.com', "race.sp.netkeiba.com"]
    start_urls = ['https://race.sp.netkeiba.com/v2/barometer/profile.html']
    base_url = "https://race.sp.netkeiba.com/v2/barometer/score.html?race_id="

    def write_html(self, response, url):
        """

        Parameters
        ----------
        path

        Returns
        -------


        """

        try:
            pathlib.Path('condition_html').mkdir()
        except:
            pass

        path = 'condition_html/' + url

        html_file = open(path, 'w')
        html_file.write(response.text)
        html_file.close()

    def parse(self, response):


        p_temp = pathlib.Path('/opt/netkeiba-scrapy/netkeiba/netkeiba/spiders/race_html')
        str_p_list = [str(x)[-12:] for x in list(p_temp.iterdir())]
        str_p_df = pd.DataFrame({"date":str_p_list})
        # 調子分析は最古が20180304
        #　と思ったが全部のレース分あるっぽい
        # str_p_df_in_condition_date = str_p_df.loc[str_p_df["date"].str[:8] < "20180304",:]
        str_p_df_in_condition_date = str_p_df

        condition_url_list = [self.base_url + x + "/" for x in str_p_df_in_condition_date["date"]]


        for condition_url in condition_url_list:
            if condition_url is not None:
                request = scrapy.Request(url=condition_url, callback=self.condition_parse)
                yield request

    def condition_parse(self, response):
        
        #HTMLだけとってくる。スクレイプは別で処理する。
        self.write_html(response, response.url[61:-1])

        print("CRAWLED:" ,response.url)


