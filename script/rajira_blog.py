import requests
import re
import json
from bs4 import BeautifulSoup


def rajira(url):
    cookies = {
        'AMCV_F2EE53755E31533C0A495F9D%40AdobeOrg': '179643557%7CMCMID%7C18818877612564026475558796745638989303%7CMCAID%7CNONE%7CMCOPTOUT-1712496083s%7CNONE%7CvVersion%7C5.5.0',
        's_cc': 'true',
        's_sq': '%5B%5BB%5D%5D',
        's_ips_orgc': '911',
        's_tp_orgc': '17639',
        's_ppv_orgc': 'p%253Aradirer%253Ars%253A88W859PYQ9%253Ablog%253Abl%253Ap30Z7R1ZY2%253Abp%253Apq7Ko3NGGq%253Aindex%2C5%2C5%2C911%2C1%2C19',
}
    
    headers = {
        'referer': url,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }

    resp = requests.get(
        url,
        headers=headers,
        cookies=cookies
    )

    resp_text = resp.text
    print(resp_text)
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
