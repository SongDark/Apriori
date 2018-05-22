# coding:utf-8
import apriori
import time
import numpy as np

# 读取训练集
with open("./data/agaricus_train.csv", "rb") as f:
    dataSet = [line[:-1].split(',') for line in f.readlines()]

# L中的每一个元素都至少在25%的样本中出现过
L, suppData = apriori.apriori(dataSet, 0.25) # 阈值越小，越慢

# 生成规则，每个规则的置信度至少是0.6
bigRuleList = apriori.generateRules(L, suppData, 0.6)

# P→H，根据P集合的大小排序
bigRuleList = sorted(bigRuleList, key=lambda x:len(x[0]), reverse=True)

# 读取测试集
with open("./data/agaricus_test.csv", "rb") as f:
    dataSet = [line[:-1].split(',') for line in f.readlines()]
labels = np.array([int(x[0]) for x in dataSet])

scores = []
for line in dataSet:
    tmp = []
    for item in bigRuleList:
        if item[0].issubset(set(line)):
            if "1" in item[1]:
                tmp.append(float(item[2]))
            # 因为是预测“为1的概率”，所以要用1减
            if "0" in item[1]:
                tmp.append(1 - float(item[2]))
    scores.append(np.mean(tmp)) # 求取均值

scores = map(lambda x:x>0.5, scores)
scores = np.array(scores, dtype='int')
print sum(np.equal(scores, labels)), len(labels), sum(np.equal(scores, labels))/float(len(labels))