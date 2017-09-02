# coding:utf-8

import random
import re
import uniout

# seq = [2, 6, 4, 3, 1, 7, 9, 8, 5]


def generate():
    return [(random.randint(0, 100), 1) for x in range(0, 10)]


def find_top_k(a, k):
    return find(a, k, 0, len(a) - 1)


def find(a, k, p, r):
    if k <= 0:
        return []
    else:
        q = partition(a, p, r)
        if q - p <= k:
            return a[p:q] + find(a, k - (q - p), q, r)
        else:
            return find(a, k, p, q - 1)


def partition(a, p, r):
    x = a[r][0]
    i = p - 1
    for j in range(p, r):
        if a[j][0] <= x:
            i += 1
            tmp = a[i]
            a[i] = a[j]
            a[j] = tmp
    tmp = a[i + 1]
    a[i + 1] = a[r]
    a[r] = tmp
    return i + 1

num_regex = ur'((大)?(约)?\d+(\.\d+)?(%|°C|℃|％)?(.{,5}左右)?)'
suffix_regex = ur'(多少|几)'

def extract_quant(sent, query):
    # suffixes = [query[match.end():] for match in re.finditer(suffix_regex, query)]
    # print(suffixes)
    quants = [x[0] for x in re.findall(num_regex, sent)]
    print(quants)
    return quants

# extract_quant(u"这a是b什么cc啊，来个百分比97.5%啊222.93％中文百分号，来个97.5小数，来个234234整数，来个32.4°C度234℃数！")
extract_quant(u"一般而言，在最初的约20秒左右,色彩感在人们对物体的视觉感中占0.2百分比", u"一般而言，在最初的几秒内,色彩感在人们对物体的视觉感中占多少百分比")





