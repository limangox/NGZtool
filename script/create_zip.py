import zipfile
import requests

# 定义函数来创建压缩文件
def create_zip(title, image_urls):
    zip_filename = f"{title}.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for image_url in image_urls:
            # 发送请求获取图片数据
            response = requests.get(image_url)
            if response.status_code == 200:
                # 从 URL 中提取文件名
                filename = image_url.split('/')[-1]
                # 将图片数据写入压缩文件
                zipf.writestr(filename, response.content)
    return zip_filename
