# -*- coding:utf-8 -*-
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')
import time
import json
import jieba
import copy
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import traceback
import json
import pickle
import re
from re_conf import *

re_dict = init_re_exp()
def read_info(filename):
    load_info=open(filename,'rb')
    info=pickle.load(load_info)#list[dict,dict] 15323行 
    load_info.close()
    return info

def save_pickle_data(data, filename):
    save_file_point = open( str(filename)+'.plf', 'wb')
    pickle.dump(data, save_file_point)
    save_file_point.close()

def re_match(content,re_cates):
    des_num = {}
    for re_cate in re_cates:
        if len(re_cate) != 2:
            continue
        describ = re_cate[1]
        ret = re_cate[0].findall(content)
        if len(ret) == 0:
            continue
        if type(ret[0]) == tuple:
            ret = ret[0]
        else:
            ret = [ret[0]]
        if len(describ) != len(ret):
            continue
        for  i in range(len(ret)):
            if describ[i] == '无用':
                continue
            des_num[describ[i]] = ret[i]
        break
    return des_num


if __name__ == '__main__':
    news_info = read_info('../data/news_con.plf')
    url_time = re.compile('(\d{4}-\d+)/(\d+)')
    news_time = re.compile('(\d{4}-\d+-\d+)')
    sentence_info = {
        'sentence':'',
        'title':'',
        'doc_num':0,
        'para_num':0,
        'sentence_num':0,
        'sentence_time':'',
        'doc_time':'',
        'final_value':0,
        'value':{},
        'sentence_id':0
    }
    sentence_tag = u"[。？！]"
    doc_num = 0
    sentence_id = 0
    all_sentence_list = []
    quchong_sentence = []
    for info in news_info:
        doc_num += 1
        if not info['time']:
            url = info['url']
            doc_time = url_time.findall(url)
            #http://politics.gmw.cn/2017-12/27/content_27199476.htm
            if len(doc_time) == 2:
                doc_time = '-'.join(doc_time)
                doc_time = datetime.strptime(doc_time ,"%Y-%m-%d")
            else:
                print 'wrong url',url
                doc_time = datetime.now()
        else:
            doc_time = news_time.findall(info['time'])
            if len(doc_time)  == 1:
                doc_time = doc_time[0]
                doc_time = datetime.strptime(doc_time ,"%Y-%m-%d")
            else:
                print "wrong time",info['time']
                doc_time = datetime.now()
        info['doc_time'] = doc_time
#分割得到的句子，句子所在文档，句子所在段落，自己顺序编号，句子所在时间，句子权重，句子的唯一编号
        content_text = info['content_text']
        para_num=0
        sentence_num =0
        last_sentence_time = doc_time
        last_para_num = 0
        for content in content_text:
            para_num+=1
            sentence_list = re.split(sentence_tag,content)
            for sentence in sentence_list:
                if sentence in quchong_sentence:
                    continue
                quchong_sentence.append(sentence)
                if len(sentence) < 5:
                    continue
                if sentence[-1:] not in [u'。',u'！',u'？']:
                    sentence+=u'。'
                sentence_num+=1
                sentence_id+=1
                if para_num == last_para_num:
                    sentence_time = last_sentence_time
                else:
                    sentence_time = doc_time
                last_para_num = para_num
                des_num = re_match(sentence, re_dict)
                for i in des_num:
                    if 'y' ==i:
                        try:
                            year = int(des_num['y'])
                            sentence_time.replace(year = year)
                        except:
                            if des_num['y'] == u'今':
                                pass
                            elif des_num['y'] == u'明':
                                sentence_time = sentence_time + relativedelta(months=12)
                            elif des_num['y'] == u'去':
                                sentence_time = sentence_time - relativedelta(months=12)
                    if 'm' ==i:
                        try:
                            month = int(des_num['m'])
                            sentence_time.replace(month = month)
                        except:
                            if des_num['m'] == u'下':
                                sentence_time = sentence_time + relativedelta(months=1)
                            elif des_num['m'] == u'上':
                                sentence_time = sentence_time - relativedelta(months=1)
                    if 'd' ==i:
                        try:
                            day = int(des_num['d'])
                            sentence_time.replace(day = day)
                        except:
                            if des_num['d'] == u'明':
                                sentence_time = sentence_time + timedelta(days=1)
                            elif des_num['d'] == u'昨':
                                sentence_time = sentence_time - timedelta(days=1)


                this_sentence = copy.deepcopy(sentence_info)
                this_sentence['doc_num'] = doc_num
                this_sentence['para_num'] = para_num
                this_sentence['sentence_num'] = sentence_num
                this_sentence['sentence_time'] = sentence_time
                this_sentence['sentence_id'] = sentence_id
                this_sentence['sentence'] = sentence
                this_sentence['title'] = info['title']
                this_sentence['doc_time'] = doc_time
                all_sentence_list.append(this_sentence)
    print len(all_sentence_list)
    save_pickle_data(all_sentence_list,'../data/all_sentence_list')


