# Pythonは公式イメージ
FROM python:latest

LABEL  maintainer "nnashiki <n.nashiki.work@gmail.com>"

# アプリケーションのコードをコンテナのappに追加
ADD baseball /usr/src/app

# 各ライブラリインストール
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y 	sqlite3\
                        tree

# ユーザ作成
RUN groupadd web
RUN useradd -d /home/python -m python
RUN echo "python:passwd" | chpasswd

# pipでインストール
RUN pip install -U pip
RUN pip install scrapy

# ユーザを変更
USER python
