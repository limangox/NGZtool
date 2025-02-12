import textwrap
import time
import re
import requests
import json
import datetime
from datetime import timezone, timedelta
import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
from script.rajira_blog import rajira
from script.create_zip import create_zip
from script.bubka import bubka_web
from script.mantan import mantan_web
from script.nbpress import nbpress_web
from script.natalie import natalie_web
from script.thetv import thetv_web
from script.realsound import realsound_web

st.set_page_config(page_title="N46综合", layout="wide")

tz = timezone(timedelta(hours=9))
datetime = datetime.datetime.now(tz)


# 保存文件非法字符判定和修改
def sanitize_filename(filename):
    filename = unquote(filename)
    filename = re.sub(r'[「」\\/*?:"<>|\s#☆.]', "_", filename)
    parts = filename.split('-')
    sanitized_parts = [parts[0]] + [p.replace('.', '_') for p in parts[1:]]
    return '-'.join(sanitized_parts)


def get_news():
    toggle1 = st.toggle('按日期选择', value=True)
    toggle2 = st.toggle('按月份选择')

    date_sel = st.date_input('选择公告日期月份,默认查看当日的新闻', datetime)
    if toggle1:
        if toggle2:
            st.warning('请选择一种模式,不能两个一起选')
            st.exception(e)
        date_sel = date_sel.strftime("%Y%m%d")
    if toggle2:
        if toggle1:
            st.warning('请选择一种模式,不能两个一起选')
            st.exception(e)
        date_sel = date_sel.strftime("%Y%m")
        st.caption(f'已选择查看 {date_sel} 月的新闻')

    headers = {
        'authority': 'www.nogizaka46.com',
        'accept': '*/*',
        'accept-language': 'ja,zh;q=0.9,zh-CN;q=0.8,ko;q=0.7,en;q=0.6,tr;q=0.5',
        'cookie': 'WAPID=9ulLdh0k9EgQ2fqvv8frLAf9A6v8Qx9kvme; __td_signed=true; _ts_yjad=1643978843049; _fbp=fb.1.1643978843522.760024492; wovn_selected_lang=ja; _fbc=fb.1.1660921246855.IwAR3JBuS09qKl5C5hGlFnmSvXq4Zp1UBYNH_zuXsNk5yzQubh8zVPK7ULUnw; wap_last_event=showWidgetPage; _ga_R9MY5W6HJK=GS1.1.1673455267.2.1.1673455671.0.0.0; wovn_uuid=xz0kgt10x; _ga_FTL2JTLQ27=deleted; _ga_FTL2JTLQ27=deleted; WAPID=zbl5hvXIQwg48mEfUhnzZ36b55AyFHubOJy; _yjsu_yjad=1694868548.e0d068f0-15a2-4ea1-a2a8-4951c0cb4d63; _tt_enable_cookie=1; _ttp=N_SHHjlbfeGE97MJr1zC0WuHRR9; _ga_MQH5407CPF=GS1.1.1696987717.8.1.1696987994.0.0.0; __utmz=174951741.1698596854.460.30.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _gcl_au=1.1.694657561.1699162597; _gid=GA1.2.44276891.1699336932; __utma=174951741.1489452597.1643978843.1699243838.1699437704.466; _gat=1; _dc_gtm_UA-70388113-2=1; _dc_gtm_UA-70385727-1=1; _dc_gtm_UA-70441218-30=1; _ga_CYV9VQHJ8W=GS1.2.1699513558.59.1.1699513566.52.0.0; _ga_HRQHK75P9N=GS1.2.1699513558.94.1.1699513566.0.0.0; _ga=GA1.1.1489452597.1643978843; _td=c9a818f0-f0bc-49c7-8ba3-fe709ff29867; _ga_FTL2JTLQ27=GS1.1.1699513557.339.1.1699513572.45.0.0',
        'referer': 'https://www.nogizaka46.com/',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }

    params = {
        'dy': f'{date_sel}',
        'callback': 'res',
    }

    news_resp = requests.get('https://www.nogizaka46.com/s/n46/api/list/news', params=params, headers=headers)

    json_data = news_resp.content.decode().replace("res(", "")[:-2]

    news_json = json.loads(json_data)['data']

    if not news_json:
        st.info(f'{date_sel} 这一天没有新闻更新')

    for item in news_json:
        news_title = item['title']
        news_date = item['date']
        news_text = item['text']
        pattern = r'width="(\d+)" height="(\d+)"'
        replacement = 'width="50%" height="50%"'
        news_text = re.sub(pattern, replacement, news_text)
        if '/files/' in news_text:
            news_text = news_text.replace('/files/', 'https://www.nogizaka46.com/files/')

        with st.expander(news_title):
            st.caption(news_date)
            st.write(news_text, unsafe_allow_html=True)


