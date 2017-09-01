#coding:utf-8
import os
import jieba
import jieba.analyse
import jieba.posseg as pseg
import pickle
from pickle import dump
from sentens import *
from collections import Counter
import uniout

stop_words = []
cutlist = "。！？"
# 加载停用词
def loadStopWords(filepath = "./stopword"):
    file_list = eachFile(filepath)
    for file_name in file_list:
        fopen = open(file_name, 'r')  # r 代表read
        for eachLine in fopen:
            stop_words.append(eachLine.replace("\r\n", "").decode("utf-8"))
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
def cutFileBySentens(filename, clear_stop_word = False):
    #TODO
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
def cutFile(filename, clear_stop_word=False):
    fopen = open(filename, 'r')  # r 代表read
    content = ""
    for eachLine in fopen:
        # print "读取到得内容如下：", eachLine
        content += eachLine.replace(" ","")
    fopen.close()
    # segList = list(jieba.cut(content))
    segList = [x.encode('utf-8') for x in list(jieba.cut(content))]

    if clear_stop_word:
        result = []
        for seg in segList:
            if not is_stop_word(seg):
                result.append(seg)
        return result

    # segList = list(jieba.cut(content))
    # print filename, ":",' '.join(segList)
    #for seg in segList:
        #print seg, is_stop_word(seg);
    return segList

# 对某字符串分词
def cut_str(str):
    return list(jieba.cut(str))

def cutFileWithPosseg(filename):
    fopen = open(filename, 'r')  # r 代表read
    content = ""
    for eachLine in fopen:
        # print "读取到得内容如下：", eachLine
        content += eachLine
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
        content += eachLine
    fopen.close()
    segList = list(jieba.analyse.extract_tags(content, 50, True))

    # segList = list(jieba.cut(content))
    # print filename, ":",' '.join(segList)
    for seg in segList:
        print seg[0],seg[1], is_stop_word(seg[0])

def gen_all_words(filePaths, destination_file, clear_stop_word):
    file = open(destination_file, 'w')
    all_words = []
    for filePath in filePaths:
        all_words.extend(cutFile(filePath, clear_stop_word))
    dump(all_words, file)
    file.close()

    file = open(destination_file + "_dic", 'w')
    dump(dict(Counter(all_words)), file)
    file.close()

def load_all_words(destination_file):
    file = open(destination_file, 'rb')
    words = pickle.load(file)
    file.close()
    return words

# 计算词字典
# 输出： 词频表、  词表
# 更新停用词
# 更新词表
# 给出常词表
# 根据词频表给出  关键词表，关键词表 + 常词表  有可能就是答案集合
#
def step_1():
    gen_all_words(filePaths, "allwords", True);
    print load_all_words("allwords");
    print load_all_words("allwords_dic")


if __name__ == '__main__':
    filePathC = "./news"
    filePaths = eachFile(filePathC)

    # 加载词典
    jieba.load_userdict("./dict")
    # 加载停用词

    loadStopWords()
    # gen_all_words(filePaths, "allwords", True);

    for filePath in filePaths:
        #cutFileWithPosseg(filePath)
        #cutFile(filePath)
        # cutWithWeight(filePath)
        # cut_file_sentens(filePath)
        # print  cutFileBySentens(filePath)
        print "================"

    # TODO
    # 自动找字典 RUN
    # 找答案集合
    # 按句子分词 OK