import lxml.html
import sqlite3
from contextlib import closing
import pathlib
import glob
import re
import pprint
import datetime

def scrape_from_page(html, filename):
    """
    1つのページからlxmlなどを使ってスクレイピングする。
    """

    html = lxml.html.fromstring(html)
    print('scraping', filename)

    # !!!xpathにtbodyふくむとうまくいかない　!!!
    tanshou_data = html.xpath('//th[@class="tan"]/following-sibling::td')

    try:

        tanshou_payback = {
            'race_id' : filename,
            'umaban': tanshou_data[0].text,
            'tanshou_payback': tanshou_data[1].text
        

        }

        tanshou_payback["race_name"] = html.xpath('//p[@class="smalltxt"]')[0].text
        
        ja_date = tanshou_payback["race_name"][:tanshou_payback["race_name"].find("日")+1]
        tanshou_payback["race_date"] = datetime.datetime.strptime(ja_date, '%Y年%m月%d日').strftime('%Y/%m/%d')

        put_to_sqlite(tanshou_payback, "payback")

    except:
        print('scraping fail!')



def put_to_sqlite(race_result, table_name):
    """
    sqlite3にデータを入れる

    Parameters
    ----------
    race_result : dict

    Returns
    -------

    """

    db_name = table_name + ".py"

    create_query = ''
    for key in race_result:
        row = '"' + key + '"' + ' varchar(30),'
        create_query = create_query + row

    create_query = create_query[:-1]

    create_query = 'create table ' + table_name + '(' + create_query + ')'

    conn = sqlite3.connect(db_name)

    c = conn.cursor()


    try:
        c.execute(create_query)
        print(db_name, 'is created!')
    except:
        print(db_name, 'is already exits!')
        pass

    put_query = ''
    for value in race_result.values():
        put_query = put_query + "'" +str(value) + "'" + ','

    put_query = put_query[:-1] #末尾の','とりのぞく

    put_query = "INSERT INTO " + table_name + " VALUES " + "(" + put_query + ")"


    c.execute(put_query)

    conn.commit()

    conn.close()



if __name__ == '__main__':

    path_to_htmldir = 'netkeiba/netkeiba/spiders/race_html/'

    path_iter = pathlib.Path(path_to_htmldir).iterdir()

    for path in path_iter:
        read = path.read_text()
        scrape_from_page(read, path.name)




