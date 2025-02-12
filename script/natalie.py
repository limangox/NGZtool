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

        if not gallery_group:
            try:
                # 第一页

                meta_image = soup.find('meta', attrs={'property': 'og:image'})['content'].split('?')[0]

                image_list.append(meta_image)

                article_class = soup.find('article', class_='NA_powerpush')
                PP_header = article_class.find('div', class_='PP_header')
                if PP_header:
                    header_image = PP_header.find('h1').find('img')['src'].split('?')[0]
                    image_list.append(header_image)

                if article_class:
                    image_blocks = article_class.find_all('img', class_='lazyload')
                    for img in image_blocks:
                        image_list.append(img['data-src'].split('?')[0])

                # 查找是否有其他页
                PP_pager_next = soup.find('li', class_='PP_pager_next')
                if PP_pager_next:
                    next_page_url = PP_pager_next.find('a')['href']
                    next_page_resp = self.session.get(next_page_url)
                    next_page_soup = BeautifulSoup(next_page_resp.text, 'html.parser')
                    article_class_next = next_page_soup.find('article', class_='NA_powerpush')
                    if article_class_next:
                        image_blocks = article_class_next.find_all('img', class_='lazyload')
                        for img in image_blocks:
                            image_list.append(img['data-src'].split('?')[0])
                    return title, image_list
                else:
                    return title, image_list
            except Exception as e:
                print(e)
                return None, None
