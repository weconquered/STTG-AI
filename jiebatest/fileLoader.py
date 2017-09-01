#coding:utf-8
import os
import jieba
import jieba.analyse
import jieba.posseg as pseg
import pickle
from pickle import dump
from sentens import *
import uniout

stop_words = []
cutlist = "。！？"
# 加载停用词
def loadStopWords(filepath):
    fopen = open(filepath, 'r')  # r 代表read
    for eachLine in fopen:
        stop_words.append(eachLine.decode('utf-8'))
    fopen.close()

# 判断是否是停用词
def is_stop_word(word):
    if word in stop_words:
        return True
    else:
        return False

# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath):
    fileList = [];
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s/%s' % (filepath, allDir))
        print child.decode('utf-8')  # .decode('utf-8')是解决中文显示乱码问题
        fileList.append(child.decode('utf-8'))
    return fileList

# 读取文件内容并打印
def cutFileBySentens(filename):
    sentenses = cut_file_sentens(filename)
    print filename, len(sentenses)
    result = []

    for sentens in sentenses:
        result.append((sentens, list(jieba.cut(sentens))))

    # segList = list(jieba.cut(content))
    # print filename, ":",' '.join(segList)
    # for seg in segList:
    # print seg, is_stop_word(seg);
    return result

    # 读取文件内容并打印
def cutFile(filename):
    fopen = open(filename, 'r')  # r 代表read
    content = "";
    for eachLine in fopen:
        # print "读取到得内容如下：", eachLine
        content += eachLine;
    fopen.close()
    segList = list(jieba.cut(content))

    # segList = list(jieba.cut(content))
    # print filename, ":",' '.join(segList)
    #for seg in segList:
        #print seg, is_stop_word(seg);
    return segList

def cutFileWithPosseg(filename):
    fopen = open(filename, 'r')  # r 代表read
    content = "";
    for eachLine in fopen:
        # print "读取到得内容如下：", eachLine
        content += eachLine;
    fopen.close()
    segList = pseg.cut(content)

    for seg in segList:
        print seg.word, seg.flag, is_stop_word(seg.word);
    return segList

# 读取文件内容并打印
def cutWithWeight(filename):
    fopen = open(filename, 'r')  # r 代表read
    content = ""
    for eachLine in fopen:
        # print "读取到得内容如下：", eachLine
        content += eachLine;
    fopen.close()
    segList = list(jieba.analyse.extract_tags(content, 50, True))

    # segList = list(jieba.cut(content))
    # print filename, ":",' '.join(segList)
    for seg in segList:
        print seg[0],seg[1], is_stop_word(seg[0])

def gen_all_words(filePaths, destination_file):
    file = open(destination_file, 'w')
    all_words = []
    for filePath in filePaths:
        all_words.append(cutFile(filePath))
    dump(all_words, file)
    file.close()

def load_all_words(destination_file):
    file = open(destination_file, 'rb')
    words = pickle.load(file)
    file.close()
    return words

if __name__ == '__main__':
    filePathC = "./news"
    filePaths = eachFile(filePathC)

    # 加载词典
    jieba.load_userdict("./dict")
    # 加载停用词

    loadStopWords("./stopwords")

    # gen_all_words(filePaths, "allwords");

    #print load_all_words("allwords");

    for filePath in filePaths:
        #cutFileWithPosseg(filePath)
        #cutFile(filePath)
        # cutWithWeight(filePath)
        # cut_file_sentens(filePath)
        print  cutFileBySentens(filePath)
        print "================"

    # TODO
    # 自动找字典
    # 找答案集合
    # 按句子分词