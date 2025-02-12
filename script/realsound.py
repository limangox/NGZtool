import requests
import re
import json
from bs4 import BeautifulSoup
import streamlit as st


class realsound_web:
    def __init__(self, url):
        self.url = url
        self.pre_url = 'https://realsound.jp'
        self.session = requests.Session()

        self.session.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

    def get_gallery_info(self):
        resp = self.session.get(self.url)
        soup = BeautifulSoup(resp.text, 'html.parser')

        title = soup.find('title').text

        gallery_link = soup.find('p', class_='img-link-wrap').find('a', class_='img-link')['href']

        return title, gallery_link

    def get_image_orig(self,image_link):
        orig_image_link = image_link.replace(re.findall(r'-\d+x\d+', image_link)[0],'')
        return orig_image_link

    def get_image_info(self):

        title, gallery_link = self.get_gallery_info()
        resp = self.session.get(gallery_link)
        soup = BeautifulSoup(resp.text, 'html.parser')

        attachment_list_imgs = soup.find('div', class_='attachment-list-imgs')

        a_block = attachment_list_imgs.find_all('a')

        image_links = []

        for a in a_block:
            image_link = a.find('img')['src']
            image_link_combine = self.pre_url + self.get_image_orig(image_link)
            image_links.append(image_link_combine)

        return title, image_links