import math
import collections
import pandas as pd
import re


## 加载数据，用户-物品倒排列表,返回一个字典，key=user,value=(user,items*)
def load_data(file_path):
    dataSet = dict()
    f = open(file_path, "r", encoding="utf-8")
    for line in f:
        data = line.strip().split(",")
        user = data[0]
        del data[0]
        dataSet[user] = data
        f.close()

    return dataSet

## 计算k=1时的支持度，返回符合支持度和不符合支持度，类型为字典，key=item_name,value=item_count
def cut_tree(data_count, data_num, support):
    data = dict([(phone, num) for phone, num in data_count.items() if (num * 1.0 / data_num) >= support])


def cut_tree(data_count, data_num, support):
    data = dict([(phone, num) for phone, num in data_count.items() if (num * 1.0 / data_num) >= support])  # 第一次剪枝

    data_cut = dict([(phone, num) for phone, num in data_count.items() if (num * 1.0 / data_num) < support])  # 第一次剪枝
    return data, data_cut


## 计算k个项的组合项集，利用递归的思想
def Combinations(data, k):
    n = len(data)
    result = []
    for i in range(n - k + 1):
        if k > 1:
            newL = data[i + 1:]
            Comb = Combinations(newL, k - 1)
            for item in Comb:
                item.insert(0, data[i])
                result.append(item)
        else:
            result.append([data[i]])

    return result


## 获取k个元素的组合项集，除去k-1不符合支持度的子集（这个值通过剪枝得到）
def move_cut(data, data_cut, K):
    phone = []
    phone_move = []
    for key, value in data.items():
        phone += key.split("、")

    phone = list(set(list(phone)))
    data_list = Combinations(phone, K)  # 获取子集
    if len(data_list) == 0:
        return data

    for key, value in data_cut.items():
        phone_move.append(key.split("、"))

    for i in phone_move:
        for j in data_list:
            if set(list(i)).issubset(list(j)):
                data_list.remove(j)

    return data_list


## 计算组合项集中的元素在用户-物品倒排表当中出现的次数，主要用于计算支持度
def num_count(dataSet, data):
    data_list = collections.OrderedDict()
    for user, phone in dataSet.items():
        phone = list(phone)
        print 'phone:', phone
        for i in data:
            if set(list(i)).issubset(list(phone)):
                print str(set(list(i))) + ":" + str(list(phone))
                keys = "、".join(list(i))
                data_list.setdefault(keys, 0)
                data_list[keys] += 1

    return data_list


## 计算所有用户items的购买次数，返回一个字典，key=item_name,value=item_count，其实就是k=1时的num_count
def first_num_count(dataSet):
    data_list = dict()
    for user, phone in dataSet.items():
        for keys in phone:
            data_list.setdefault(keys, 0)
            data_list[keys] += 1
    return data_list


## 函数主程序入口
if __name__ == '__main__':

    # dataSet = load_data(file_path)
    dataSet = {'A': ['Mix3', 'XR', 'mate20'], 'B': ['Mix3', 'P20', 'nexs'], 'C': ['Mix3', 'P20', 'nexs', 'mate20'],
               'D': ['P20', 'nexs']}
    print("用户-物品倒排列表: ", dataSet)

    ## 获取所有用户items的购买次数
    data_count = first_num_count(dataSet)
    print("第1次剪枝前拓展项计数: ", data_count)

    ## 获取用户-物品倒排列表的大小
    data_num = len(dataSet)
    print data_num
    ## 物品的项集为1时，根据支持度进行剪枝
    data, data_cut = cut_tree(data_count, data_num, 0.5)
    print("第1次剪枝后拓展项计数: ", data)

    ## 将物品的项集置为2
    K = 2
    while True:
        ## 获取k个元素的组合项集，除去k-1不符合支持度的子集：data_cut
        data = move_cut(data, data_cut, K)
        print("第%d次拓展初始集合: %s" % (K, data))
        ## 计算组合项集中每个元素在用户-物品倒排表当中出现的次数
        data_count = num_count(dataSet, data)
        print("第%d次剪枝前拓展项计数: %s" % (K, data_count))

        if len(data_count) == 0:  # 如果无法拓展，表示已经完成，data为最后的拓展项集
            print(">>>>>拓展结束")
            break

        # 剪枝，剪去不满足支持度的项
        data, data_cut = cut_tree(data_count, data_num, 0.5)
        print("第%d次剪枝后拓展项计数: %s" % (K, data))
        print("第%d次被剪枝数据: %s" % (K, data_cut))

        K += 1

    print '最后的拓展项集为:', data

    phone = []
    for key, value in data.items():
        phone = key.split("、")
        num = value

    # 获取列表的非空子集
    print("phone: ", phone)
    data_num = []
    for i in range(1, len(phone)):
        data_num += Combinations(phone, i)

    print("非空子集:", data_num)

    conf_data = {}
    # 置信度计算
    for i in data_num:
        count = 0
        for u, v in dataSet.items():
            if set(i).issubset(list(v)):
                count += 1
                conf_data.setdefault(str(i), 0)
                conf_data[str(i)] = (float(num) / count)
    # 输出各子集置信度
    print '各子集置信度:', conf_data

    # 筛选掉不符合置信度的选项
    new_conf_data = dict([(conf, num) for conf, num in conf_data.items() if num >= 0.75])

    print '符合置信度的项集:', new_conf_data

    ## 计算提升度，需要get到support(X),support(Y),support(X交Y)
    ## 定义一个列表，用于存放所有项集的集合
    dim_conf_gather = []
    for conf_i in new_conf_data:
        ## 定义一个list,用于存放计算提升度的项集集合
        conf_gather = []
        conf_gather.append(conf_i[1:len(conf_i) - 1].replace("'", "").replace(", ", ",").split(","))
        conf_gather.append(
            list(set(phone) - set(conf_i[1:len(conf_i) - 1].replace("'", "").replace(", ", ",").split(","))))
        conf_gather.append(phone)
        dim_conf_gather.append(conf_gather)
    print '所有项集的集合:', dim_conf_gather

    ## 带入计算，每个项集的在用户-物品倒排表出现的次数
    ## 定义一个列表用于存放data_count
    list_data_count = []
    for i in dim_conf_gather:
        data_count = num_count(dataSet, i)
        list_data_count.append(data_count)
    print list_data_count
    ## 计算提升度
    lift = {}
    for i in list_data_count:
        for index in range(len(i.items())):
            index_name = i.items()[0][0]
            if index == 0:
                support_X = i.items()[0][1]
            elif index == 1:
                support_Y = i.items()[1][1]
            elif index == 2:
                support_XY = i.items()[2][1]
        ## 根据公式计算提升度
        lift.setdefault(index_name, 0)
        lift[index_name] = (float(support_XY) / len(dataSet)) / (
                    (float(support_X) / len(dataSet)) * (float(support_Y) / len(dataSet)))

    for i in lift.items():
        if i[1] > 1:
            print '由于{0}大于1，所以购买了{1}的用户，很可能会购买{2}'.format(i[1], i[0], list(set(phone) - set(i[0].split("、"))))
