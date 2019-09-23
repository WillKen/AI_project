import numpy as np
import math

# 读取训练集并将数据转换为矩阵形式
features = []
labels = []
trainFile_features = open('train-features.txt', 'r')
trainFile_labels = open('train-labels.txt', 'r')
for lines in trainFile_features:
    features.append(list(map(lambda x: int(x), lines.split())))
trainSet = np.matrix(features)
trainFile_features.close()
for lines in trainFile_labels:
    labels.append(list(map(lambda x: int(x), lines.split())))
trainLabel = np.matrix(labels)
trainFile_labels.close()

# 相关数据的定义及初始化
wordInSpam = dict()  # 垃圾邮件单词字典
wordInNormal = dict()  # 正常邮件单词字典
PofWord_spam = dict()  # P(word[i]|spam)
PofWord_normal = dict()  # P(word[i]|normal)
totalWord = trainSet[:, 1].max()  # 非重复单词总数
wordNumInSpam = 0  # 垃圾邮件单词数（重复）
wordNumInNormal = 0  # 正常邮件单词数（重复）
for i in range(totalWord + 1):
    wordInSpam[i] = 0
    wordInNormal[i] = 0
    PofWord_spam[i] = 0
    PofWord_normal[i] = 0

# 学习阶段
for i in range(trainSet.shape[0]):  # 遍历训练集矩阵中每一行
    if trainLabel[trainSet[i, 0] - 1, 0] == 1:  # 垃圾邮件
        wordNumInSpam += trainSet[i, 2]
        wordInSpam[trainSet[i, 1]] += trainSet[i, 2]
    elif trainLabel[trainSet[i, 0] - 1, 0] == 0:  # 正常邮件
        wordNumInNormal += trainSet[i, 2]
        wordInNormal[trainSet[i, 1]] += trainSet[i, 2]
# 计算P(垃圾邮件中的单词|垃圾邮件)和P(正常邮件中的单词|正常邮件)
for i in range(totalWord + 1):
    PofWord_spam[i] = (wordInSpam[i] + 1) / (wordNumInSpam + totalWord)  # 拉普拉斯平滑，分子加1避免为0，分母加上分类
    PofWord_normal[i] = (wordInNormal[i] + 1) / (wordNumInNormal + totalWord)

# 测试阶段
t_features = []
t_labels = []
testFile_features = open('test-features.txt', 'r')
testFile_labels = open('test-labels.txt', 'r')
for lines in testFile_features:
    t_features.append(list(map(lambda x: int(x), lines.split())))
testSet = np.matrix(t_features)
testFile_features.close()
for lines in testFile_labels:
    t_labels.append(list(map(lambda x: int(x), lines.split())))
testLabel = np.matrix(t_labels)
testFile_labels.close()

email = testSet[:, 0].max()
result = []
f = open("result.txt", "w")  # 将结果写入文件
spam = 0
normal = 0
for i in range(email + 1):  # 遍历所有邮件
    if i == 0:  # 邮件编号从1开始
        continue
    pSpam = 0
    pNormal = 0
    for r in range(testSet.shape[0]):  # 遍历所有行数
        if testSet[r, 0] == i:  # 只处理第i封邮件
            # 使用log形式，使得数据的差别更加明显，不加log，正确率好像是0.65
            pSpam += testSet[r, 2] * math.log(PofWord_spam[testSet[r, 1]], 10)
            pNormal += testSet[r, 2] * math.log(PofWord_normal[testSet[r, 1]], 10)
    pSpam += math.log(wordNumInSpam / (wordNumInSpam + wordNumInNormal), 10)
    pNormal += math.log(wordNumInNormal / (wordNumInSpam + wordNumInNormal), 10)
    if pSpam > pNormal:
        spam += 1
        result.append(1)  # 垃圾邮件
        print("垃圾邮件", file=f)
        print("垃圾邮件")
    else:
        normal += 1
        result.append(0)  # 正常邮件
        print("正常邮件", file=f)
        print("正常邮件")
correct = 0
for i in range(testLabel.shape[0]):
    if result[i] == testLabel[i, 0]:
        correct += 1
# 输出正确率
print("总共分析了：", len(result), "封邮件，其中垃圾邮件", spam, "封。NBC正确率为：", "%.5f" % (correct / testLabel.shape[0]), file=f)
print("总共分析了：", len(result), "封邮件，其中垃圾邮件", spam, "封。NBC正确率为：", "%.5f" % (correct / testLabel.shape[0]))
f.close()
