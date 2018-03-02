# -*- coding:utf-8 -*-
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')
import time
import json
import jieba
import copy
from datetime import datetime
import traceback
import json
import pickle
import re
from util import *
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer

FIRST_PARA = 1

def get_samilar(sentence_1,sentence_2):
    sum_value = []
    if sentence_1 and sentence_2:
        for i in sentence_1:
            for j in sentence_2:
                sum_value.append(model.similarity(i, j))
    else:
        return 0
    return sum(sum_value) * 1.0 / len(sum_value) 

def get_w2v(sentence):
    w2v_list = []
    sencent = jieba.cut(sentence)
    for i in sencent:
        i = clean_str(i)
        if i and i not in stopword_dict and i in model.wv.vocab:
            w2v_list.append(i)
    return w2v_list

def get_corpus(sentence_list):
    corpus = {}
    max_num = 0
    for sentence in sentence_list:
        sentence_con = jieba.cut(sentence['sentence'])
        if int(sentence['doc_num']) >max_num:
            max_num = int(sentence['doc_num'])
        if sentence['doc_num'] not in corpus:
            corpus[sentence['doc_num']] = []
        for seg in sentence_con:
            if (seg != '' and seg != "\n" and seg != "\n\n"):
                corpus[sentence['doc_num']].append(seg)
    new_corpus = ['nan' for i in range(max_num)]
    for k,v in corpus.items():
        v=' '.join(v)
        new_corpus[int(k)-1] = v
    return new_corpus

def get_tfidf(sentence_list):
    corpus = get_corpus(sentence_list)
    vectorizer=CountVectorizer() 
    transformer=TfidfTransformer()
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))
    word=vectorizer.get_feature_names()
    weight=tfidf.toarray()
    return word,weight

def get_tdidf_value(sentence,doc_num):
    weight_doc_num = weight[int(doc_num-1)]
    sentence = jieba.cut(sentence)
    w_weight = 0
    w_num = 0
    for i in sentence:
        if i in word:
            w_index = word.index(i)
            w_weight += weight_doc_num[w_index]
            w_num += 1
    return w_weight*1.0/w_num if w_num!=0 else 0
   
def make_v_weight(sentence_list):
    weight_v = {
    'pos':0,      
    'sent_samilar_value':0,
    'query_samilar_value':0,
    'tfidf_value':0,
    }
    count = 0
    for i in sentence_list:
        count+=1
        for k,v in i['value'].items():
            weight_v[k]+=v 
    for j in weight_v:
        weight_v[j] =count*1.0/ weight_v[j]
    all_weight = 0
    for j in weight_v:
        all_weight += weight_v[j]
    for j in weight_v:
        weight_v[j] =weight_v[j]/all_weight
    weight_v['query_samilar_value'] = weight_v['query_samilar_value']/2
    weight_v['sent_samilar_value'] = weight_v['sent_samilar_value']*2
    weight_v['pos'] = weight_v['pos']/2
    return weight_v

def get_final_value(value,weight_v):
#    weight_v = {
#    'pos':1,
#    'sent_samilar_value':1,
#    'query_samilar_value':1,
#    'tfidf_value':1,
#    }
    f_value = 0
    for k in value:
        f_value+=(value[k]*weight_v[k])
    return f_value

if __name__ == '__main__':
    sentence_list = read_info('../data/all_sentence_list.plf')
    stopword_dict = stopword('../data/stopword.txt')
    model = Word2Vec.load("../w2v/all/all_embedding_128")
    word,weight = get_tfidf(sentence_list)
    sentence_info = {
        'sentence':'',
        'doc_num':0,
        'para_num':0,
        'sentence_num':0,
        'sentence_time':'',
        'doc_time':'',
        'title':'',
        'value':{},
        'final_value':0,
        'sentence_id':0
    }
    query = u'网上购买地铁票'
#    time_list = []
#    for i in open('time.txt','rb'):
#        time_list.append(i.strip()) 
    #value :pos位置,查询相似度，标题相似度
    w2v_query = get_w2v(query)
    
    for sentence in sentence_list:
        w2v_title = get_w2v(sentence['title'])
        value = {}
        value['pos'] = FIRST_PARA if sentence['para_num']==1 else 0
        w2v_sentence = get_w2v(sentence['sentence'])
        value['sent_samilar_value'] = get_samilar(w2v_sentence,w2v_title)
        value['query_samilar_value'] = get_samilar(w2v_sentence,w2v_query)
        value['tfidf_value'] = get_tdidf_value(sentence['sentence'],sentence['doc_num'])

        sentence['value'] = value
        #print value
        for k,v in sentence.items():
            print str(k)+'#'+str(v)

    weight_v = make_v_weight(sentence_list)
    print weight_v
    for sentence in sentence_list:
        sentence['final_value'] = get_final_value(sentence['value'], weight_v)
        #print sentence['final_value']
    sort_sen = sorted(sentence_list,key = lambda e:e.__getitem__('final_value'), reverse=True)
    for i in  sort_sen[:10]:
        print i['final_value'],i['sentence'],i['value']
