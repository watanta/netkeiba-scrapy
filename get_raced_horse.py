# race_htmlから一度でもレースした馬のidを抽出する
import scrapy
import pathlib
import lxml
import pandas as pd 

def get_all_horse_crawled(target_race_id):

    path = '/opt/netkeiba-scrapy/netkeiba/netkeiba/spiders/race_html/' + target_race_id
    path = pathlib.Path(path)
    read = path.read_text()
    html = lxml.html.fromstring(read)

    horse_list = html.xpath('//*[@id="umalink_'+ target_race_id +'"]/@href')
    horse_id_list = [x[7:-1] for x in horse_list]

    return set(horse_id_list)

race_path_list = pathlib.Path('/opt/netkeiba-scrapy/netkeiba/netkeiba/spiders/race_html')
race_id_list = [str(x)[-12:] for x in list(race_path_list.iterdir())]

all_horse_set = set()
i = 0
for race_id in race_id_list:
    i += 1
    print(i/len(race_id_list))
    should = get_all_horse_crawled(race_id)
    all_horse_set = all_horse_set | should
all_horse_df = pd.DataFrame(all_horse_set)
all_horse_df.columns = ["columns"]
all_horse_df = all_horse_df.sort_values("columns", ascending=False)
all_horse_df.to_csv("all_horse.csv")
