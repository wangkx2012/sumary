#!/usr/bin/env python
#encoding=utf-8
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import time
import json
import jieba
import copy
from datetime import datetime
import traceback
import re
import pickle
import numpy as np

def clean_str(string):
    string = re.sub(ur"[^\u4e00-\u9fff]", "", string)
    #string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    #string = re.sub(r"\'s", " \'s", string)
    #string = re.sub(r"\'ve", " \'ve", string)
    #string = re.sub(r"n\'t", " n\'t", string)
    #string = re.sub(r"\'re", " \'re", string)
    #string = re.sub(r"\'d", " \'d", string)
    #string = re.sub(r"\'ll", " \'ll", string)
    #string = re.sub(r",", " , ", string)
    #string = re.sub(r"!", " ! ", string)
    #string = re.sub(r"\(", " \( ", string)
    #string = re.sub(r"\)", " \) ", string)
    #string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", "", string)
    #return string.strip().lower()
    return string.strip()

def stopword(filename):
    stopword_dict = {}
    wordfile= open(filename,'rb')
    for word in wordfile:
        word =word.strip().decode("utf-8")
        stopword_dict[word] = 1
    return stopword_dict

def make_bagofword(word_list):
    word_to_num = {}
    num_to_word = {}
    num = 0
    for i in word_list:
        if i not in word_to_num:
            word_to_num[i] = num
            num_to_word[num] = i
            num +=1
    return word_to_num,num_to_word

def read_info(filename):
    load_info=open(filename,'rb')
    info=pickle.load(load_info)#list[dict,dict] 15323行 
    load_info.close()
    return info

def make_vob(news_info):
    word_list = []
    for info in news_info:
        news_list = info['content_text']
        for sencent in news_list:
            sencent = jieba.cut(sencent)
            for i in sencent:
                i = clean_str(i)
                if i and i not in word_list and i not in stopword_dict:
                    word_list.append(i)
    vocab = tuple(word_list)
    return vocab

if __name__ == '__main__':
    stopword_dict = stopword('../data/stopword.txt')
    news_info = read_info('../data/news_con.plf')
    model = Word2Vec.load("all/all_embedding_128")
    print len(model.wv.vocab)
    vocab = make_vob(news_info)
    word_to_num,num_to_word = make_bagofword(vocab)
    LEN_WORD = len(word_to_num)
    #w2vModel.vector_size
    #w2vModel.wv.vocab
    print LEN_WORD
    similar_max = []
    conut=0
    for word in vocab:
        if conut%100==0:
            print conut
        conut+=1
        if word not in model.wv.vocab:
            similar_max.append([0 for i in range(LEN_WORD)])
            continue
        one_all_similar = []
        for one in vocab:
            one_index = vocab.index(one)
            word_index = vocab.index(word)
            if one not in model.wv.vocab or word_index>one_index:
                one_all_similar.append(0)
            else:
                one_all_similar.append(model.similarity(word, one))
    similar_max = np.array(similar_max)
    print similar_max.shape
