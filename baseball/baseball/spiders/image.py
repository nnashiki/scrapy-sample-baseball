# -*- coding: utf-8 -*-
import scrapy
from ..image_items import ImageItem
import re
from scrapy.exceptions import NotSupported
from urllib.parse import urlparse

class ImageSpider(scrapy.Spider):
      name = 'image'
      # 見つけたドメインを入れる
      tracked_domains = []
      # 全てを対象
      allowed_domains = ['npb.jp']

      def __init__(self, category=None, *args, **kwargs):
          super(ImageSpider, self).__init__(*args, **kwargs)
          self.start_urls = ['http://npb.jp/bis/teams/%s' % category]

      # response　を毎回処理する関数
      def parse(self, response):
          try:
              # データ処理
              # この関数内の処理が終わると続きを実行する
              # dataPipeline を利用した場合もここに戻って来る
              yield self.parse_items(response)

              # リンクを辿る
              for link in response.xpath('//@href').extract():
                  if re.match(r"^http?://", link) or re.match(r"^https?://", link):
                      yield scrapy.Request(link, callback=self.parse)
                  else:
                      yield scrapy.Request(response.urljoin(link), callback=self.parse)

          except NotSupported:
              # GET のレスポンスが txt じゃなかった場合
              # Spiders の logging 機能が用意されているのでそれを利用
              self.logger.info("Raise NotSupported")

      # ドメインごとにページに表示された画像を保存する
      def parse_items(self, response):
          # domain の抽出
          url = response.url
          parsed_url = urlparse(url)
          domain = parsed_url.netloc

          # 同じ Domain は一回しかチェックしない
          # if domain in self.tracked_domains:
          #     return

          self.tracked_domains.append(domain)

          item = ImageItem()
          item['domain'] = domain

          # title の抽出
          title = response.xpath(r'//html/head/title/text()').extract()
          if len(title) > 0:
              item['title'] = title[0]
          else:
              item['title'] = None

          # 画像 URL をセット
          item["image_urls"] = []
          for image_url in response.xpath("//*[@id=\"pc_v_photo\"]/img/@src").extract():
              if "http" not in image_url:
                  item["image_urls"].append(response.url.rsplit("/", 1)[0]
                         + "/" + image_url)
              else:
                  item["image_urls"].append(image_url)

          # item を返すと datapipeline に渡される
          return item