import requests
import re
import json
from bs4 import BeautifulSoup
import streamlit as st


def rajira(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8,ko;q=0.7,en;q=0.6,tr;q=0.5,ru;q=0.4',
        'cookie': 'AMCV_F2EE53755E31533C0A495F9D%40AdobeOrg=179643557%7CMCMID%7C18818877612564026475558796745638989303%7CMCAID%7CNONE%7CMCOPTOUT-1712496083s%7CNONE%7CvVersion%7C5.5.0; s_cc=true; s_ips_orgc=2510; s_tp_orgc=6120; s_ppv_orgc=p%253Aradirer%253Ars%253A88W859PYQ9%253Ablog%253Abl%253Ap30Z7R1ZY2%253Aindex%2C100%2C41%2C6120%2C7%2C7; s_sq=%5B%5BB%5D%5D',
        'referer': 'https://www.nhk.jp/p/radirer/rs/88W859PYQ9/blog/bl/p30Z7R1ZY2/?pastOffset=15',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }

    if '/' not in url.split('/',11)[-1]:
        url = f'{url}/'

    st.write('split:',rajira_url.split('/',11)[-1])
    st.write('url:',url)

    resp = requests.get(
        url,
        headers=headers
    )

    if resp.status_code == 200:
        resp_text = resp.text
        title = re.findall('<title>(.*?)</title>', resp_text)[0]
        json_file = \
        re.findall('<script type="application/json" id="__NUXT_DATA__" data-ssr="true">(.*?)</script>', resp_text)[0]
        # 使用正则表达式从地址中提取标识符
        matched_id = re.search(r'/bp/(\w+)/', url)
        if matched_id:
            identifier = matched_id.group(1)

            # 使用标识符构造匹配文本段落的正则表达式
            regex = fr'"{identifier}",\s*"(.*?)\d{{4}}-\d{{2}}-\d{{2}}T\d{{2}}:\d{{2}}:\d{{2}}\+\d{{2}}:\d{{2}}"'

            # 使用正则表达式匹配文本段落
            matched_text = re.search(regex, json_file, re.DOTALL)

            if matched_text:
                paragraph_text = matched_text.group(1)
                # 使用正则表达式提取标题
                title_match = re.search(r'【([^】]+)】', paragraph_text)
                if title_match:
                    title = title_match.group(1)


                    # 使用正则表达式匹配图片地址
                    image_urls = re.findall(r'!\[\]\((.*?)\)', paragraph_text)
                    return title,image_urls
