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
from script.get_rajira_blog import get_rajira_blog

st.set_page_config(page_title="N46综合", layout="wide")

tz = timezone(timedelta(hours=9))
datetime = datetime.datetime.now(tz)


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
                   {'name': '岡本 姫奈', 'cate': '5期生', 'code': '55401'},
                   {'name': '川﨑 桜', 'cate': '5期生', 'code': '55400'},
                   {'name': '池田 瑛紗', 'cate': '5期生', 'code': '55397'},
                   {'name': '五百城 茉央', 'cate': '5期生', 'code': '55396'},
                   {'name': '中西 アルノ', 'cate': '5期生', 'code': '55395'},
                   {'name': '奥田 いろは', 'cate': '5期生', 'code': '55394'},
                   {'name': '冨里 奈央', 'cate': '5期生', 'code': '55393'},
                   {'name': '小川 彩', 'cate': '5期生', 'code': '55392'},
                   {'name': '菅原 咲月', 'cate': '5期生', 'code': '55391'},
                   {'name': '井上 和', 'cate': '5期生', 'code': '55389'},
                   {'name': '弓木 奈於', 'cate': '4期生', 'code': '55387'},
                   {'name': '松尾 美佑', 'cate': '4期生', 'code': '55386'},
                   {'name': '林 瑠奈', 'cate': '4期生', 'code': '55385'},
                   {'name': '佐藤 璃果', 'cate': '4期生', 'code': '55384'},
                   {'name': '黒見 明香', 'cate': '4期生', 'code': '55383'},
                   {'name': '清宮 レイ', 'cate': '4期生', 'code': '48014'},
                   {'name': '北川 悠理', 'cate': '4期生', 'code': '48012'},
                   {'name': '金川 紗耶', 'cate': '4期生', 'code': '48010'},
                   {'name': '矢久保 美緒', 'cate': '4期生', 'code': '48019'},
                   {'name': '早川 聖来', 'cate': '4期生', 'code': '48018'},
                   {'name': '掛橋 沙耶香', 'cate': '4期生', 'code': '48009'},
                   {'name': '賀喜 遥香', 'cate': '4期生', 'code': '48008'},
                   {'name': '筒井 あやめ', 'cate': '4期生', 'code': '48017'},
                   {'name': '田村 真佑', 'cate': '4期生', 'code': '48015'},
                   {'name': '柴田 柚菜', 'cate': '4期生', 'code': '48013'},
                   {'name': '遠藤 さくら', 'cate': '4期生', 'code': '48006'},
                   {'name': '与田 祐希', 'cate': '3期生', 'code': '36760'},
                   {'name': '吉田 綾乃クリスティー', 'cate': '3期生', 'code': '36759'},
                   {'name': '山下 美月', 'cate': '3期生', 'code': '36758'},
                   {'name': '向井 葉月', 'cate': '3期生', 'code': '36757'},
                   {'name': '中村 麗乃', 'cate': '3期生', 'code': '36756'},
                   {'name': '佐藤 楓', 'cate': '3期生', 'code': '36755'},
                   {'name': '阪口 珠美', 'cate': '3期生', 'code': '36754'},
                   {'name': '久保 史緒里', 'cate': '3期生', 'code': '36753'}]

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

    select_name = st.selectbox('选择成员', (
        '乃木坂46', '与田 祐希', '吉田 綾乃クリスティー', '山下 美月', '向井 葉月', '中村 麗乃', '佐藤 楓', '阪口 珠美',
        '久保 史緒里', '弓木 奈於', '松尾 美佑', '林 瑠奈', '佐藤 璃果', '黒見 明香', '清宮 レイ', '北川 悠理',
        '金川 紗耶',
        '矢久保 美緒', '早川 聖来', '掛橋 沙耶香', '賀喜 遥香', '筒井 あやめ', '田村 真佑', '柴田 柚菜', '遠藤 さくら',
        '岡本 姫奈',
        '川﨑 桜', '池田 瑛紗', '五百城 茉央', '中西 アルノ', '奥田 いろは', '冨里 奈央', '小川 彩', '菅原 咲月', '井上 和'))

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
                if st.button('查看BLOG', key=i):
                    sidebar.write(
                        f'<div class="member_name">{member_name}</div>&nbsp<div class="update_date">{update_date}</div><br><br><br>' + blog_text,
                        unsafe_allow_html=True)
                    if sidebar.button('关闭'):
                        sidebar.empty()

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
                    if st.button('查看BLOG', key=i):
                        sidebar.write(
                            f'<div class="member_name">{member_name}</div>&nbsp<div class="update_date">{update_date}</div><br><br><br>' + blog_text,
                            unsafe_allow_html=True)
                        if sidebar.button('关闭'):
                            sidebar.empty()

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
    st.caption('*目前支持 MDPR | 日刊Sports | Oricon news | Mantan-Web | らじらー blog*')

    def nikkansports(news_url):
        if '/photonews/photonews_nsInc_' in news_url:
            news_url = news_url.replace(news_url,
                                        f'https://www.nikkansports.com/{re.findall("https://www.nikkansports.com/(.*?)/photonews/photonews", news_url)[0]}/news/{re.findall("photonews/photonews_nsInc_([0-9+]*)", news_url)[0]}.html')

        resp = requests.get(
            news_url,
        ).text

        i = 0

        imgs = []
        orig_imgs = []
        article_title = re.findall(r'<title>(.*?)</title>', resp, re.S)[0]
        st.subheader(article_title)

        for pic in resp:
            imgs = re.findall('<meta name="nsPicture" content="(.*?)">', resp)
            for pic in imgs:
                orig_imgs = imgs[i].replace('w500', 'w1300')
                st.sidebar.image(orig_imgs, width=300)
                i += 1
            break
        if 'entertainment/column/sakamichi' in news_url:
            soup = BeautifulSoup(resp, 'html.parser')

            news_div = soup.find('div', {'id': 'news'})
            p_tags = news_div.find_all('p')

            article_text = ''
            for p in p_tags:
                article_text += str(p)

        else:
            article_text = re.findall(r'<div id="news" class="article-body ">(.*?)</div>', resp, re.S)[0]
        st.markdown(article_text, unsafe_allow_html=True)

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

        # 文章正文
        article_text1 = re.sub(re.compile(r'<.*?>'), '',
                               re.findall('<!--StartText-->(.*?)<!--EndText-->', resp, re.S)[0])

        # 第一种 script
        script1 = re.findall(r'<div .*?>+<script>(.*?)</script></div>+', resp)

        # 移除第一种 script
        for script in script1:
            article_text1 = article_text1.replace(script, '')

        # 第二种 script
        pattern = r"googletag\.cmd\.push\(function\(\) \{[^\}]*\}\);"
        matches = re.findall(pattern, article_text1)

        # 移除第二种 script
        for script2 in matches:
            article_text1 = article_text1.replace(script2, '')

        # 第三种 script
        pattern = r'<div class="gmossp_core_g939027">\s*<script>(.*?)</script>\s*</div>'
        match = re.search(pattern, resp, re.DOTALL)

        # 如果找到匹配项，提取 <script> 内容并移除
        if match:
            script3 = match.group(1)
            article_text1 = article_text1.replace(script3, '')

        # 输出提取的正文内容
        st.markdown(article_text1.strip(), unsafe_allow_html=True)

        # 图片
        img_re = re.findall('div class="unit-photo-preview"><h2 class="title">関連写真</h2>(.*?)</div>', resp, re.S)

        # 输出页面部分

        if 'この記事の写真を見る' in resp:
            pic_num = re.findall('この記事の写真を見る（全(.*?)枚）', resp)[0]
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
            x = 0
            img_contnt = '<div style="display:inline">'
            for img in range(len(img_list)):
                pic = img_list[x]
                img_contnt += f'''<img src='{pic}' width="50%">'''
                x += 1
            st.markdown(img_contnt, unsafe_allow_html=True)

        if 'この記事の写真を見る' not in resp and '関連写真' not in resp:

            img = ''.join(re.findall('<!--StartText-->(.*?)<!--EndText-->', resp, re.S))
            img_urls = re.findall('<a\s+[^>]*href="([^"]*photo[^"]*)"[^>]*>', img)
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
            x = 0
            img_contnt = '<div style="display:inline">'
            for img in range(len(og_list)):
                pic = og_list[x]
                img_contnt += f'''<img src='{pic}' width="30%">'''
                x += 1
            st.markdown(img_contnt, unsafe_allow_html=True)

    def mantan(url):
        global img_url
        global url_article
        if 'gravure' in url and 'photo' not in url:
            img_url = url.replace('.html', '/photopage/001.html')
            url_article = url
        if 'photo' not in url:
            img_url = url.replace('.html', '/photopage/001.html')
            url_article = url
        if 'photo' in url:
            img_url = url
            url_article = img_url.replace('/photopage/001.html', '.html')

        headers = {
            'referer': 'https://mantan-web.jp',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }

        # 文字部分
        resp = requests.get(url_article, headers=headers)
        resp.encoding = 'utf-8'  # 指定UTF-8编码
        html_content = resp.text

        pattern = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)
        matches = pattern.findall(html_content)
        if matches:
            # 对匹配到的内容进行解码
            script_content = matches[0]

            # 提取headline字段的内容
            headline_pattern = re.compile(r'"headline"\s*:\s*"(.*?)"')
            headline_match = headline_pattern.search(script_content)

            if headline_match:
                article_title = headline_match.group(1)
                st.subheader(article_title)

        soup = BeautifulSoup(html_content, 'html.parser')
        # 文章部分
        all_p_tags = soup.find_all('p', class_='article__text')
        result_text = '<br></br>'.join([p.get_text(strip=True) for p in all_p_tags])
        st.markdown(result_text, unsafe_allow_html=True)

        # 图片部分
        if 'gravure' in url:
            resp = requests.get(img_url, headers=headers)
            resp.encoding = 'utf-8'  # 指定UTF-8编码
            img_content = resp.text
            img_soup = BeautifulSoup(img_content, 'html.parser')

            # 获取图片所在链接
            url_list = []
            for div_tag in img_soup.find_all('div', class_='swiper-slide'):
                a_tag = div_tag.find('a')
                if a_tag:
                    href = a_tag.get('href')
                    url_list.append(href)
            # 获取图片链接
            img_list = []
            for url in url_list:
                photo_url = f'https://gravure.mantan-web.jp{url}'
                photo_url_resp = requests.get(photo_url, headers=headers).text
                img_soup = BeautifulSoup(photo_url_resp, 'html.parser')
                img_div = img_soup.find('div', class_='photo__photo--minh')
                if img_div:
                    # 查找div标签下的img标签
                    img_tag = img_div.find('img')

                    if img_tag:
                        img_src = img_tag.get('src')
                        img_list.append(img_src)

            i = 0
            img_contnt = '<div style="display:inline">'
            for img in range(len(img_list)):
                pic = img_list[i].split('?')[0]
                img_contnt += f'''<img src='{pic}' width="50%">'''
                i += 1
            st.markdown(img_contnt, unsafe_allow_html=True)

        # 没有gravure
        resp = requests.get(img_url, headers=headers)
        resp.encoding = 'utf-8'  # 指定UTF-8编码
        img_content = resp.text
        img_soup = BeautifulSoup(img_content, 'html.parser')

        script_content = []
        for script_tag in img_soup.find_all('script'):
            if 'var __images = JSON.parse' in script_tag.text:
                script_content = script_tag.text
                break
        img_list = []
        if script_content:
            # 使用正则表达式提取JSON内容部分
            json_match = script_content.split("('")[1].replace("')", '')
            list_ = json.loads(json_match)
            i = 0
            for img in list_:
                pic = list_[i]['src']
                img_list.append(pic)
                i += 1
        i = 0
        img_contnt = '<div style="display:inline">'
        for img in range(len(img_list)):
            pic = img_list[i].split('?')[0]
            img_contnt += f'''<img src='{pic}' width="50%">'''
            i += 1
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
        st.subheader(mdpr_arti_title, anchor='title')

        soup = BeautifulSoup(mdpr_photo_resp, 'html.parser')
        # 获取头图
        imageWrapper = soup.find('img', {'class': 'c-image__image'}).get('src').split('?')[0]

        img_list = re.findall('<img src="(.*?)" alt=".*" width="125"', mdpr_photo_resp)
        i = 0
        x = 1
        st.caption(f'图片数量：{len(img_list) + 1}')
        # 图片展示
        st.markdown(f"""<div><img src='{imageWrapper}' width="30%"></div>""", unsafe_allow_html=True)
        i = 0
        img_contnt = '<div style="display:inline">'
        for img in range(len(img_list)):
            pic = img_list[i].split('?')[0]
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
    if 'radirer' in news_url:
        get_rajira_blog(news_url)

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
