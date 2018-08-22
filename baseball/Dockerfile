# Pythonは公式イメージ
FROM python:3.6

LABEL  maintainer "nnashiki <n.nashiki.work@gmail.com>"



# 各ライブラリインストール
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y 	sqlite3\
                        tree\
                        mysql-client

# pipでインストール
RUN pip install -U pip
RUN pip install scrapy==1.4\
                mysqlclient

# アプリケーションのコードをコンテナのappに追加
ADD baseball /usr/src/app

WORKDIR /usr/src/app
