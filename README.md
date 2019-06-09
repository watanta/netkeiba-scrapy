netkeiba-scrapy
====

[netkeiba.com](https://www.netkeiba.com/)からデータを取ってきてデータベースを作る。

## Description
①crawlerがHTMLを取ってくる。  
②scraperがHTMLからスクレイピングして、データベースに突っ込む。
![構成図](https://files-uploader.xzy.pw/upload/20190609115341_5736645242.png)

## Usage

①cralwer起動  
scrapy run spider cralwer名  
②scraper起動  
python scraper名.py

cralwer一覧
- race_crawler:レース結果のHTMLをとってくる。ページ例：https://db.netkeiba.com/race/201909030101/

scraper一覧
- race_result:レース結果をスクレイピングする。

## Install

git clone 【これ】

pipenv install

## Tips
splite3のデータベースが作られる。データベースの確認は[ブラウザ](https://sqlitebrowser.org/)使うのがおすすめです。

## ToDo
- [予想](https://race.netkeiba.com/?pid=yoso&id=c201905030401)とか[掲示板](https://race.netkeiba.com/?pid=race_board&id=201905030401)とかもクローラとスクレイパー書く。
