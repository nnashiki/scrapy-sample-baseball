# Pythonは公式イメージ
FROM python:3.7

LABEL  maintainer "nnashiki <n.nashiki.work@gmail.com>"



# 各ライブラリインストール
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y 	tree\
                        mysql-client

# pipでインストール
RUN pip install -U pip
RUN pip install scrapy \
                mysqlclient \
                pillow

# アプリケーションのコードをコンテナのappに追加
ADD baseball /usr/src/app

WORKDIR /usr/src/app
