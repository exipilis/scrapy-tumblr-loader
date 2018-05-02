# -*- coding: utf-8 -*-
import os
import re
from urllib.parse import urlparse

import scrapy


class TumblrSpiderSpider(scrapy.Spider):
    name = 'tumblr-spider'

    def start_requests(self):
        with open('start_urls.txt') as f:
            for url in f:
                yield scrapy.Request(url.strip())

    @staticmethod
    def get_fn(hostname, image_url):
        """
        create file name from url
        all images should be stored in 'images/hostname' folder
        :param hostname: tumblr blog hostname
        :param image_url: image url
        :return: file name
        """
        o = urlparse(image_url)
        fn = 'images/' + hostname + '/' + o.path.strip('/').replace('/', '_')
        return fn

    def parse(self, response):
        html = response.body.decode('utf-8')

        o = urlparse(response.url)

        for image_link in re.findall(r'https://\d+\.media\.tumblr\.com/[\d\w/_]+_\d+\.jpg', html):
            image_link = re.sub(r'_\d+.jpg', '_1280.jpg', image_link)
            fn = self.get_fn(o.hostname, image_link)
            if os.path.isfile(fn):
                continue

            print('image link ' + image_link)
            print(fn)
            print()

            d = os.path.dirname(fn)
            if not os.path.isdir(d):
                os.makedirs(d)
            yield response.follow(image_link, self.save_img, meta={'fn': fn})

        for page_link in re.findall(r'href[="]*(/page/\d+)[">]*', html):
            yield response.follow(page_link, self.parse)

    @staticmethod
    def save_img(response):
        with open(response.meta['fn'], 'wb') as f:
            f.write(response.body)
