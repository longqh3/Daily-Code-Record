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

# 遍历表格内每个记录并予以记录
name_link_dict = {}

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
            name_link_dict[file_name[0].get_text().strip()] = correct_answer

    # print("\n", list[i], ":", questions[0].get_text())
    # i += 1
    # for answer in answers:
    #     print(answer.get_text())

# 更换页面
import requests
url = "https://data.cnki.net/Yearbook/Single/N2008070078"
data = {"ybcode":"N2008070078",
        "entrycode":"",
        "page":5,
        "pagerow":20}
res = requests.post(url=url,data=data)
print(res.text)

# 获取当前页面内的年、页面信息
curr_year_record_list = soup.find_all("div", {"class":"s_year clearfix"})[0].find_all("a")
curr_year_link_dict = {}
for single_record in curr_year_record_list:
    curr_year_link_dict[single_record.get_text()] = single_record.attrs['href']

# 获取当前页面的页数信息
curr_page_info = soup.find_all("span", {"class":"s_p_listl"})[0].contents[0].strip()
import re
number = re.findall("\d+",curr_page_info)    # 输出结果为列表
print(number)

# 更换页面
url = "	https://data.cnki.net/Yearbook/PartialGetCatalogResult"
data = {"ybcode":"N2008070078",
        "entrycode":"",
        "page":5,
        "pagerow":20}
res = requests.post(url=url,data=data)
print(res.text)

# 保存网页内容于本地
init_html_info = urlopen("https://data.cnki.net/Yearbook/Single/N2008070078", timeout=2).read()
soup = BeautifulSoup(init_html_info, features="lxml")
with open("C:\\Users\\-PC\Desktop\\test.html", "w", encoding='utf-8') as f:
    f.write(res.text)

# 读取网址
import urllib
page = urllib.request.urlopen("https://data.cnki.net/Yearbook/Single/N2006010750")
contents = page.read()
#获得了整个网页的内容也就是源代码
print(contents)

# 下载文件
## 新建文件夹
import os
os.mkdir("C:\\Users\-PC\Desktop\\test")
#引用 requests文件
import requests
f=open(r"C:\Users\-PC\Desktop\test\cookie.txt",'r')#打开所保存的cookies内容文件
cookies={}#初始化cookies字典变量
for line in f.read().split(';'):   #按照字符：进行划分读取
    #其设置为1就会把字符串拆分成2份
    name,value=line.strip().split('=',1)
    cookies[name]=value  #为字典cookies添加内容
#下载地址
Download_addres='https://data.cnki.net/download/excel?filecode=N2021020056000004'
#把下载地址发送给requests模块
f=requests.get(Download_addres, cookies=cookies)
#下载文件
with open(os.path.join("C:\\Users\-PC\Desktop\\test", "1-1 分地区年末人口数.xls"),"wb") as code:
     code.write(f.content)