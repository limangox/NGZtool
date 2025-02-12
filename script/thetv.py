import requests
import re
import json
from bs4 import BeautifulSoup
import streamlit as st


class thetv_web:
    def __init__(self, url):
        self.url = url
        self.pre_url = 'https://thetv.jp/'

        self.session = requests.Session()
        self.session.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        self.session.headers['referer'] = 'https://t.co/'

    def get_gallery_info(self):
        resp = self.session.get(self.url)
        soup = BeautifulSoup(resp.text, 'html.parser')

        # title
        title = soup.find('title').text

        news_image_block = soup.find('div', class_='newsimage')

        # 图片数量
        image_count = news_image_block.find('div',class_='imagecount').text

        ul_class = news_image_block.find('ul', class_='thumblist')

        li_list = ul_class.find_all('li')

        image_list = []
        for li in li_list:
            image = li.find('img')['data-original'].split('?')[0]
            orig_image_url = self.pre_url + image
            image_list.append(orig_image_url)

        return title, image_count, image_list