def blog():
    member_list = [{'name': '乃木坂46', 'cate': '', 'code': '10001'},
                   {'name': '五百城茉央', 'cate': '', 'code': '55396'},
                   {'name': '池田瑛紗', 'cate': '', 'code': '55397'},
                   {'name': '一ノ瀬美空', 'cate': '', 'code': '55390'},
                   {'name': '伊藤理々杏', 'cate': '', 'code': '36749'}, {'name': '井上和', 'cate': '', 'code': '55389'},
                   {'name': '岩本蓮加', 'cate': '', 'code': '36750'}, {'name': '梅澤美波', 'cate': '', 'code': '36751'},
                   {'name': '遠藤さくら', 'cate': '', 'code': '48006'}, {'name': '岡本姫奈', 'cate': '', 'code': '55401'},
                   {'name': '小川彩', 'cate': '', 'code': '55392'}, {'name': '奥田いろは', 'cate': '', 'code': '55394'},
                   {'name': '賀喜遥香', 'cate': '', 'code': '48008'}, {'name': '金川紗耶', 'cate': '', 'code': '48010'},
                   {'name': '川﨑桜', 'cate': '', 'code': '55400'}, {'name': '久保史緒里', 'cate': '', 'code': '36753'},
                   {'name': '黒見明香', 'cate': '', 'code': '55383'}, {'name': '佐藤楓', 'cate': '', 'code': '36755'},
                   {'name': '佐藤璃果', 'cate': '', 'code': '55384'}, {'name': '柴田柚菜', 'cate': '', 'code': '48013'},
                   {'name': '菅原咲月', 'cate': '', 'code': '55391'}, {'name': '田村真佑', 'cate': '', 'code': '48015'},
                   {'name': '筒井あやめ', 'cate': '', 'code': '48017'}, {'name': '冨里奈央', 'cate': '', 'code': '55393'},
                   {'name': '中西アルノ', 'cate': '', 'code': '55395'}, {'name': '中村麗乃', 'cate': '', 'code': '36756'},
                   {'name': '林瑠奈', 'cate': '', 'code': '55385'}, {'name': '松尾美佑', 'cate': '', 'code': '55386'},
                   {'name': '向井葉月', 'cate': '', 'code': '36757'},
                   {'name': '矢久保美緒', 'cate': '', 'code': '48019'},
                   {'name': '弓木奈於', 'cate': '', 'code': '55387'},
                   {'name': '吉田綾乃クリスティー', 'cate': '', 'code': '36759'},
                   {'name': '与田祐希', 'cate': '', 'code': '36760'}, {'name': '運営スタッフ', 'cate': '', 'code': '40003'},
                   {'name': '3期生', 'cate': '', 'code': '40004'}, {'name': '4期生', 'cate': '', 'code': '40005'},
                   {'name': '新4期生', 'cate': '', 'code': '40001'}, {'name': '5期生', 'cate': '', 'code': '40007'}]

    headers = {
        'authority': 'www.nogizaka46.com',
        'accept': '*/*',
        'accept-language': 'ja,zh;q=0.9,zh-CN;q=0.8,ko;q=0.7,en;q=0.6,tr;q=0.5',
        'cookie': 'WAPID=9ulLdh0k9EgQ2fqvv8frLAf9A6v8Qx9kvme; wap_last_event=showWidgetPage; __td_signed=true; _ts_yjad=1643978843049; _fbp=fb.1.1643978843522.760024492; wovn_selected_lang=ja; _fbc=fb.1.1660921246855.IwAR3JBuS09qKl5C5hGlFnmSvXq4Zp1UBYNH_zuXsNk5yzQubh8zVPK7ULUnw; wap_last_event=showWidgetPage; _ga_R9MY5W6HJK=GS1.1.1673455267.2.1.1673455671.0.0.0; wovn_uuid=xz0kgt10x; _ga_FTL2JTLQ27=deleted; _ga_FTL2JTLQ27=deleted; WAPID=zbl5hvXIQwg48mEfUhnzZ36b55AyFHubOJy; _gcl_au=1.1.1700913064.1683221336; auth_tkn_nogizaka46.com=Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODY2NzM2OTAsImlhdCI6MTY4NDA4MTY5MCwibmJmIjowLCJzdWIiOiI3NjAwNTU0NzQxNDkxMzEzMTEiLCJpc3MiOiJmZW5zaS1pZC1ub2dpemFrYS1tb2JpbGUiLCJhdWQiOiJmZW5zaS1pZC1ub2dpemFrYS1tb2JpbGUifQ.yKCuEK_VaX_L8xZV0XDgPOPHr7jIsba_JHwK2LKzV-_LZOk1OwDSlsUa8faScViPpsu5qXmFfjFu4BRnOjsPsg; _ga_MQH5407CPF=GS1.1.1684659932.4.0.1684659932.0.0.0; __utmz=174951741.1685186281.336.16.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=174951741; _gid=GA1.2.303585636.1685585526; _td=c9a818f0-f0bc-49c7-8ba3-fe709ff29867; _ga=GA1.2.1489452597.1643978843; _ga_FTL2JTLQ27=GS1.1.1685599011.151.0.1685599011.0.0.0; _gat=1; __utma=174951741.1489452597.1643978843.1685585525.1685599012.346; __utmt=1; __utmb=174951741.1.10.1685599012',
        'referer': 'https://www.nogizaka46.com/s/n46/diary/MEMBER?ima=1116',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    css = '''<style>

    .css-1aumxhk {
            background-color: #9e3eb2;
        }
    .list_img {
        width: 15%;
        border-radius: 12px;
        height: 30%;
        aspect-ratio: 1/1;
        object-fit: cover;
      	display: flex;
      	position: relative;
      	align-items: flex-end;
    }

    #container {
      	max-width: 50%;
       	margin: 0 auto;
      	margin-top: 2vh;
      	display: flex;
    	flex-direction: column;


      /* 在水平轴线上居中放置 container */
      margin: 0 auto;

      /* 在 container 上方添加空白区域（视窗高度的 20% 位置） */
      margin-top: 2vh;
    }

    /* 在屏幕宽度小于或等于 600px 时应用以下样式 */
@media only screen and (max-width: 600px) {
  #container {
    max-width: 100%; /* 或者设置其他固定值 */
  }
}

    .card {
      /* 修改背景色 */
      display: flex;
      flex-direction: column;
      position: relative;
      background-color: white;

      /* 增加边框 */
      border: 1px solid #9e3eb2;

      /* 在边框和内容之间添加空白区域 */
      padding: 8px;

      border-radius: 12px;
    }

    .info-container {
        display: flex;
        justify-content: space-between;
        position: absolute;
        bottom: 0;
      	right: 0;
      	padding: 10px;
    }


    /* 给具有 tag class 的 div 元素添加样式 */
    .member_name {
      border: 1px solid #9e3eb2;
      box-shadow: 1px 1px 3px #9e3eb2;
      padding: 8px;
      border-radius: 15px;
      display: inline-block;
      font-size: 12px;
      padding: 5px;
      color: #9e3eb2;
    }

    .update_date {
      border: 1px solid #9e3eb2;
      box-shadow: 1px 1px 3px #9e3eb2;
      padding: 8px;
      border-radius: 15px;
      display: inline-block;
      padding: 5px;
      font-size: 12px;
      color: #788697;
    }

    .blog_title {
        position: absolute;
      max-width: 65%;
      word-wrap: break-word;
      text-align: left;
      top: 0;
      right: 0;
      margin: 10px;
        font-size: 16px;
        color: #9e3eb2;
    }

    .st-emotion-cache-19rxjzo{
        border: none;
        padding: 6px 24px;
        border-radius: 30px;

        font-weight: 600;
        color: #ffffff;
        background-color: #9e3eb2;

        /* Button 默认是行内元素，display 属性值为 block，margin 值为 0 auto; */
        margin: 0 auto;
        margin-top: 2px;
        display: block;

        /* Button 是一个可点击的元素，因此需要有一个 pointer cursor */
        cursor: pointer;
    }

    .st-emotion-cache-19rxjzo:focus,
    .st-emotion-cache-19rxjzo:hover {
      background-color: #C46ED6;
      color: #ffffff;
    }
    }

    </style>'''

    st.markdown(css, unsafe_allow_html=True)

    def member_select(select_name):
        for i in member_list:
            if select_name == i['name']:
                return i['code']

    select_name = st.radio('选择成员', [
        '乃木坂46', '五百城茉央', '池田瑛紗', '一ノ瀬美空', '伊藤理々杏', '井上和', '岩本蓮加', '梅澤美波', '遠藤さくら',
        '岡本姫奈', '小川彩', '奥田いろは', '賀喜遥香', '金川紗耶', '川﨑桜', '久保史緒里', '黒見明香', '佐藤楓',
        '佐藤璃果', '柴田柚菜', '菅原咲月', '田村真佑', '筒井あやめ', '冨里奈央', '中西アルノ', '中村麗乃', '林瑠奈',
        '松尾美佑', '向井葉月', '矢久保美緒', '弓木奈於', '吉田綾乃クリスティー', '与田祐希', '運営スタッフ', '3期生', '4期生',
        '新4期生', '5期生'], horizontal=True)

    st_ = st.number_input('请输入页码', value=1)

    if st_ == 0:
        st.warning('请输入正确页码！')

    def member_blog(code):
        member_headers = {
            'authority': 'www.nogizaka46.com',
            'accept': '*/*',
            'accept-language': 'ja,zh;q=0.9,zh-CN;q=0.8,ko;q=0.7,en;q=0.6,tr;q=0.5',
            'cookie': 'WAPID=9ulLdh0k9EgQ2fqvv8frLAf9A6v8Qx9kvme; wap_last_event=showWidgetPage; __td_signed=true; _ts_yjad=1643978843049; _fbp=fb.1.1643978843522.760024492; wovn_selected_lang=ja; _fbc=fb.1.1660921246855.IwAR3JBuS09qKl5C5hGlFnmSvXq4Zp1UBYNH_zuXsNk5yzQubh8zVPK7ULUnw; wap_last_event=showWidgetPage; _ga_R9MY5W6HJK=GS1.1.1673455267.2.1.1673455671.0.0.0; wovn_uuid=xz0kgt10x; _ga_FTL2JTLQ27=deleted; _ga_FTL2JTLQ27=deleted; WAPID=zbl5hvXIQwg48mEfUhnzZ36b55AyFHubOJy; _gcl_au=1.1.1700913064.1683221336; auth_tkn_nogizaka46.com=Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODY2NzM2OTAsImlhdCI6MTY4NDA4MTY5MCwibmJmIjowLCJzdWIiOiI3NjAwNTU0NzQxNDkxMzEzMTEiLCJpc3MiOiJmZW5zaS1pZC1ub2dpemFrYS1tb2JpbGUiLCJhdWQiOiJmZW5zaS1pZC1ub2dpemFrYS1tb2JpbGUifQ.yKCuEK_VaX_L8xZV0XDgPOPHr7jIsba_JHwK2LKzV-_LZOk1OwDSlsUa8faScViPpsu5qXmFfjFu4BRnOjsPsg; _ga_MQH5407CPF=GS1.1.1684659932.4.0.1684659932.0.0.0; __utmz=174951741.1685186281.336.16.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=174951741; _gid=GA1.2.303585636.1685585526; _td=c9a818f0-f0bc-49c7-8ba3-fe709ff29867; _ga=GA1.2.1489452597.1643978843; _ga_FTL2JTLQ27=GS1.1.1685599011.151.0.1685599011.0.0.0; _gat=1; __utma=174951741.1489452597.1643978843.1685585525.1685599012.346; __utmt=1; __utmb=174951741.1.10.1685599012',
            'referer': f'https://www.nogizaka46.com/s/n46/artist/{code}?ima=3527',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        }

        if st_ == 1:
            st_page = 0
        else:
            st_page = int((st_ - 1) * 16)

        member_params = {
            'ct': f'{code}',
            'rw': '16',
            'st': f'{st_page}',
            'callback': 'res',
        }

        resp = requests.get('https://www.nogizaka46.com/s/n46/api/list/blog', params=member_params,
                            headers=member_headers)

        json_data = resp.content.decode().replace("res(", "")[:-2]

        member_blog_js = json.loads(json_data)

        member_blog_data = member_blog_js['data']

        member_blog_count = member_blog_js['count']

        i = 0
        try:
            for name in range(len(member_blog_data)):
                blog_title = member_blog_data[i]['title']
                member_name = member_blog_data[i]['name']
                update_date = member_blog_data[i]['date'][:16]
                list_img = member_blog_data[i]['img']
                blog_text = member_blog_data[i]['text']
                sidebar = st.sidebar
                if list_img == '/files/46/assets/img/blog/none.png':
                    list_img = list_img.replace('/files/46/assets/img/blog/none.png',
                                                'https://www.nogizaka46.com/files/46/assets/img/blog/none.png')
                if '/files/' in blog_text:
                    blog_text = blog_text.replace('/files/', 'https://www.nogizaka46.com/files/').replace('.jpg"',
                                                                                                          '.jpg" style="width: 100%;height: 50%;"')
                if '/images/' in blog_text:
                    blog_text = blog_text.replace('/images/', 'https://www.nogizaka46.com/images/').replace('.jpg"',
                                                                                                            '.jpg" style="width: 100%;height: 50%;"')

                st.markdown(
                    f'<div id="container"><div class="card"><img class="list_img" src="{list_img}"><div class="blog_title">{blog_title}</div><div class="info-container"><div class="member_name">{member_name}</div>&nbsp<div class="update_date">{update_date}</div></div></div>',
                    unsafe_allow_html=True)

                @st.dialog(f'{blog_title}', width='large')
                def blog_viewer():
                    st.write(
                        f'<div class="member_name">{member_name}</div>&nbsp<div class="update_date">{update_date}</div><br><br><br>' + blog_text,
                        unsafe_allow_html=True)
                    
                    
                if st.button('查看BLOG', key=i):
                    blog_viewer()
                    # if sidebar.button('关闭'):
                    #     sidebar.empty()

                i += 1
        except IndexError:
            pass

    def all_blog():
        st_num = int((st_ - 1) * 32)

        params = {
            'ima': '1116',
            'rw': '32',
            'st': f'{st_num}',
            'callback': 'res',
        }

        response = requests.get('https://www.nogizaka46.com/s/n46/api/list/blog', params=params, headers=headers)

        if response.status_code == 200:

            json_data = response.content.decode().replace("res(", "")[:-2]

            data_js = json.loads(json_data)

            data = data_js['data']

            # blog列表
            i = 0

            try:
                for name in range(32):
                    blog_title = data[i]['title']
                    member_name = data[i]['name']
                    update_date = data[i]['date'][:16]
                    list_img = data[i]['img']
                    blog_text = data[i]['text']
                    if list_img == '/files/46/assets/img/blog/none.png':
                        list_img = list_img.replace('/files/46/assets/img/blog/none.png',
                                                    'https://www.nogizaka46.com/files/46/assets/img/blog/none.png')
                    sidebar = st.sidebar
                    if '/files/' in blog_text:
                        blog_text = blog_text.replace('/files/', 'https://www.nogizaka46.com/files/').replace('.jpg"',
                                                                                                              '.jpg" style="width: 100%;height: 50%;"')
                    if '/images/' in blog_text:
                        blog_text = blog_text.replace('/images/', 'https://www.nogizaka46.com/images/').replace('.jpg"',
                                                                                                                '.jpg" style="width: 100%;height: 50%;"')

                    st.markdown(
                        f'<div id="container"><div class="card"><img class="list_img" src="{list_img}"><div class="blog_title">{blog_title}</div><div class="info-container"><div class="member_name">{member_name}</div>&nbsp<div class="update_date">{update_date}</div></div></div>',
                        unsafe_allow_html=True)

                    @st.dialog(f'{blog_title}', width='large')
                    def blog_viewer():
                        st.write(
                            f'<div class="member_name">{member_name}</div>&nbsp<div class="update_date">{update_date}</div><br><br><br>' + blog_text,
                            unsafe_allow_html=True)

                    if st.button('查看BLOG', key=i):
                        blog_viewer()

                        # sidebar.write(
                        #     f'<div class="member_name">{member_name}</div>&nbsp<div class="update_date">{update_date}</div><br><br><br>' + blog_text,
                        #     unsafe_allow_html=True)
                        # if sidebar.button('关闭'):
                        #     sidebar.empty()

                    i += 1
            except IndexError:
                pass

    if select_name == '乃木坂46':
        all_blog()
    if member_select(select_name):
        member_blog(member_select(select_name))


def news_catch():
    st.markdown("""<a name="top"></a>""", unsafe_allow_html=True)
    st.write("""<head><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4156995100078455"
         crossorigin="anonymous"></script></head>""", unsafe_allow_html=True)

    news_url = st.text_input(label='请输入网址,图片在侧边栏 ')
    st.caption(
        '*目前支持 MDPR | 日刊Sports | Oricon news | Mantan-Web | らじらー blog | Bubka Web | NBpress | natalie | Thetv | Realsound *')

    def zip_download(news_title, image_list_group):
        if st.button("下载图片"):
            st.info('请稍等,正在将图片处理至压缩包')
            zip_filename = create_zip(sanitize_filename(news_title), image_list_group)
            with open(zip_filename, "rb") as f:
                bytes_data = f.read()
            st.success('压缩完整,请点击下载')
            st.download_button(label="点击下载", data=bytes_data, file_name=zip_filename)

    def nikkansports(news_url):
        if '/photonews/photonews_nsInc_' in news_url:
            news_url = news_url.replace(news_url,
                                        f'https://www.nikkansports.com/{re.findall("https://www.nikkansports.com/(.*?)/photonews/photonews", news_url)[0]}/news/{re.findall("photonews/photonews_nsInc_([0-9+]*)", news_url)[0]}.html')

        resp = requests.get(
            news_url,
        ).text

        img_list = []

        article_title = re.findall(r'<title>(.*?)</title>', resp, re.S)[0]
        i = 0
        for item in resp:
            imgs = re.findall('<meta name="nsPicture" content="(.*?)">', resp)
            for img in imgs:
                orig_imgs = imgs[i].replace('w500', 'w1300')
                i += 1
                img_list.append(orig_imgs)
            break

        st.caption(f'图片数量: {len(img_list)}')

        zip_download(article_title, img_list)

        # if st.button("下载图片"):
        #     st.info('请稍等,正在将图片处理至压缩包')
        #     zip_filename = create_zip(article_title, img_list)
        #     with open(zip_filename, "rb") as f:
        #         bytes_data = f.read()
        #     st.success('压缩完整,请点击下载')
        #     st.download_button(label="点击下载", data=bytes_data, file_name=zip_filename)

        st.subheader(article_title)

        img_contnt = '<div style="display:inline">'
        for pic in img_list:
            img_contnt += f'''<img src='{pic}' width="30%">'''
        st.markdown(img_contnt, unsafe_allow_html=True)

    def oricon(url):
        url_new = ''
        if 'full' not in url:
            url_new = f'{url}/full/'
        if 'full' not in url and len(url) > 38:
            url_new = f'{url[:38]}/full/'
        resp = requests.get(url_new).text
        # 文章标题
        article_title = re.findall('<title>(.*?)</title>', resp, re.S)[0]
        st.subheader(article_title)

        # 图片
        img_re = re.findall('div class="unit-photo-preview"><h2 class="title">関連写真</h2>(.*?)</div>', resp, re.S)

        # 输出页面部分

        if 'この記事の写真を見る' in resp:
            pic_num = None
            pic_num_find = re.findall('この記事の写真を見る（全(.*?)枚）', resp)
            if pic_num_find:
                pic_num = pic_num_find[0]
            photo_url = f'{url_new.replace("full/", "")}photo/1/'

            photo_url_resp = requests.get(photo_url).text
            soup = BeautifulSoup(photo_url_resp, 'html.parser')

            # 找到<div class="photo_slider" id="photo_slider_box">元素
            photo_slider_div = soup.find('div', class_='photo_slider', id='photo_slider_box')

            # 在<div>元素中查找所有带有href属性的<a>标签
            href_tags = photo_slider_div.find_all('a', href=True)

            # 创建一个空的链接列表
            link_list = []

            # 提取所有的链接地址并添加到列表中
            for tag in href_tags:
                link_list.append(f"https://www.oricon.co.jp{tag['href']}")

            i = 0
            img_list = []
            for link in range(len(link_list)):
                # 请求每个link
                link_resp = requests.get(link_list[i]).text
                # 找到每个link里面所有的原图
                og_img = re.findall('<meta property="og:image" content="(.*?)">', link_resp, re.S)
                if og_img:
                    og_img = og_img[0].replace('width=1200,quality=85,', '')
                # 把图片链接放入图片列表
                img_list.append(og_img)
                i += 1
            st.caption(f'图片数量： {len(img_list)}')
            zip_download(article_title, img_list)
            x = 0
            img_contnt = '<div style="display:inline">'
            for img in range(len(img_list)):
                pic = img_list[x]
                img_contnt += f'''<img src='{pic}' width="50%">'''
                x += 1
            st.markdown(img_contnt, unsafe_allow_html=True)

        if 'この記事の写真を見る' not in resp and '関連写真' not in resp:

            img = ''.join(re.findall('<!--StartText-->(.*?)<!--EndText-->', resp, re.S))
            img_urls = re.findall('<a\\s+[^>]*href="([^"]*photo[^"]*)"[^>]*>', img)
            i = 0
            img_list = []
            for url in img_urls:
                if 'photo' in url:
                    img_url = img_urls[i]
                    ori_resp = requests.get(img_url).text
                    og_imgs = re.findall('<meta property="og:image" content="(.*?)">', ori_resp)
                    i += 1

                    for pic in og_imgs:
                        og_img = pic.replace('cdn-cgi/image/width=1200,quality=85,format=auto/', '')
                        img_list.append(og_img)

            st.caption(f'图片数量： {len(img_list)}')
            zip_download(article_title, img_list)
            x = 0
            img_contnt = '<div style="display:inline">'
            for img in range(len(img_list)):
                pic = img_list[x]
                img_contnt += f'''<img src='{pic}' width="30%">'''
                x += 1
            st.markdown(img_contnt, unsafe_allow_html=True)

        if 'この記事の写真を見る' not in resp and '関連写真' in resp:
            img_url = re.findall('<a href="(.*?)">', ''.join(img_re))

            og_list = []

            i = 0
            for pic in img_url:
                ori_url = img_url[i]
                ori_resp = requests.get(ori_url).text
                og_imgs = re.findall('<meta property="og:image" content="(.*?)">', ori_resp)
                for pic in og_imgs:
                    og_img = pic.replace('cdn-cgi/image/width=1200,quality=85,format=auto/', '')
                    i += 1
                    og_list.append(og_img)

            st.caption(f'图片数量： {len(og_list)}')
            zip_download(article_title, og_list)
            x = 0
            img_contnt = '<div style="display:inline">'
            for img in range(len(og_list)):
                pic = og_list[x]
                img_contnt += f'''<img src='{pic}' width="30%">'''
                x += 1
            st.markdown(img_contnt, unsafe_allow_html=True)

    def mantan(url):

        mantan_app = mantan_web(url)

        title, images_list = mantan_app.get_page_info()

        st.caption(f'图片数量: {len(images_list)}')
        zip_download(title, images_list)

        st.subheader(title)

        img_contnt = '<div style="display:inline">'
        for img in range(len(images_list)):
            img_contnt += f'''<img src='{img}' width="50%">'''
        st.markdown(img_contnt, unsafe_allow_html=True)

    def mdpr(url):
        mdpr_headers = {
            'referer': f'{url}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }

        if 'photo' not in url and 'mdpr.jp' in url:
            mdpr_resp = requests.get(url, headers=mdpr_headers).text
            mdpr_photo_url = re.findall('<a class="c-image__image" href="(.*?)" >', mdpr_resp)[0]
            url = f'https://mdpr.jp{mdpr_photo_url}'
        if "photo" in url:
            url = url
        mdpr_photo_resp = requests.get(url, headers=mdpr_headers).text
        # 标题
        mdpr_arti_title = re.findall('<h1 class="p-articleHeader__title">(.*?)</h1>', mdpr_photo_resp)[0]

        soup = BeautifulSoup(mdpr_photo_resp, 'html.parser')

        img_list = re.findall('<img src="(.*?)" alt=".*" width="125"', mdpr_photo_resp)
        i = 0
        x = 1
        st.caption(f'图片数量：{len(img_list) + 1}')
        i = 0
        new_image_list = []
        # 获取头图
        imageWrapper = soup.find('img', {'class': 'c-image__image'}).get('src').split('?')[0]

        new_image_list.append(imageWrapper)
        img_contnt = '<div style="display:inline">'
        for img in range(len(img_list)):
            pic = img_list[i].split('?')[0]
            new_image_list.append(pic)
            img_contnt += f'''<img src='{pic}' width="30%">'''
            i += 1

        zip_download(mdpr_arti_title, new_image_list)

        st.subheader(mdpr_arti_title, anchor='title')

        # 图片展示
        st.markdown(f"""<div><img src='{imageWrapper}' width="30%"></div>""", unsafe_allow_html=True)

        st.markdown(img_contnt, unsafe_allow_html=True)

    def rajira_blog(url):
        title, image_urls = rajira(url)
        # 创建压缩文件并下载
        zip_download(title, image_urls)
        st.title(title)
        i = 0
        img_contnt = '<div style="display:inline">'
        for img in range(len(image_urls)):
            pic = image_urls[i]
            img_contnt += f'''<img src='{pic}' width="30%">'''
            i += 1
        st.markdown(img_contnt, unsafe_allow_html=True)

    def bubka(url):
        bubka_app = bubka_web(url)
        title, images_list = bubka_app.get_image_urls()
        image_count = len(images_list)
        st.caption(f'图片数量: {image_count}')

        zip_download(title, images_list)
        st.subheader(title)
        img_contnt = '<div style="display:inline">'
        i = 0
        for img in range(len(images_list)):
            pic = images_list[i]
            img_contnt += f'''<img src='{pic}' width="30%">'''
            i += 1
        st.markdown(img_contnt, unsafe_allow_html=True)

    def nbpress(url):
        app = nbpress_web(url)
        title, gallery_image_groups = app.get_gallery_image_groups()
        image_count = len(gallery_image_groups)
        st.caption(f'图片数量: {image_count}')

        zip_download(title, gallery_image_groups)

        st.subheader(title)
        img_contnt = '<div style="display:inline">'
        i = 0
        for img in range(len(gallery_image_groups)):
            pic = gallery_image_groups[i]
            img_contnt += f'''<img src='{pic}' width="30%">'''
            i += 1
        st.markdown(img_contnt, unsafe_allow_html=True)

    def natalie(url):
        app = natalie_web(url)
        title, gallery_image_groups = app.get_gallery_image_groups()
        if not gallery_image_groups or not title:
            st.warning('该页面没有图片/代码异常')
        else:
            image_count = len(gallery_image_groups)
            st.caption(f'图片数量: {image_count}')

            zip_download(title, gallery_image_groups)
            st.subheader(title)
            img_contnt = '<div style="display:inline">'
            i = 0
            for img in range(len(gallery_image_groups)):
                pic = gallery_image_groups[i]
                img_contnt += f'''<img src='{pic}' width="30%">'''
                i += 1
            st.markdown(img_contnt, unsafe_allow_html=True)

    def thetv(url):
        app = thetv_web(url)
        title, image_count, gallery_image_groups = app.get_gallery_info()
        if not any([title, image_count, gallery_image_groups]):
            st.warning('该页面没有图片/代码异常')
        else:
            st.caption(f'图片数量: {image_count}')
            zip_download(title, gallery_image_groups)
            st.subheader(title)
            img_contnt = '<div style="display:inline">'
            i = 0
            for img in range(len(gallery_image_groups)):
                pic = gallery_image_groups[i]
                img_contnt += f'''<img src='{pic}' width="30%">'''
                i += 1
            st.markdown(img_contnt, unsafe_allow_html=True)

    def realsound(url):
        app = realsound_web(url)
        title, gallery_image_groups = app.get_image_info()
        if not any([title, gallery_image_groups]):
            st.warning('该页面没有图片/代码异常')
        else:
            image_count = len(gallery_image_groups)
            st.caption(f'图片数量: {image_count}')
            zip_download(title, gallery_image_groups)
            st.subheader(title)
            img_contnt = '<div style="display:inline">'
            i = 0
            for img in range(len(gallery_image_groups)):
                pic = gallery_image_groups[i]
                img_contnt += f'''<img src='{pic}' width="30%">'''
                i += 1
            st.markdown(img_contnt, unsafe_allow_html=True)

    if 'nikkansports' in news_url:
        nikkansports(news_url)
    if 'oricon' in news_url:
        oricon(news_url)
    if 'mantan' in news_url:
        mantan(news_url)
    if 'mdpr' in news_url:
        mdpr(news_url)
    if 'www.nhk.jp/p/radirer/' in news_url:
        rajira_blog(news_url)
    if 'idol-culture.jp' in news_url:
        bubka(news_url)
    if 'nbpress.online' in news_url:
        nbpress(news_url)
    if 'natalie.mu' in news_url:
        natalie(news_url)
    if 'thetv.jp' in news_url:
        thetv(news_url)
    if 'realsound.jp' in news_url:
        realsound(news_url)

    if news_url == '':
        pass
    else:
        st.markdown(
            """<a href="#top" style="text-decoration:none;border-radius:30px;padding: 10px 10px 10px 10px;display:block;margin:5px 5px 5px 5px;background-color:#9e3eb2;color:white;text-align:center;">返回顶部</a>""",
            unsafe_allow_html=True)


def schedule():
    col1, col2, col3 = st.columns([1, 2, 3], gap='medium')
    cate_info = {
        '': '',
        "live": "ライブ/イベント",
        "meet": "握手会",
        "tv": "TV",
        "radio": "ラジオ",
        "book": "書籍",
        "web": "WEB",
        "movie": "映画",
        "musical": "舞台/ミュージカル",
        "release": "リリース",
        "birthday": "誕生日",
        "other": "その他"
    }
    cate_value = []
    cate_key = ''
    for cate_value in cate_info:
        cate_value = cate_info.values()

    with col2:
        schedule_toggle = st.toggle('按月份查看日程')
        schedule_option = st.selectbox('选择类别', cate_value)
        if schedule_option != '' and schedule_option in cate_value:
            for key, value in cate_info.items():
                if value == schedule_option:
                    cate_key = key
        date_sel = st.date_input('选择日程日期,默认查看当天的日程', datetime)

    with col3:

        schedule_headers = {
            'authority': 'www.nogizaka46.com',
            'accept': '*/*',
            'accept-language': 'ja,zh;q=0.9,zh-CN;q=0.8,ko;q=0.7,en;q=0.6,tr;q=0.5',
            'cookie': 'WAPID=9ulLdh0k9EgQ2fqvv8frLAf9A6v8Qx9kvme; __td_signed=true; _ts_yjad=1643978843049; _fbp=fb.1.1643978843522.760024492; wovn_selected_lang=ja; _fbc=fb.1.1660921246855.IwAR3JBuS09qKl5C5hGlFnmSvXq4Zp1UBYNH_zuXsNk5yzQubh8zVPK7ULUnw; wap_last_event=showWidgetPage; _ga_R9MY5W6HJK=GS1.1.1673455267.2.1.1673455671.0.0.0; wovn_uuid=xz0kgt10x; _ga_FTL2JTLQ27=deleted; _ga_FTL2JTLQ27=deleted; WAPID=zbl5hvXIQwg48mEfUhnzZ36b55AyFHubOJy; _yjsu_yjad=1694868548.e0d068f0-15a2-4ea1-a2a8-4951c0cb4d63; _tt_enable_cookie=1; _ttp=N_SHHjlbfeGE97MJr1zC0WuHRR9; _ga_MQH5407CPF=GS1.1.1696987717.8.1.1696987994.0.0.0; __utmz=174951741.1698596854.460.30.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _gcl_au=1.1.694657561.1699162597; _gid=GA1.2.44276891.1699336932; __utma=174951741.1489452597.1643978843.1699535065.1699583784.471; __utmc=174951741; __utmt=1; _ga_CYV9VQHJ8W=GS1.2.1699583784.64.0.1699583784.60.0.0; _ga_HRQHK75P9N=GS1.2.1699583784.99.0.1699583784.0.0.0; _gat=1; __utmb=174951741.2.10.1699583784; _dc_gtm_UA-70388113-2=1; _dc_gtm_UA-70385727-1=1; _dc_gtm_UA-70441218-30=1; _ga=GA1.1.1489452597.1643978843; _td=c9a818f0-f0bc-49c7-8ba3-fe709ff29867; _ga_FTL2JTLQ27=GS1.1.1699583784.344.1.1699584304.59.0.0',
            'referer': 'https://www.nogizaka46.com/',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        }

        date_num = str(date_sel).replace('-', '')
        if schedule_toggle:
            date_num = str(date_sel).replace('-', '')[:6]

        schedule_params = {
            'dy': f'{date_num}',
            'callback': 'res',
            'ct': f'{cate_key}',
        }
        response = requests.get('https://www.nogizaka46.com/s/n46/api/list/schedule', headers=schedule_headers,
                                params=schedule_params)

        if response.status_code == 200:
            # 提取有效的 JSON 数据
            json_data = response.content.decode().replace("res(", "")[:-2]

            # 将 JSON 数据转换为 Python 字典对象
            data = json.loads(json_data)

            if not data['data']:
                st.warning('选择的类别/日期暂无日程')

            # 按月显示开关打开
            if schedule_toggle:
                date_dict = {}
                for item in data['data']:
                    cate = cate_info.get(item['cate'], "N/A")
                    title = item['title']
                    link = item['link']
                    cate_date = item['date']
                    if cate_date in date_dict:
                        date_dict[cate_date].append(
                            (cate, title, link, item.get('start_time', ''), item.get('end_time', '')))
                    else:
                        date_dict[cate_date] = [
                            (cate, title, link, item.get('start_time', ''), item.get('end_time', ''))]

                for date, schedules in date_dict.items():
                    st.info(f"{date}")
                    st.write('<div style="padding-top:0"></div>', unsafe_allow_html=True)
                    for schedule in schedules:
                        if schedule[0] in ['radio', 'tv', 'web']:
                            start_time = schedule[3] if schedule[3] else ''
                            end_time = schedule[4] if schedule[4] else ''
                            schedule_text = f'<font size=1><font style="border-radius:25px;border:1px solid #AD00E5;padding:3px;">{schedule[0]}</font><font color=#9e3eb2> **{start_time}~{end_time}** </font>| <a href="{schedule[2]}" style="text-decoration:none;color:#9e3eb2;">{schedule[1]}</a></font>'
                            st.write(schedule_text, unsafe_allow_html=True)
                        else:
                            schedule_text = f'<font size=1><font style="border-radius:25px;border:1px solid #AD00E5;padding:3px;">{schedule[0]}</font>  <a href="{schedule[2]}" style="text-decoration:none;color:#9e3eb2;"><font size=2>{schedule[1]}</font></a></font>'
                            st.write(schedule_text, unsafe_allow_html=True)
            # 按月显示开关关闭
            if not schedule_toggle:
                for item in data['data']:
                    cate = cate_info.get(item['cate']) if cate_info.get(item['cate']) else "N/A"
                    title = item['title']
                    link = item['link']
                    start_time = []
                    end_time = []
                    cate_date = item['date']
                    if item['cate'] == 'radio' or item['cate'] == 'tv' or item['cate'] == 'web':
                        start_time = item['start_time']
                        end_time = item['end_time']
                        schedule_text = '<font size=1><font style="border-radius:25px;border:1px solid #AD00E5;padding:3px;">{}</font><font color=#9e3eb2> **{}~{}** </font>| <a href="{}" style="text-decoration:none;color:#9e3eb2;">{}</a></font>'.format(
                            cate, start_time, end_time, link, title)
                        st.write(schedule_text, unsafe_allow_html=True)
                    else:
                        schedule_text = '<font size=1><font style="border-radius:25px;border:1px solid #AD00E5;padding:3px;">{}</font>  <a href="{}" style="text-decoration:none;color:#9e3eb2;"><font size=2>{}</font></a></font>'.format(
                            cate, link, title)
                        st.write(schedule_text, unsafe_allow_html=True)


selected1 = option_menu(None, ['乃木坂46日程', "乃木坂46新闻", "成员Blog", "新闻抓图", ],
                        icons=['calendar3', 'newspaper', 'book', "search", ],
                        menu_icon="cast", default_index=0, orientation="horizontal",
                        styles={
                            'icon': {"color": "#ec92ff"},
                            'nav-link': {"color": "#9e3eb2", "--hover-color": "#ffffff"},
                            "nav-link-selected": {"background-color": "#9e3eb2", 'color': 'white'},
                        })

if selected1 == "乃木坂46日程":
    schedule()
if selected1 == "乃木坂46新闻":
    get_news()
if selected1 == "成员Blog":
    blog()
if selected1 == "新闻抓图":
    news_catch()
