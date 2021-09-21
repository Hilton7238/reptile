# -*- coding: UTF-8 -*-
import re  # 正则表达
import urllib.error  # url操作
import urllib.request

import pymysql
import xlwt
from bs4 import BeautifulSoup

# 编写基础的正则表达方便查找
from Movie import Movie
# 导入下载图片模块
import DownLoad

baseItem = re.compile(r'<span class="subject-rate>')
#  <img alt="黑寡妇" class="" src="https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2665872718.jpg" width="75"/>
findImg = re.compile(r'<img.*src="(.*)" .*/>')
'''
<a class="" href="https://movie.douban.com/subject/25828589/">
                        黑寡妇
                        / <span style="font-size:13px;">The Black Widow</span>
</a>
'''
findcName = re.compile(r'<a.*>\n(.+)\n.*<span.*>.*</span>\n</a>', re.S)
findeName = re.compile(r'.*<span .*>(.*)</span>\n</a>', re.S)
findUrl = re.compile(r'<a class="" href="(.*)">\n.+\n.*<span.*>.*</span>\n</a>', re.S)
#  <span class="pl">(76939人评价)</span>
findScore = re.compile(r'<span class="pl">.(\d+)人评价.</span>', re.S)

def getConnetion():
    return pymysql.connect(host="127.0.0.1", port=3306, database="movie", user="root", password="88888888", charset="utf8")


def main():
    baseurl = "https://movie.douban.com/chart"
    # 1.爬取网页获取数据
    data = getData(baseurl)
    # 2.存储数据在本地或数据库
    saveData(data)


def getData(baseurl):
    data = []
    html = askURL(baseurl)
    soup = BeautifulSoup(html, "html.parser")
    for item in (soup.find_all("table", class_="")):
        cName = str(re.findall(findcName, str(item))[0]).strip()  # 提取中文名并去掉空格
        eName = str(re.findall(findeName, str(item))[0])  # 提取英文名
        url = str(re.findall(findUrl, str(item))[0])  # 提取电影路径
        score = str(re.findall(findScore, str(item))[0])  # 提取评分
        img = str(re.findall(findImg, str(item))[0])  # 提取图片链接
        data.append(Movie(cName, eName, score, img, url))
    return data


def saveData(data):
    conn = getConnetion()  # 获取数据库连接
    cursor = conn.cursor()  # 得到查询对象
    # 保存到excel
    excel = xlwt.Workbook(encoding="utf-8")  # 创建excel对象
    movieTable = excel.add_sheet("movie")  # 创建一张表
    movieTable.write(0, 0, "中文名")
    movieTable.write(0, 1, "英文名")
    movieTable.write(0, 2, "电影链接")
    movieTable.write(0, 3, "图片链接")
    movieTable.write(0, 4, "评分")
    i = 1
    for movie in (data):
        cName = movie.getcName()
        # eName = movie.geteName()
        # url = movie.getUrl()
        img = movie.getImg()
        # score = movie.getScore()
        #  保存到excel
        # movieTable.write(i, 0, cName)
        # movieTable.write(i, 1, eName)
        # movieTable.write(i, 2, url)
        # movieTable.write(i, 3, img)
        # movieTable.write(i, 4, score)
        # #  保存的数据库
        # cursor.execute("insert into movie values (%s, %s, %s, %s, %s)", (cName, eName, url, img, score))
        #  下载图片
        DownLoad.downLoad(img, cName)
        i = i + 1
    # excel.save("movie.xls")  # 保存写入磁盘
    # conn.commit()  # 提交事务
    # conn.close()  # 关闭连接


def askURL(url):
    # 头部信息，用于给服务器识别是哪种类型浏览器能够接受什么数据，服务器才会让返回信息回来
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" +
                      "Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71"}
    html = ""
    request = urllib.request.Request(url, headers=head)  # 给服务器发请求获得已连接的对象
    # 异常捕获
    try:
        response = urllib.request.urlopen(request)  # 使用已连接的对象向服务器请求数据
        html = response.read().decode("utf-8")  # 获取html文档
    except urllib.error.URLError as e:
        if hasattr(e, "code"):  # 若有错误码 则打印错误码信息
            print(e.code)
        if hasattr(e, "reason"):  # 打印详情
            print(e.reason)
    return html


if __name__ == '__main__':
    main()
