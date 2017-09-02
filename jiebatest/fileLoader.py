#coding:utf-8
import os
import jieba
import jieba.analyse
import jieba.posseg as pseg
import pickle
from pickle import dump
from sentens import *
from collections import Counter
import math
# from threading import Thread as worker
from processing import Process as worker
import uniout
import sys
# pre_fix = "/home/nimbix/corpus/"
pre_fix = "/Users/boloomo/Downloads/corpus/"
tag_1 = pre_fix + "1_产品使用说明文档"
tag_2 = pre_fix + "2_产品制作工艺流程"
tag_3 = pre_fix + "3_产品原材料需求文档"
tag_4 = pre_fix + "4_产品外观外形设计文档"
tag_5 = pre_fix + "5_产品相关专利文档"
tag_6 = pre_fix + "6_产品工艺设计"
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

all_words = []

def gen_all_words_worker(worker_id, filePaths, clear_stop_word):
    count_w = 0
    le = len(filePaths)
    for filePath in filePaths:
        all_words.extend(cutFile(filePath, clear_stop_word))
        count_w += 1
        print worker_id, str(count_w) + "/" + str(le) ,filePath

def gen_all_words(pre, filePaths, destination_file, clear_stop_word):
    file = open(pre + destination_file, 'w')

    print "共：" + str(len(filePaths)) + " 个文件"
    worker_size = 3
    total_len = len(filePaths)
    sentens_per_worker = math.ceil(total_len / worker_size)

    worker_index = []

    threads = []
    # top_x
    for i in range(0, worker_size):
        worker_index.append((i * sentens_per_worker, min((i + 1) * sentens_per_worker, total_len) - 1))
        # t = worker(target=gen_all_words_worker,
        #                      args=(i, filePaths[int(i * sentens_per_worker): int(min((i + 1) * sentens_per_worker, total_len))],clear_stop_word))
        t = worker(target=gen_all_words_worker, args=(i, filePaths[int(i * sentens_per_worker): int(min((i + 1) * sentens_per_worker, total_len))],
                         clear_stop_word))

        threads.append(t)

    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()

    dump(all_words, file)
    file.close()

    file = open(pre + destination_file + "_dic", 'w')
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
def step_1(pre, filePaths):
    gen_all_words(pre, filePaths, "allwords", True);
    # print load_all_words("allwords");
    # print load_all_words("allwords_dic")


if __name__ == '__main__':
    filePathC = tag_2
    filePaths = eachFile(filePathC)

    #tag = sys.argv[1]
    #begin = sys.argv[2]
    #end = sys.argv[3]
    #pre = sys.arg[4]
    # 加载词典
    jieba.load_userdict("./dict")
    # 加载停用词

    loadStopWords()
    step_1("2_", filePaths)
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