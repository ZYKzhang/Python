#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "pytest", charset="utf8")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()

print ("Database version : %s " % data)

cursor.execute("set names utf8")
#查询
#cursor.execute("SELECT * FROM zufang")
#for row in cursor.fetchall():
    #print(row)

print ("kaishi")
links = []
for u in ['https://xa.lianjia.com/zufang/changan2/', 'https://xa.lianjia.com/zufang/changan2/pg2/', 'https://xa.lianjia.com/zufang/changan2/pg3/']:
    r = requests.get('https://xa.lianjia.com/zufang/changan2/')
    soup = BeautifulSoup(r.text, "html.parser")
    links_div = soup.find_all('div', class_="pic-panel")
    link = [div.a.get('href')for div in links_div]
    links += link
print ("jieshu")
#f = open("E:\All Code\Python\pythontest\shuju.txt",'w')
count = 1
for i in links:
    print(i, end='\n')
    r_house = requests.get(i)
    soup_house = BeautifulSoup(r_house.text, "html.parser")
    price = soup_house.find('span', class_="total").text.strip()
    unit = soup_house.find('span', class_="unit").text.strip()
    info = soup_house.find_all('p',class_="lf")
    info_address = soup_house.find_all('p')
    area = info[0].text[3:]  # type: object
    type = info[1].text[5:]
    address = info_address[5].text[3:10]
    floor = info[2].text[3:]
    towards = info[3].text[5:]
    phone = soup_house.find('div', class_="phone").text
    phone = phone[15:25]
    print(count)
    count = count + 1
    print('价格：%s%s' % (price, unit))
    jiage = price +unit
    print('面积：%s' % area)
    print('户型：%s' % type)
    print('楼层：%s' % floor)
    print('朝向：%s' % towards)
    print('联系电话：%s' % phone)
    print('小区：%s' % address)
    # SQL 插入语句
    sql = "INSERT INTO zufang VALUES ('%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" % (count, jiage, area, type, floor, towards, phone, address)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()

    except:
        # 如果发生错误则回滚
        db.rollback()
        print("出错")
    '''
    f.write(str(count))
    count = count + 1
    f.write('\n')
    f.write('价格：')
    f.write(price)
    f.write(unit)
    f.write('\n')
    f.write('面积：')
    f.write(area)
    f.write('\n')
    f.write('户型：')
    f.write(type)
    f.write('\n')
    f.write('楼层：')
    f.write(floor)
    f.write('\n')
    f.write('朝向：')
    f.write(towards)
    f.write('\n')
    f.write('中介电话：')
    f.write(phone)
    f.write('\n')
    f.write('小区：')
    f.write(address)
    f.write('\n')
    f.write('\n')
f.close()
'''
# 关闭数据库连接
db.close()