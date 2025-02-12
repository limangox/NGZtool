import zipfile
import requests

# 定义函数来创建压缩文件
def create_zip(title, image_urls):
    zip_filename = f"{title}.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        # 使用 enumerate 以便为每个图片加上递增的编号
        for index, image_url in enumerate(image_urls, start=1):
            # 发送请求获取图片数据
            response = requests.get(image_url)
            if response.status_code == 200:
                # 从 URL 中提取文件名
                original_filename = image_url.split('/')[-1].split('?')[0]
                # 添加三位数的序号，格式为 "001_原始文件名"
                numbered_filename = f"{str(index).zfill(3)}_{original_filename}"
                # 将图片数据写入压缩文件
                zipf.writestr(numbered_filename, response.content)
    return zip_filename
