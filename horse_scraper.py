import lxml.html
import sqlite3
from contextlib import closing
import pathlib
import glob
import re
import pprint
import datetime
import re

def scrape_from_page(html, filename):
    """
    1つのページからlxmlなどを使ってスクレイピングする。
    """

    html = lxml.html.fromstring(html)
    print('scraping', filename)

    # !!!xpathにtbodyふくむとうまくいかない　!!!
    result_table_rows = html.xpath('//*[@id="contents"]/div[5]/div/table//tr[not(contains(@align, "center"))]')

    for result_table_row in result_table_rows:

        #　どうしてもスクレイプうまくいかないhtmlはある。（netkeiba側でミスってるとき）そのためのtry-except
        # try:

        race_href = result_table_row.xpath("td[5]/a/@href")[0]
        jokey_href = result_table_row.xpath("td[13]/a/@href")[0]

        horse_result = {
            'horse_id' : filename,
            "horse_name": html.xpath('//*[@id="db_main_box"]/div[1]/div[1]/div[1]/h1')[0].text,
            'sell_price': html.xpath('//*[@id="db_main_box"]/div[2]/div/div[2]/table//td')[5].text,
            'birth_date': html.xpath('//*[@id="db_main_box"]/div[2]/div/div[2]/table//tr[1]/td')[0].text,
            "race_date": result_table_row.xpath("td[1]/a")[0].text,
            "race_id": re.sub("\\D", "", race_href),
            "horse_num": result_table_row.xpath("td[7]")[0].text,
            "wakuban": result_table_row.xpath("td[8]")[0].text,
            "umaban": result_table_row.xpath("td[9]")[0].text,
            "odds": result_table_row.xpath("td[10]")[0].text,
            "popularity": result_table_row.xpath("td[11]")[0].text,
            "finish_order": result_table_row.xpath("td[12]")[0].text,
            "jokey_id": re.sub("\\D", "", jokey_href),
            "weight": result_table_row.xpath("td[14]")[0].text,
            "distance": result_table_row.xpath("td[15]")[0].text,
            "field_condition": result_table_row.xpath("td[16]")[0].text,
            "finish_time": result_table_row.xpath("td[18]")[0].text,
            "horse_weight": result_table_row.xpath("td[24]")[0].text,

        

        }

        unique_key = ["horse_id", "race_id"]
        put_to_sqlite(horse_result, "horse", unique_key)

        # except:
        #     print('scraping fail!')



def put_to_sqlite(race_result, table_name, unique_key):
    """
    sqlite3にデータを入れる

    Parameters
    ----------
    race_result : dict

    Returns
    -------

    """

    db_name = table_name + ".db"

    create_query = ''
    for key in race_result:
        row = '"' + key + '"' + ' varchar(30),'
        create_query = create_query + row

    row = 'unique(' + ", ".join(unique_key) + '),'
    create_query = create_query + row

    create_query = create_query[:-1]

    create_query = 'create table ' + table_name + '(' + create_query + ')'

    conn = sqlite3.connect(db_name)

    c = conn.cursor()


    try:
        c.execute(create_query)
        print(db_name, 'is created!')
    except:
        #print(db_name, 'is already exits!')
        pass

    put_query = ''
    for value in race_result.values():
        put_query = put_query + "'" +str(value) + "'" + ','

    put_query = put_query[:-1] #末尾の','とりのぞく

    put_query = "INSERT OR IGNORE INTO "+ table_name +" VALUES " + "(" + put_query + ")"


    c.execute(put_query)

    conn.commit()

    conn.close()



if __name__ == '__main__':

    path_to_htmldir = 'netkeiba/netkeiba/spiders/horse_html/'

    path_iter = pathlib.Path(path_to_htmldir).iterdir()

    for path in path_iter:
        read = path.read_text()
        scrape_from_page(read, path.name)




