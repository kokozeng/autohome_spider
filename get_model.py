# -*- coding: UTF-8 -*-

import requests
import os
import sys
import re
import time
import csv
from bs4 import  BeautifulSoup
import  lxml

reload(sys)
sys.setdefaultencoding( "utf-8" )

#得到一个网址的html信息
def get_page_html(detailurl):
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Referer": "http://www.example.com/",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}
    #user_agent = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    #headers = {'User_agent': user_agent}
    r = requests.get(detailurl, headers=headers)
    #r = requests.get(detailurl)
    r.encoding = 'UTF-8'
    result = r.text
    return result

def get_GBK_page_html(detailurl):
    #user_agent = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    #headers = {'User_agent': user_agent}
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Referer": "http://www.example.com/",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}
    r = requests.get(detailurl, headers=headers)
    r.encoding = 'GBK'
    result = r.text
    return result

#将一个网页信息保存在txt文档里
def write_html_txt(detail_url):
    data = get_page_html(detail_url)
    file = open('/home/koko/Documents/carspider/save/car_product.txt','w')
    file.write(data)
    file.close()


def write_csv(data):
    with open('huaian.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)

def write_txt(data, filename):
    file = open(filename + '.txt' ,'a')
    file.write(data)
    file.close()

def replace_others(data):
    data = str(data)
    data = data.replace('\r', '').replace('\n', '').replace('\t', '')
    return data

def get_car_data(url):
    source = get_GBK_page_html(url)
    soup = BeautifulSoup(source, 'lxml')
    car_list = soup.find_all('li')
    for car_link in car_list:
        single_car = car_link.find('h4')
        pattern = re.compile('<a href="//car.autohome.com.cn/pic(.*?)" id="atk', re.S)
        car_link_source = str(car_link)
        items = re.findall(pattern, car_link_source)
        try:
            car_name = single_car.get_text()
            car_row = str(car_name) + '\t' + str(items[0]) + '\n'
            #print car_row
            write_txt(car_row + '\n', 'cars_less')
        except:
            continue

#get_car_data(page)
for i in xrange(26):
    number = chr(i+ord('A'))
    number = str(number)
    page="https://www.autohome.com.cn/grade/carhtml/" + number +".html"
    print (page)
    get_car_data(page)