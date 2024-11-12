import requests
import re
import json
from bs4 import BeautifulSoup
import streamlit as st


class nbpress_web:
    def __init__(self, url):
        self.url = url
        self.gallery_id = url.split('/')[4]
        self.session = requests.Session()
        self.session.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        self.session.headers['referer'] = 'https://nbpress.online/'

    def get_gallery_image_groups(self):
        image_list = []
        response = self.session.get(self.url).text
        soup = BeautifulSoup(response, 'html.parser')
        gallery_groups = soup.find_all('div', id='gallery-1')[0].find_all('dl')
        title = soup.find('title').text.split('&#8211;')[0]
        if gallery_groups:
            for item in gallery_groups:
                image_url = item.find('a')['href']
                image_list.append(image_url)
            return title,image_list
        else:
            st.warning('该页面没有图片/代码异常')
            return None




