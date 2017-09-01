#coding:utf-8
import os
import jieba
import jieba.analyse
import jieba.posseg as pseg

stop_words = []

# 加载停用词
def loadStopWords(filepath):
    fopen = open(filepath, 'r')  # r 代表read
    for eachLine in fopen:
        stop_words.append(eachLine.decode('utf-8'))
    fopen.close()
    print stop_words

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
    for seg in segList:
        print seg, is_stop_word(seg);

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

# 读取文件内容并打印
def cutWithWeight(filename):
    fopen = open(filename, 'r')  # r 代表read
    content = "";
    for eachLine in fopen:
        # print "读取到得内容如下：", eachLine
        content += eachLine;
    fopen.close()
    segList = list(jieba.analyse.extract_tags(content, 50, True))

    # segList = list(jieba.cut(content))
    # print filename, ":",' '.join(segList)
    for seg in segList:
        print seg[0],seg[1], is_stop_word(seg[0]);


if __name__ == '__main__':
    filePathC = "./news"
    filePaths = eachFile(filePathC)

    # 加载词典
    jieba.load_userdict("./dict")
    # 加载停用词
    loadStopWords("./stopwords")

    for filePath in filePaths:
        cutFileWithPosseg(filePath)
        # cutFile(filePath)
        # cutWithWeight(filePath)
        print "================"

    # TODO
    # 自动找字典
    # 找答案集合
    # 按句子分词