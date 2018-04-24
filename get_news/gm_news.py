# -*- coding:utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import socket
import httplib
import sys
import pickle
import os
reload(sys)
sys.setdefaultencoding('utf8')

def getNews(url):
    xinwen = ''
    request = urllib2.Request(url)
    request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; \
        WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')
    try:
        html = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print e.code
        return False,None
    info_dict = {}
    soup = BeautifulSoup(html,'html.parser')
    way = [news_type2,news_type1,news_type3,news_type4,]
    success = False
    for one_way in way:
    #    one_way(soup)
        try:
            title,time,content_text = one_way(soup)
            success = True
        except Exception as e:
            print e
        if success:
            info_dict = {
                        'url':url,
                        'title':title,
                        'time':time,
                        'content_text':content_text,}
            break
    return success,info_dict

def news_type1(soup):
    title = soup.select('div#articleTitle')[0].get_text().replace('\r','').replace('\n','').replace(' ','').strip()
    time = soup.select('span#pubTime')[0].get_text().replace('\r','').replace('\n','').strip()
    content = soup.select('div#contentMain')[0].find_all('p')
    content_text = []
    for i in content:
        if i.get('class'):
            continue
        i = i.get_text().replace('\r','').replace('\n','').replace(' ','').replace('u\u3000','')
        if len(i)<15:
            continue
        content_text.append(i.strip()) 
    return title,time,content_text

def news_type2(soup):
    title = soup.select('h1#articleTitle')[0].get_text().replace('\r','').replace('\n','').replace(' ','').strip()
    time = soup.select('span#pubTime')[0].get_text().replace('\r','').replace('\n','').strip()
    content = soup.select('div#contentMain')[0].find_all('p')
    content_text = []
    for i in content:
        if i.get('class'):
            continue
        i = i.get_text().replace('\r','').replace('\n','').replace(' ','').replace('u\u3000','')
        if len(i)<15:
            continue
        content_text.append(i.strip()) 
    return title,time,content_text

def news_type3(soup):
    title = soup.select('div.hd > h1')[0].get_text().replace('\r','').replace('\n','').replace(' ','').strip()
#    time = soup.select('span#pubTime')[0].get_text()
    time = ''
    content = soup.select('div.bd')[0].find_all('p')
    content_text = []
    for i in content:
        if i.get('class'):
            continue
        i = i.get_text().replace('\r','').replace('\n','').replace(' ','').replace('u\u3000','')
        if len(i)<15:
            continue
        content_text.append(i.strip()) 
    return title,time,content_text
def news_type4(soup):
    title = soup.select('div.title > h2')[0].get_text().replace('\r','').replace('\n','').replace(' ','').strip()
    time = soup.select('div.title > p > span:nth-of-type(2)')[0].get_text().replace('\r','').replace('\n','')
    content = soup.select('div.content')[0].find_all('p')
    content_text = []
    for i in content:
        if i.get('class'):
            continue
        i = i.get_text().replace('\r','').replace('\n','').replace(' ','').replace(u'\u3000','')
        if len(i)<15:
            continue
        content_text.append(i.strip()) 
    return title,time,content_text

def save_pickle_data(data, filename):
    save_file_point = open( str(filename)+'.plf', 'wb')
    pickle.dump(data, save_file_point)
    save_file_point.close()


#getNews('http://tech.gmw.cn/2017-11/30/content_26955386.htm')
all_url = 0
success_count = 0
all_info =[]
for url in open('hongmao.url'):
    all_url+=1
    url = url.strip()
    success,info_dict = getNews(url)
    if success:
        all_info.append(info_dict)
        success_count +=1
print success_count*1.0/all_url
save_pickle_data(all_info, '../data/hongmao')


