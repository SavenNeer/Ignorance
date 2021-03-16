import os
import random

##参数##

#每题提供的选项数目
max_selection_num = 4
#单词合格标准:即答对learn_ok次后就不再提问该单词
learn_ok = 3
#记录单词的文件
readinfilename = "in.txt"

##命令##

#不再使用单词
killOrder = ["kill","l"]
#清屏
clearAll = ["clear","c","cls"]


########################################################

# 读取filename相对路径中的文件内的单词
def readline(filename = ""):
    words = [] #每个单词是一个dict 表示一个单词和一个列表中的多个意思
    wordslist = [] #所有单词的集合
    wordsdict = dict() #单词映射到意思的词典
    inner = open(str(filename),"r",encoding="utf-8")
    while True:
        line = inner.readline()
        if line == "":
            break
        if line[-1] == '\n':
            line = line[:-1]
        lis = line.split(" ")
        if len(lis) < 2:
            break
        word = lis[0]
        expl = lis[1:]
        pick = dict()
        pick[word] = expl
        words.append(pick)
        wordslist.append(word)
        wordsdict[word] = expl
    inner.close()
    return words,wordslist,wordsdict

#初始化记录表
def initTaker(wordslist = []):
    taker = dict()
    for oneword in wordslist:
        taker[str(oneword)] = int(0)
    return taker


#乱序生成器
def shuffle(wordslist = []):
    lis = wordslist.copy()
    random.shuffle(lis) #对lis列表中的单词乱序
    return lis

#从一个列表中随机抽取一个对象
def getOneFomeList(lister = []):
    if len(lister) == 0:
        return "null"
    lis = lister.copy()
    random.shuffle(lis)
    return lis[0]


#获取一个问题答案和解析
def getQuestion(wordslist=[],cur=0,wordsdict=dict()):
    getlis_word = []
    getlis_mean = []
    #获取考察单词的意思
    thisword = wordslist[cur]
    getlis_word.append(thisword)
    #随机获取其他几个单词
    allnum = 1
    lenth = len(wordslist)
    while allnum < max_selection_num:
        p = random.randint(0,lenth)
        ch = wordslist[int(p%lenth)]
        if ch in getlis_word:
            continue
        getlis_word.append(ch)
        allnum+=1
    getlis_word = shuffle(getlis_word)
    # print(getlis_word)
    ##下面出题
    ques = ""
    explain = "[解析] \n"
    ans = -1
    ques += ( "[ " + str(thisword) + " ]:\n" )
    for i in range(0,max_selection_num):
        curword = getlis_word[i]
        curmean = getOneFomeList(wordsdict[curword])
        ques += ( str(i+1) + ": " + str(curmean) + "\n" )
        if str(curword) == str(thisword):
            ans = i+1
        getlis_mean.append(curmean)
    ques += ("请选择:")
    ##下面给出解析
    for ch in getlis_word:
        means_list = wordsdict[ch]
        explain += ( str(ch) + ":" + str(means_list) + "\n")
    return ques,(int)(ans),explain



####主程序####

#获取单词列表
words,wordslist,wordsdict = readline(str(readinfilename))


#初始化记录表
wordstaker = initTaker(wordslist)

os.system("cls")
print("===Begin===")
#开始运行
run = True
roundnum = 1
getnewques = True
ques = ""
ans = 0
explain = ""
all_ok = 0 #全部已经完成的单词数量

while run:
    print("this is " + str(roundnum))
    roundnum+=1
    #乱序处理
    curlist = shuffle(wordslist)
    #出题程序
    lenth = len(curlist)
    i = 0
    getnewques = True
    while i < lenth and all_ok < lenth:
        myword = curlist[i] #当前需要考核的词汇
        if wordstaker[str(myword)] >= learn_ok:
            i+=1
            continue
        if getnewques:
            ques,ans,explain = getQuestion(curlist,i,wordsdict)
        #布置题目
        print(ques)
        myans = input()
        #检测
        if str(myans) in clearAll:
            os.system("cls")#清屏后回退再次考核该单词
            getnewques = False
            continue
        if str(myans) in killOrder:
            print("[KILL WORD]:" + str(myword) + "\n")
            wordstaker[str(myword)] += learn_ok
            all_ok += 1
            i+=1
            getnewques = True
            continue
        #判断答案
        if myans == str(ans):
            print("OK")
            wordstaker[myword] += 1
            if wordstaker[myword] >=learn_ok:
                all_ok+=1
        else:
            print("NO [" + str(ans) + "]")
            print(explain)
            wordstaker[myword] -= 1
        getnewques = True
        i+=1
    if all_ok == lenth:
        run = False
    else:
        run = True

print("[Over...]")





# print(words)
# print()
# print(wordslist)
# print()
# print(wordsdict)

