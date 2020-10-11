from pyquery import PyQuery as pq

from urllib.request import urlopen

from bs4 import BeautifulSoup

###
# 2019研究生学术道德规范在线考试网页信息提取
###

path = "C:/Users/-PC/Desktop/考试云平台.html"
htmlfile = open(path, 'r', encoding='utf-8')
htmlhandle = htmlfile.read()

soup = BeautifulSoup(htmlhandle)

allList = soup.find_all("dl", {"class":"questionsContent"})

list = list(range(1,26)) + list(range(1,26))
i = 0

for Q_A in allList:
    questions = Q_A.find_all("span",{"class":"qq"})
    answers = Q_A.find_all("a", {"class":"words"})

    print("\n", list[i], ":", questions[0].get_text())
    i += 1
    for answer in answers:
        print(answer.get_text())


# for name in nameList:
#     print("",name.get_text())

