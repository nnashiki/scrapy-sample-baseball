# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from scrapy.exceptions import DropItem


import MySQLdb
import time


class BaseballPipeline(object):

    CREATE_TABLE_BATTER ="""
    CREATE TABLE batter (
      id integer primary key,
      year integer,
      name text ,
      team text ,
      bat text ,
      games integer ,
      pa integer ,
      ab integer ,
      r integer ,
      h integer ,
      double integer ,
      triple integer ,
      hr integer ,
      tb integer ,
      rbi integer ,
      so integer ,
      bb integer ,
      ibb integer ,
      hbp integer ,
      sh integer ,
      sf integer ,
      sb integer ,
      cs integer ,
      dp integer ,
      ba real ,
      slg real ,
      obp real,
      create_date date,
      update_date date
    ) 
    """

    CREATE_TABLE_PITCHER ="""
    CREATE TABLE pitcher (
      id integer primary key,
      year integer,
      name text ,
      team text ,
      throw text ,
      games integer ,
      w integer ,
      l integer ,
      sv integer ,
      hld integer ,
      hp integer ,
      cg integer ,
      sho integer ,
      non_bb integer ,
      w_per real ,
      bf integer ,
      ip real ,
      h integer ,
      hr integer ,
      bb integer ,
      ibb integer ,
      hbp integer ,
      so integer ,
      wp integer ,
      bk integer ,
      r integer ,
      er integer ,
      era real ,
      create_date date,
      update_date date
    ) 
    """

    INSERT_BATTER = """
    insert into batter(
    `year`, 
    `name`, 
    `team`, 
    `bat`, 
    `games`, 
    `pa`, 
    `ab`, 
    `r`, 
    `h`, 
    `double`, 
    `triple`, 
    `hr`, 
    `tb`, 
    `rbi`, 
    `so`, 
    `bb`, 
    `ibb`, 
    `hbp`, 
    `sh`, 
    `sf`,
    `sb`,
    `cs`,
    `dp`,
    `ba`,
    `slg`,
    `obp`,
    `create_date`,
    `update_date`
    ) 
    values(
    %s,'%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s','%s' 
    )
    """

    INSERT_PITCHER = """
    insert into pitcher(
    year, 
    name, 
    team, 
    throw, 
    games, 
    w, 
    l, 
    sv, 
    hld, 
    hp, 
    cg, 
    sho, 
    non_bb, 
    w_per, 
    bf, 
    ip, 
    h, 
    hr, 
    bb, 
    ibb, 
    hbp, 
    so,
    wp,
    bk,
    r,
    er,
    era,
    create_date,
    update_date
    ) 
    values(
    %s,'%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s','%s'
    )
    """

    DATABASE_NAME = 'baseball.db'
    cursor = None
    connector = None

    def __init__(self):
        """
        Tableの有無をチェック,無ければ作る
        """

        connector = MySQLdb.connect(
            user='baseball_user',
            passwd='baseball_pass',
            host='172.17.0.2',
            port=3306,
            db='baseball_db',
            charset='utf8')

        connector.ping(True)
        cursor = connector.cursor()
        cursor.execute("select * from batter")

        for row in cursor.fetchall():
            print(row)

        cursor.close
        connector.close

    def open_spider(self, spider):
        """
        初期処理(DBを開く)
        :param spider: ScrapyのSpiderオブジェクト
        """

        self.connector = MySQLdb.connect(
            user='baseball_user',
            passwd='baseball_pass',
            host='172.17.0.2',
            port=3306,
            db='baseball_db',
            charset='utf8')

        self.cursor = self.connector.cursor()

    def process_item(self, item, spider):
        """
        成績をSQLite3に保存
        :param item: Itemの名前
        :param spider: ScrapyのSpiderオブジェクト
        :return: Item
        """
        # Spiderの名前で投入先のテーブルを判断
        if spider.name == 'batter':

            # 打者成績
            self.cursor.execute(self.INSERT_BATTER.format() % (
                int(item['year']),
                str(item['name']),
                str(item['team']),
                str(item['bat']),
                int(item['games']),
                int(item['pa']),
                int(item['ab']),
                int(item['r']),
                int(item['h']),
                int(item['double']),
                int(item['triple']),
                int(item['hr']),
                int(item['tb']),
                int(item['rbi']),
                int(item['so']),
                int(item['bb']),
                int(item['ibb']),
                int(item['hbp']),
                int(item['sh']),
                int(item['sf']),
                int(item['sb']),
                int(item['cs']),
                int(item['dp']),
                float(item['ba']),
                float(item['slg']),
                float(item['obp']),
                time.strftime('%Y-%m-%d %H:%M:%S'),
                time.strftime('%Y-%m-%d %H:%M:%S')
            ))
        elif spider.name == 'pitcher':
            # 投手成績
            self.cursor.execute(self.INSERT_PITCHER,(
                item['year'], item['name'], item['team'], item['throw'], item['games'], item['w'], item['l'],
                item['sv'], item['hld'], item['hp'], item['cg'], item['sho'], item['non_bb'], item['w_per'], item['bf'],
                item['ip'], item['h'], item['hr'], item['bb'], item['ibb'], item['hbp'], item['so'], item['wp'],
                item['bk'], item['r'], item['er'], item['era'],
            ))
        else:
            raise DropItem('spider not found')

        self.connector.commit()
        return item

    def close_spider(self, spider):
        """
        終了処理(DBを閉じる)
        :param spider: ScrapyのSpiderオブジェクト
        """
        self.cursor.close
        self.connector.close