import requests
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote


class mantan_web:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.main_url = 'https://mantan-web.jp'
        self.session.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        self.session.headers['referer'] = 'https://gravure.mantan-web.jp'

    def get_size_guessing_func(self, large_num):
        def get_large_img(url):
            m = re.match(r"^.*(_thumb|_size(\d{1,2}))(.jpg|.jpeg|.png)$", url, re.IGNORECASE)
            if m:
                ext = m[3]
                if ext:
                    return {
                        "url": url.replace(m[1] + ext, f"_size{large_num}{ext}"),
                        "retries": [url.replace(m[1] + ext, f"_size{i}{ext}") for i in range(large_num - 1, 5, -1)]
                    }
            return {"url": url, "retries": []}

        return get_large_img

    def validate_url(self, url):
        # 使用 HEAD 请求检查图片是否存在
        try:
            response = self.session.head(url, allow_redirects=True)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_page_info(self):
        # 根据URL规则调整URL
        if 'photopage' not in self.url:
            self.url = self.url.split('.html')[0] + '/photopage/001.html'

        # 获取页面
        resp = self.session.get(self.url)
        resp.encoding = resp.apparent_encoding  # 设置正确的编码方式
        soup = BeautifulSoup(resp.text, 'html.parser')

        # 获取标题
        title = re.sub(r'\s', ' ', soup.find('div', class_='article__head').find('h1').text.strip())

        # 获取图片列表
        image_list = []

        # JavaScript 中的选择器列表
        selectors = [
            ".article__wrap .article__photolist img",  # article image gallery
            ".photo__wrap .photo__photolist img",  # article image gallery
            ".article__wrap .photo__photo img",  # article top image
            ".article__wrap .photo__photo--minh img",  # article top image
            ".photo__wrap .photo__photo img",  # photo page top image
            ".photo__wrap .photo__photolist .thumb-item img",  # photo page top image
            ".photo__photolist-wrap .swiper-slide .photo__photolist-item img",  # photo page top image
        ]

        get_large_img = self.get_size_guessing_func(10)

        # 查找符合条件的图片
        for selector in selectors:
            for img_tag in soup.select(selector):
                img_url = img_tag.get('src') or img_tag.get('data-src')
                if img_url and not img_url.endswith("/clear.gif"):
                    img_info = get_large_img(img_url)
                    # 尝试获取 large size 图片并验证
                    if self.validate_url(img_info["url"]):
                        image_list.append(img_info["url"])
                    else:
                        # 尝试回退机制
                        for retry_url in img_info["retries"]:
                            if self.validate_url(retry_url):
                                image_list.append(retry_url)
                                break

        # 如果没有找到图片，尝试从 script 标签中提取 JSON 数据
        if not image_list:
            script_content = ""
            for script_tag in soup.find_all('script'):
                if 'var __images = JSON.parse' in script_tag.text:
                    script_content = script_tag.text
                    break

            if script_content:
                json_match = script_content.split("('")[1].replace("')", '')
                list_ = json.loads(json_match)
                for item in list_:
                    img_info = get_large_img(item['src'])
                    # 验证 large size 图片链接是否有效
                    if self.validate_url(img_info["url"]):
                        image_list.append(img_info["url"])
                    else:
                        # 尝试回退机制
                        for retry_url in img_info["retries"]:
                            if self.validate_url(retry_url):
                                image_list.append(retry_url)
                                break

        # 去掉重复的图片 URL
        image_list = list(set(image_list))

        return title, image_list


# # 测试使用改进后的类
# app = mantan_web('https://mantan-web.jp/article/20241118dog00m200014000c.html')
# print(app.get_page_info())
