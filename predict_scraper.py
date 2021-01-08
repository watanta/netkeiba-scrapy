import lxml.html
import sqlite3
from contextlib import closing
import pathlib
import glob
import re
import pprint
import datetime
import sys

def scrape_from_page(html, filename):
    """
    1つのページからlxmlなどを使ってスクレイピングする。
    """

    html = lxml.html.fromstring(html)
    print('scraping', filename)

    # !!!xpathにtbodyふくむとうまくいかない　!!!
    result_table_rows = html.xpath('//*[@id="page"]/div[3]/div[2]/table//tr[@class="HorseList"]')

    for result_table_row in result_table_rows:

        # try:

        race_result = {
            'race_id' : filename,
            'wakuban': result_table_row.xpath("td/span")[0].text,
            'umaban': result_table_row.xpath("td")[1].text,
            'horsename': result_table_row.xpath("td[4]//a")[0].text,
            'horse_id': result_table_row.xpath("td[4]//a/@href")[0][30:-1],
            'sex&age': result_table_row.xpath("td[5]")[0].text,
            'weight': result_table_row.xpath("td[6]")[0].text,
            'jokey': result_table_row.xpath("td[7]//a")[0].text,
            'jokey_id': result_table_row.xpath("td[7]//a/@href")[0][31:-1],
            "horse_weight": result_table_row.xpath("td[9]")[0].text,
            "horse_weight_diff": result_table_row.xpath("td[9]/small")[0].text[1:-1],
            "odds": result_table_row.xpath("td[10]/span")[0].text,
            "popularity": result_table_row.xpath("td[11]/span")[0].text,
            

        }


        unique_key = ["race_id", "horse_id", "jokey_id"]
        put_to_sqlite(race_result, "predict", unique_key)


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

    path_to_htmldir = 'netkeiba/netkeiba/spiders/test_html/' + sys.argv[1]

    path = pathlib.Path(path_to_htmldir)

    read = path.read_text()
    scrape_from_page(read, path.name)




