from script.create_zip import create_zip
from script.rajira_blog import rajira
import streamlit as st

def get_rajira_blog(url):
    title, image_urls = rajira(url)
    # 创建压缩文件并下载
    if st.button("下载图片"):
        st.info('请稍等,正在将图片处理至压缩包')
        zip_filename = create_zip(title, image_urls)
        with open(zip_filename, "rb") as f:
            bytes_data = f.read()
        st.success('压缩完整,请点击下载')
        st.download_button(label="点击下载", data=bytes_data, file_name=zip_filename)
    st.title(title)
    i = 0
    img_contnt = '<div style="display:inline">'
    for img in range(len(image_urls)):
        pic = image_urls[i]
        img_contnt += f'''<img src='{pic}' width="30%">'''
        i += 1
    st.markdown(img_contnt, unsafe_allow_html=True)
