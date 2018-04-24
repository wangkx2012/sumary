# -*- coding:utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import socket
import httplib
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')


class Spider(object):
    """Spider"""
    def __init__(self):
        self.return_url = []

    def getNextUrls(self,url):
        self.url = url
        request = urllib2.Request(self.url)
        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')

        html = urllib2.urlopen(request)
        soup = BeautifulSoup(html,'html.parser')
        print soup.prettify()
        #result = soup.select('h3.c-title')
        result = soup.select('div.media-body')
        for i in result:
            #news_url = i.select('a')[0].get("href")
            try:
                news_url = i.select('span.lks')[0].get_text()
            except:
                print i
                continue
            if news_url in self.return_url:
                continue
            self.return_url.append(news_url)
            print news_url

s = Spider()
append_list = 10
page =1
while append_list != 0:
    url = 'http://search.gmw.cn/search.do?c=n&cp='+str(page)+'&q=%25E5%258F%2599%25E5%2588%25A9%25E4%25BA%259A%25E6%2588%2598%25E4%25BA%258B&tt=false&to=true&adv=false'
    before_list = len(s.return_url)
    s.getNextUrls(url)
    after_list = len(s.return_url)
    #print after_list
    append_list = before_list - after_list
    page+=1
#s.getNextUrls(url)

