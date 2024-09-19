import requests
import re
import json
from bs4 import BeautifulSoup
import streamlit as st


class bubka_web:
    def __init__(self, url):
        self.url = url
        self.main_url = 'https://www.idol-culture.jp'
        if 'attachment_id' not in self.url:
            self.url = self.get_gallery_url()

    def headers(self):
        return {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8,ko;q=0.7,en;q=0.6,tr;q=0.5,ru;q=0.4',
            'referer': f'{self.url}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        }

    def get_gallery_url(self):
        resp = requests.get(self.url, headers=self.headers())
        soup = BeautifulSoup(resp.text, 'html.parser')
        attachment_link_area = soup.find('div', class_='btn_post_attachment_link')
        attachment_link = attachment_link_area.find('a')['href']
        return attachment_link

    def get_image_urls(self):
        resp = requests.get(self.url, headers=self.headers())
        soup = BeautifulSoup(resp.text, 'html.parser')
        entrybody = soup.find('div', class_='entrybody')
        ul_ = entrybody.find('ul', class_='post_attachment_thumbnail')
        if ul_:
            lis = ul_.find_all('li')
            image_urls = [self.main_url + li.find('img')['src'].replace('-300x300','') for li in lis]
            return image_urls
