# -*- coding:utf-8 -*-
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import json
import jieba
import copy
from datetime import datetime
import re
import pickle
import numpy as np
import lda
import lda.datasets
import docx

def read_docx(file_name):
    doc = docx.Document(file_name)
    content = [para.text for para in doc.paragraphs]
    sentence_tag = u"[。？！]"
    sentence_list = []
    for c in content:
        c = re.split(sentence_tag,c)
        sentence_list.extend(c)
    return sentence_list[0],sentence_list[1:]

def make_info(dir_name):
    news_info=[]
    path = dir_name #u'D:\办公' #unicode
    for root, dirs, files in os.walk(path): #该目录下所有文件和文件夹 os.listdir仅当前
        for ff in files:
            file_name = os.path.join(root,ff)
            title,file_content = read_docx(file_name)
            content={'title':title,'content_text':file_content}
            news_info.append(content)
    return news_info

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
                if i not in word_list and i not in stopword_dict:
                    word_list.append(i)
    vocab = tuple(word_list)
    return vocab

def make_lda_data(news_info, LEN_WORD,stopword_dict):
    titles = []
    X=[]
    for info in news_info:
        one_line = [0 for i in range(0,LEN_WORD)]
        one_word_list = {}
        titles.append(info['title'])

        news_list = info['content_text']
        for sencent in news_list:
            sencent = jieba.cut(sencent)
            for i in sencent:
                i = clean_str(i)
                if i and i not in stopword_dict:
                    if i not in one_word_list:
                        one_word_list[i] = 1
                    else:
                        one_word_list[i] +=1

        for j in one_word_list:
            if j not in word_to_num:
                continue
            index = word_to_num[j]
            one_line[index] = one_word_list[j]
        X.append(one_line)

    return np.array(X), tuple(titles)

if __name__ == '__main__':
    stopword_dict = stopword('../data/stopword.txt')
    #list中存放dict形式，title，content_text为list，为每个句子。
    ready=False
    if ready:
        news_info = read_info('../data/news_con.plf')
        print len(news_info)
    else:
        #读取文件目录下的所有文件
        news_info = make_info('../')
        print len(news_info)

    #词袋list
    vocab = make_vob(news_info)
    word_to_num,num_to_word = make_bagofword(vocab)
    LEN_WORD = len(word_to_num)
    #形成标题和文档矩阵
    X, titles = make_lda_data(news_info, LEN_WORD,stopword_dict)
    print len(word_to_num),len(vocab),len(titles)
    
    model = lda.LDA(n_topics=10, n_iter=1000, random_state=1)
    model.fit(X)  # model.fit_transform(X) is also available
    topic_word = model.topic_word_  # model.components_ also works
    n_top_words = 8
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
        print('Topic {}: {}'.format(i, '#'.join(topic_words)))
