import requests
import re
import json
from bs4 import BeautifulSoup


def rajira(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8,ko;q=0.7,en;q=0.6,tr;q=0.5,ru;q=0.4',
        'referer': f'{url}',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }

    resp = requests.get(
        url,
        headers=headers
    )

    if resp.status_code == 200:
        resp_text = resp.text
        title = re.findall('<meta name="og:title" property="og:title" content="(.*?)">', resp_text)[0]
        json_file = \
        re.findall('<script type="application/json" id="__NUXT_DATA__" data-ssr="true">(.*?)</script>', resp_text)[0]
        # print(json.dumps(json.loads(json_file),ensure_ascii=False,indent=1))
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
