# -*- coding: utf-8 -*-
import uniout
from fileLoader import *

delimiters = ['。', '，', '！', '“', '”', '……', '？', '.', ',', '!', '"', '"', '?', '(', ')', '（', '）', '、']


def count_neighbours(the_whole):
    res = {}
    for seg_list in the_whole:
        zipped = filter(lambda x: not (x[0] in delimiters or x[1] in delimiters), zip(seg_list[:-1], seg_list[1:]))
        for a, b in zipped:
            key = a + b
            if key in res:
                res[key] += 1
            else:
                res[key] = 1
    res = [(v, k) for k, v in res.items()]
    res.sort(reverse=True)
    return res


def write_combined(path, res):
    with open(path, 'w') as f:
        f.writelines([x[1] + '\n' for x in res[:len(res) / 4]])


print("Reading all words...")
the_whole = load_all_words('./allwords')
print("Counting neighbours...")
result = count_neighbours(the_whole)
print("Writing to file...")
write_combined('./out/combined', result)

