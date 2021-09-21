import requests


def downLoad(url, name):
    r = requests.get(url)
    #  状态码200代表请求成功
    if r.status_code == 200:
        open("D:\\pachong\\" + str(name) + ".jpg", "wb").write(r.content)
        print("第" + str(name) + "张图片下载完成")
    else:
        print("第" + str(name) + "张图片下载失败")
    r.close()

