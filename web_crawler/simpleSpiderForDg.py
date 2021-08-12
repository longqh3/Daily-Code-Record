from pyquery import PyQuery as pq

from urllib.request import urlopen

from bs4 import BeautifulSoup

###
# 中国经济与社会发展统计数据库-单本年鉴网页信息提取
###

path = "C:/Users/-PC/Desktop/中国经济与社会发展统计数据库-单本年鉴.html"
htmlfile = open(path, 'r', encoding='utf-8')
htmlhandle = htmlfile.read()

soup = BeautifulSoup(htmlhandle, features="lxml")

curr_page_record_list = soup.find_all("tr")

# print(curr_page_record_list)

# 
for single_record in curr_page_record_list:
    file_name = single_record.find_all("a",{"class":"model_a"})
    # print(file_name[0].get_text())
    answers = single_record.find_all("a", {"target":"_blank"})
    # 进一步找到具体excel下载链接
    for answer in answers:
        explicit_answer = answer.find_all("img", {"src": "./中国经济与社会发展统计数据库-单本年鉴_files/nS_down2.png"})
        if len(explicit_answer) == 1:
            correct_answer = answer.attrs['href']
            print(file_name[0].get_text(), correct_answer)
    # print("\n", list[i], ":", questions[0].get_text())
    # i += 1
    # for answer in answers:
    #     print(answer.get_text())

