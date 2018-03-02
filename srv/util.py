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
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

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

def save_pickle_data(data, filename):
    save_file_point = open( str(filename)+'.plf', 'wb')
    pickle.dump(data, save_file_point)
    save_file_point.close()
