import threading
import time
import urllib.request
from bs4 import BeautifulSoup
import re  # 正则表达
import smtplib
from email.mime.text import MIMEText
import pymysql


def getHtml():
  head = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  + 'Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47'}
  requese = urllib.request.Request('https://www.apple.com.cn/cn-k12/shop/buy-iphone/iphone-12', headers=head)
  response = urllib.request.urlopen(requese)
  html = response.read().decode('utf-8')
  return html


def getNew_val(html):
  soup = BeautifulSoup(html, "html.parser")
  item = soup.find_all('span', class_='nowrap')
  findData = re.compile(r'<span .*>.* (.*)</span>', re.S)
  data = re.findall(findData, str(item[0]))
  s = str(data[0])
  s = list(s)
  for j in range(1, len(s) - 1):
    i = j + 1
    s[j] = s[i]
  del s[-1]
  val = eval(''.join(s))
  return val


def sendEmail():
  subject = '减价了'
  message = MIMEText('iPhone12减价了', 'html', 'utf-8')
  message['From'] = '2021761583@qq.com'
  message['To'] = '595384262@qq.com'
  message['subject'] = subject
  smtp = smtplib.SMTP()
  smtp.connect('smtp.qq.com', )  #连接服务器
  smtp.login('2021761583@qq.com', 'udfalfmzjthlcggf')  #login in
  smtp.sendmail('2021761583@qq.com', '595384262@qq.com', message.as_string())
  smtp.quit()


def updateVal(val, new_val):
  conn = pymysql.connect(host="127.0.0.1", port=3306, database="test", user="root", password="88888888", charset="utf8")
  cur = conn.cursor()
  cur.execute('update valtable set val = %s where val = val', new_val)
  conn.commit()
  cur.close()
  conn.close()


def getVal():
  conn = pymysql.connect(host="127.0.0.1", port=3306, database="test", user="root", password="88888888", charset="utf8")
  cur = conn.cursor()
  cur.execute('select val from valtable')
  val = cur.fetchall()[0][0]
  cur.close()
  conn.close()
  return val


if __name__ == '__main__':
  val = getVal()
  print(val)
  while True:
    new_val = getNew_val(getHtml())
    if new_val < val:
      print(val,new_val)
      updateVal(val, new_val)
      sendEmail()
      val = new_val
  time.sleep(18000)





