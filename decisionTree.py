# -*- coding: utf-8 -*-
'''
决策树
* 熵H(Y)：表示随机变量的不确定性= -sum(pi * logpi)
  条件熵H(Y|X)：sum(pi * H(Y|X == xi))

* 信息增益/互信息 g(D,A) = H(Y) - H(Y|X)
  用法：特征选择

* ID3算法构建决策树：每一步根据当前决策树的信息增益进行划分
    - 手写决策树实现过程

* C4.5算法构建决策树：
'''

import operator
from math import log
import numpy as np

def load_data():
    dataSet = [[0, 0 ,0, 0, 'no'],
               [0, 0 ,0, 1, 'no'],
               [0, 1 ,0, 1, 'yes'],
               [0, 1 ,1, 0, 'yes'],
               [0, 0 ,0, 0, 'no'],
               [1, 0, 0, 0, 'no'],
               [1, 0, 0, 1, 'no'],
               [1, 1, 1, 1, 'yes'],
               [1, 0, 1, 2, 'yes'],
               [1, 0, 1, 2, 'yes'],
               [2, 0, 1, 2, 'yes'],
               [2, 0, 1, 1, 'yes'],
               [2, 1, 0, 1, 'yes'],
               [2, 1, 0, 2, 'yes'],
               [2, 0, 0, 0, 'no']]
    feature_names = ['age','job','house','credit']
    return dataSet, feature_names

def entropy(dataSet):
    m = len(dataSet)
    labelCounts = {}
    for featureVec in dataSet:
        currentLabel = featureVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1

    e = 0.0
    for _ ,value in labelCounts.items():
            e -= value/m * log(value/m,2)
    return e

def splitDataSet(dataSet, axis):
    ret_dataSet = {}
    for featureVec in dataSet:
        if featureVec[axis] not in ret_dataSet.keys():
            ret_dataSet[featureVec[axis]] = []
        tmpVec = featureVec.copy()
        tmpVec.pop(axis)
        ret_dataSet[featureVec[axis]].append(tmpVec)
    return ret_dataSet

def chooseFeature(dataSet):
    H_x_list = []
    node_id = -1
    ret_dataSet = {}
    feature_nums = len(dataSet[0])-1
    for feature_id in range(feature_nums):
        tmp_dataset = splitDataSet(dataSet,feature_id)
        H_x = 0
        for _, sub_dataset in tmp_dataset.items():
            H_x += len(sub_dataset) / len(dataSet) * entropy(sub_dataset)
        H_x_list.append(H_x)
        if node_id == -1 or H_x < H_x_list[node_id]:
            node_id = feature_id
            ret_dataSet = tmp_dataset
    return node_id, ret_dataSet

# 以叶子结点中最多result为res
def vote(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def trainTree(dataSet, feature_names):
    # 使用终止条件: 当前子集中所有类别都一致/没有可选特征了(即没有可判断节点了)
    # todo：也可以使用信息增益最低阈值
    # 返回dict形式
    classList = [featureVec[-1] for featureVec in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(feature_names) == 0:
        return vote(classList)
    feature_id , sub_trees= chooseFeature(dataSet)
    feature_name = feature_names[feature_id]
    tmp_feature_names = feature_names.copy()
    tmp_feature_names.pop(feature_id)
    resTree = {feature_name:{}}
    for key, subtree in sub_trees.items():
        resTree[feature_name][key] = trainTree(subtree,tmp_feature_names)
    return resTree

def predict(dtree, feature_names, testVec):
    first_feature_name = list(dtree.keys())[0]
    print("current feature_name is :",first_feature_name )
    first_feature_index = feature_names.index(first_feature_name)
    first_value = testVec[first_feature_index]
    print("current feature_value is :",first_value)
    node = dtree[first_feature_name][first_value]
    if (isinstance(node,dict)):
        predict(node, feature_names,testVec)
    else:
        print(node)

if __name__ == '__main__':
    dataSet, feature_names = load_data()
    H = entropy(dataSet)
    print(H)
    dtree = trainTree(dataSet, feature_names)
    predict(dtree, feature_names,[1,1,0,1])


   