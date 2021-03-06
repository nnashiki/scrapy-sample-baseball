# 日本プロ野球の成績を取得してDBに格納するサンプル

## 何ができるのか

* 日本プロ野球機構(NPB)の[ホームページ](http://npb.jp/)から12球団選手の打撃・投球成績を取得
* 取得したデータをDB(SQLite3)に保存

## 動作環境

作者(shinyorke)の動作環境より.

* gitクライアント(何でもOK)
    * ソースコードを取得するために使う
    * 面倒くさい方は直接ダウンロードしてもらってもOK
* Python 3系の最新Ver
    * 3.6以上を推奨
    * 試してはいませんが,3.3.x以上なら動くと思う
    * 2.7.x系は未検証ですが多分動くと思います(がオススメしません&対応する気は無いです)
* Scrapyのインストールが必要(後述)
    * 1.4.0で検証(作成時点の最新バージョン)
* MacOS Sierra(10.12.6)
    * 上記のPythonバージョンおよびScrapyバージョンであればOS関係なく動くハズ

## セットアップ

### 1. リポジトリをclone or ダウンロードする

#### クローンの場合

```bash
$ git clone https://github.com/Shinichi-Nakagawa/scrapy-sample-baseball.git
```

#### ダウンロードの場合

```bash
$ wget https://github.com/Shinichi-Nakagawa/scrapy-sample-baseball/archive/master.zip
$ unzip master.zip
```

### 2. Pythonをインストール

* [ダウンロードサイト(公式)](https://www.python.org/downloads/)
* お使いのOS・プラットフォームに合わせてお使いください
* (繰り返しになりますが)Python 3.6以上が推奨です！

### 3. Scrapyをインストール

```bash
$ pip install scrapy
```

## 使い方

### 1. ディレクトリに移動

Scrapyのエンドポイントにcdします.

```bash
$ cd scrapy-sample-baseball/baseball
```

なお,ダウンロードで手に入れた人は最初のディレクトリ名が変わるので注意

```bash
$ cd scrapy-sample-baseball-master/baseball
```

### 2. 打者成績を取得

scrapyのコマンドで取得します.

初回実施の時はDBファイル(baseball.db)が生成され,同時にSchemeも作成されます.

```bash
$ scrapy crawl batter -a year=2017 -a league=1
```

### 3. 投手成績を取得

同じく,scrapyのコマンドで取得します.

初回実施の時はDBファイル(baseball.db)が生成され,同時にSchemeも作成されます.

```bash
$ scrapy crawl pitcher -a year=2017 -a league=1
```

### [TIPS]オプション引数(打者・投手共通)

いずれも省略可能,省略時はdefault値が使われます.

#### year(default:2017)

取得する成績年度

#### league(default:1)

1軍成績もしくは2軍成績

2軍の場合は

```bash
$ scrapy crawl {batter|pitcher} -a year=2017 -a league=2
```

これで取得可能です.

## データについて

### 構造

[baseball/baseball/item.py](https://github.com/Shinichi-Nakagawa/scrapy-sample-baseball/blob/master/baseball/baseball/items.py)に乗っているカラムと解説が全てです.

カラムの名称は一般的に使われる野球英語の略称を用いています.

詳細は各Itemのコメントを参照ください.

### Table Scheme

[baseball/baseball/pipelines.py](https://github.com/Shinichi-Nakagawa/scrapy-sample-baseball/blob/master/baseball/baseball/pipelines.py)にCreate Table文があります.

カラムの意味と解説はItemと全く同じです(id値とcreate_date/update_dateがあるぐらいの違い)

なお,indexは全く貼っていないので必要な方は随時書き換えてもらえると.


# 起動
```
docker build -t scrapy:0.1 -f `pwd`/baseball/Dockerfile .
docker run -it --rm --name scrapy --link baseball_db:baseball_db scrapy:0.1 bash

mysql -h 127.0.0.1 -u baseball_user baseball_db -p 



sqlite3 baseball.db
select * from pitcher;
select * from batter;
.exit
```

# noteで実行

```
import pymysql
db = pymysql.connect(host=  '172.17.0.2',
                             user='baseball_user',
                             password='baseball_pass',
                             db='baseball_db',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with db as cursor:
        sql = "SELECT * FROM batter"
        cursor.execute(sql)
 
        dbdata = cursor.fetchall()
        for rows in dbdata:
            print(rows)
 
finally:
    db.close()

```

サンプル

```
import pymysql
db = pymysql.connect(host=  '172.17.0.2',
                             user='baseball_user',
                             password='baseball_pass',
                             db='baseball_db',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

from matplotlib import pyplot as plt
plt.style.use('ggplot')

fig = plt.figure(figsize=(20, 20))

# プロットを1つ作成
ax = fig.add_subplot(111)
# ラベルをつける
ax.set_xlabel('打率')
ax.set_ylabel('ホームラン')
teamData = []

try:
    with db as cursor:
        sql = "SELECT * FROM batter where ab > 300 and ba > 0.3"
        cursor.execute(sql)
 
        dbdata = cursor.fetchall()
        for rows in dbdata:
            teamData.append([rows['name'],rows['ba'],rows['hr']])
finally:
    db.close()
    
for row in teamData:
    ax.scatter(row[1],row[2],alpha=0.5)
    ax.annotate(row[0],xy=(row[1],row[2]),size=10)
```

dataframe

```
import pymysql
import pandas as pd
db = pymysql.connect(host=  '172.17.0.2',
                             user='baseball_user',
                             password='baseball_pass',
                             db='baseball_db',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

from matplotlib import pyplot as plt
plt.style.use('ggplot')

fig = plt.figure(figsize=(20, 20))

# プロットを1つ作成
ax = fig.add_subplot(111)
# ラベルをつける
ax.set_xlabel('打率')
ax.set_ylabel('ホームラン')
teamData = []

try:
    with db as cursor:
        sql = "SELECT * FROM batter where ab > 300 and ba > 0.3"
        df = pd.read_sql_query(sql,db)
finally:
    db.close()

# 打率とHR
for _, row in df.iterrows():
    ax.scatter(row['ba'],row['hr'],alpha=0.5)
    ax.annotate(str(row['year'])+'-'+row['name'],xy=(row['ba'],row['hr']),size=15)

```


```
db = pymysql.connect(host=  '172.17.0.2',
                             user='baseball_user',
                             password='baseball_pass',
                             db='baseball_db',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with db as cursor:
        sql = "SELECT * FROM batter where ab > 400 and ba > 0.3"
        dfn = pd.read_sql_query(sql,db)
finally:
    db.close()

# matplotlibを使用してみる
from matplotlib import pyplot as plt
plt.style.use('ggplot')

fign = plt.figure(figsize=(20, 20))

# プロットを1つ作成
axn = fign.add_subplot(111)
# ラベルをつける
axn.set_xlabel('打率',size=20)
axn.set_ylabel('ホームラン',size=20)

# 打率とHR
for _, row in dfn.iterrows():
    axn.scatter(row['ba'],row['hr'],alpha=0.5)
    if  '山田' in row['name'] or '坂本' in row['name'] :
        axn.annotate(str(row['year'])+'-'+row['name'],xy=(row['ba'],row['hr']),size=15,alpha=0.8)
```

```
db = pymysql.connect(host=  '172.17.0.2',
                             user='baseball_user',
                             password='baseball_pass',
                             db='baseball_db',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with db as cursor:
        sql = "SELECT * FROM batter where name = '坂本 勇人' or name = '山田 哲人'"
        df3 = pd.read_sql_query(sql,db)
finally:
    db.close()

df3 = df3[['name','year','pa','ab','h','double','triple','hr','tb','rbi','sb','bb','so','dp','ba','slg','obp']].sort_values(['name','year'])

from matplotlib import pyplot as plt
import numpy as np
plt.style.use('ggplot')


fig = plt.figure(figsize=(20, 20))
ax = fig.add_subplot(1,1,1)

df3


x = np.array(['坂本 勇人','山田 哲人'])

df4 = df3[df3['name'] == '坂本 勇人' ]
df5 = df3[df3['name'] == '山田 哲人' ]

for year in (df5['year'].values.tolist()):
    print( df4[df4['year'] == year]['h'].values[0])
    print( df5[df5['year'] == year]['h'].values[0])
    plt.bar(x,  np.array([
        df4[df4['year'] == year]['h'].values[0],
        df5[df5['year'] == year]['h'].values[0]]), 
            label = str(year), align = "center")
        # bottomの登録必要

plt.legend()
plt.show()

df4[['h','year']]

```
