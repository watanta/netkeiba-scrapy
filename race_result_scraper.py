import lxml.html
import sqlite3
from contextlib import closing
import pathlib
import glob
import re
import pprint

def scrape_from_page(html, filename):
    """
    1つのページからlxmlなどを使ってスクレイピングする。
    """

    html = lxml.html.fromstring(html)
    print('scraping', filename)

    # !!!xpathにtbodyふくむとうまくいかない　!!!
    result_table_rows = html.xpath('//table[@class="race_table_01 nk_tb_common"]//tr[position()>1]')

    for result_table_row in result_table_rows:

        try:

            race_result = {
                'race_id' : filename,
                'order': result_table_row.xpath('td[1]')[0].text,
                'wakuban': result_table_row.xpath('td[2]/span')[0].text,
                'umaban': result_table_row.xpath('td[3]')[0].text,
                'horsename': result_table_row.xpath('td[4]/a/@title')[0],
                'horse_id': result_table_row.xpath('td[4]/a/@href')[0][7:-1],
                'sex&age': result_table_row.xpath('td[5]')[0].text,
                'weight': result_table_row.xpath('td[6]')[0].text,
                'jokey': result_table_row.xpath('td[7]/a/@title')[0],
                'jokey_id': result_table_row.xpath('td[7]/a/@href')[0][8:-1],
                'time': result_table_row.xpath('td[8]')[0].text,
                'diff_from_top': result_table_row.xpath('td[9]')[0].text,
                'order_of_corners':result_table_row.xpath('diary_snap_cut[1]/td[2]')[0].text,
                'nobori': result_table_row.xpath('diary_snap_cut[1]/td[3]/span')[0].text,
                'tanshou_odds': result_table_row.xpath('td[10]')[0].text,
                'popularity': result_table_row.xpath('td[11]/span')[0].text,
                'horse_weight': result_table_row.xpath('td[12]')[0].text,
                'trainer': result_table_row.xpath('td[13]/a/@title')[0],
                'trainer_id': result_table_row.xpath('td[13]/a/@href')[0][9:-1],
                'owner': result_table_row.xpath('diary_snap_cut/td/a/@title')[0],
                'owner_id': result_table_row.xpath('diary_snap_cut/td/a/@href')[0][7:-1],
                'reward': result_table_row.xpath('diary_snap_cut[3]/td[2]')[0].text

            }

            put_race_result_to_sqlite(race_result)

        except:
            print('scraping fail!')



def put_race_result_to_sqlite(race_result):
    """
    sqlite3にデータを入れる

    Parameters
    ----------
    race_result : dict

    Returns
    -------

    """

    db_name = 'race.db'

    create_query = ''
    for key in race_result:
        row = '"' + key + '"' + ' varchar(30),'
        create_query = create_query + row

    create_query = create_query[:-1]

    create_query = 'create table race_result ' + '(' + create_query + ')'

    # print(create_query)

    conn = sqlite3.connect(db_name)

    c = conn.cursor()


    try:
        c.execute(create_query)
        print(db_name, 'is created!')
    except:
        # print(db_name, 'is already exits!')
        pass

    put_query = ''
    for value in race_result.values():
        put_query = put_query + "'" +str(value) + "'" + ','

    put_query = put_query[:-1] #末尾の','とりのぞく

    put_query = "INSERT INTO race_result VALUES " + "(" + put_query + ")"


    c.execute(put_query)

    conn.commit()

    conn.close()







if __name__ == '__main__':

    path_to_htmldir = 'netkeiba/netkeiba/race_html/'

    path_iter = pathlib.Path(path_to_htmldir).iterdir()

    for path in path_iter:
        read = path.read_text()
        scrape_from_page(read, path.name)




