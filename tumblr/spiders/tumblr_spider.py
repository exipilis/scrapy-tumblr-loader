# -*- coding: utf-8 -*-
import os
import re
from urllib.parse import urlparse

import scrapy


class TumblrSpiderSpider(scrapy.Spider):
    name = 'tumblr-spider'

    @staticmethod
    def parse_cookies(cookie: str) -> dict:
        cookie = cookie.split(':')[-1]
        q = {k.strip(): v for k, v in re.findall(r'(.*?)=(.*?);', cookie)}
        return q

    def start_requests(self):
        # cookies = self.parse_cookies(self.cookies_str)
        # print(cookies)

        with open('start_urls.txt') as f:
            for url in f:
                yield scrapy.Request(url.strip(), cookies={
                    'pfg': '477cc7d08af3433b166e93f39babf79d3be08db0396145eb8a30db4f5e7a137c%23%7B%22' +
                           'eu_resident%22%3A1%2C%22' +
                           'gdpr_is_acceptable_age%22%3A1%2C%22' +
                           'gdpr_consent_core%22%3A1%2C%22' +
                           'gdpr_consent_first_party_ads%22%3A1%2C%22' +
                           'gdpr_consent_third_party_ads%22%3A1%2C%22' +
                           'gdpr_consent_search_history%22%3A1%2C%22exp%22%3A1558465652%7D%237501684376'})

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

        re_images = re.findall(r'(https://\d+\.media\.tumblr\.com/[\d\w/_]+_\d+\.(jpg|gif))', html)
        for image_link in re_images:
            image_link = image_link[0]
            image_link = re.sub(r'_\d+.jpg$', '_1280.jpg', image_link)
            image_link = re.sub(r'_\d+.gif$', '_1280.gif', image_link)
            fn = self.get_fn(o.hostname, image_link)
            if os.path.isfile(fn):
                continue

            # print('image link ' + image_link)
            # print(fn)
            # print()

            d = os.path.dirname(fn)
            if not os.path.isdir(d):
                os.makedirs(d)
            yield response.follow(image_link, self.save_img, meta={'fn': fn})

        # some tumblr blogs do not have next page link in form of /page/\d+ substring
        # but we will crawl next page if there are downloadable images
        # this thing may not work for some blogs, uncomment with care
        # if len(re_images):
        #     page = 1
        #     match = re.search('/page/(\d+)', response.url)
        #     if match:
        #         page = match.group(1)
        #     page = int(page) + 1
        #     yield response.follow('/page/%s' % page, self.parse)

        for page_link in re.findall(r'href[="]*(/page/\d+)[">]*', html):
            yield response.follow(page_link, self.parse)

    @staticmethod
    def save_img(response):
        with open(response.meta['fn'], 'wb') as f:
            f.write(response.body)
