#-*- coding:utf-8 -*-
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import re


re_dict = [
[u'(\d{4})年(\d+)月(\d+)日',['y','m','d']],
[u'(今)年(\d+)月(\d+)日',['y','m','d']],
[u'(明)年(\d+)月(\d+)日',['y','m','d']],
[u'(去)年(\d+)月(\d+)日',['y','m','d']],
[u'(\d{4})年(\d+)月',['y','m','d']],
[u'(今)年(\d+)月',['y','m']],
[u'(明)年(\d+)月',['y','m']],
[u'(去)年(\d+)月',['y','m']],
[u'(\d+)月(\d+)日',['m','d']],
[u'(上)个月(\d+)日',['m','d']],
[u'(下)个月(\d+)日',['m','d']],
[u'(上)个月',['m']],
[u'(下)个月',['m']],
[u'(\d+)月',['m']],
[u'(\d+)日',['d']],
[u'(昨)天',['d']],
[u'(昨)日',['d']],
[u'(明)天',['d']],
[u'(明)日',['d']]
]

def init_re_exp():
    for i in range(len(re_dict)):
        try:
            re_dict[i][0] = re.compile(re_dict[i][0])
        except:
            print 'wrong re:', re_dict[i][0]
    return re_dict

