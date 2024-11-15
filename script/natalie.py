import requests
import re
import json
from bs4 import BeautifulSoup
import streamlit as st


class natalie_web:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update(
            {
                'referer': 'https://natalie.mu/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            }
        )

    def get_gallery_image_groups(self):
        image_list = []
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text
        gallery_group = soup.find('div', class_="NA_article_gallery")

        if gallery_group:
            ul_group = gallery_group.find('ul', class_='NA_imglist')
            li_ = ul_group.find_all('li')
            for item in li_:
                image_url = item.find('img')['data-src'].split('?')[0]
                image_list.append(image_url)
            more_image = gallery_group.find('div', class_='NA_omit')
            if more_image:
                more_ul_group = more_image.find('ul', class_='NA_imglist')
                more_li_ = more_ul_group.find_all('li')
                for item in more_li_:
                    image_url = item.find('img')['data-src'].split('?')[0]
                    image_list.append(image_url)
            return title, image_list
        else:
            return None

