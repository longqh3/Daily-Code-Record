###
# 中国经济与社会发展统计数据库-单本年鉴网页信息提取
# 遇到问题：
# 1. 采取lazy-load形式，因而此处选择取巧，直接获取POST请求内的真实信息
# 2. 需要IP认证下载，经过验证后发现，使用IDM、浏览器可以下载，迅雷则无法下载，
# 因此猜测是cookie在发挥作用，request模块中加入cookie后即可正常下载
###

import re

from urllib.request import urlopen

from bs4 import BeautifulSoup

import requests

import os

import time

# 输入：读取为文本信息的html信息
# 输出：当前页面下的所有下载链接（以文件名-链接形式存储于dict中）
def html_extractor_for_dg(html_info):
    # 应用解析器解析html信息
    soup = BeautifulSoup(html_info, features="lxml")
    # 提取指定标签信息
    curr_page_record_list = soup.find_all("tr")
    # 遍历网页表格内每个记录、解析并予以记录
    name_link_dict = {}
    for single_record in curr_page_record_list:
        file_name = single_record.find_all("a",{"class":"model_a"})
        # print(file_name[0].get_text())
        answers = single_record.find_all("a", {"target":"_blank"})
        # 进一步获取具体excel下载链接
        for answer in answers:
            explicit_answer = answer.find_all("img", {"src": "/resources/design/images/nS_down2.png"})
            if len(explicit_answer) == 1:
                correct_answer = answer.attrs['href']
                name_link_dict[file_name[0].get_text().strip()] = "https://data.cnki.net" + correct_answer
                print(file_name[0].get_text(), "https://data.cnki.net" + correct_answer)
    return(name_link_dict)

# 输入：读取为文本信息的html信息（初始页面，不重要）
# 输出：可供下载的所有年份-链接信息（存储于dict中）
def year_iter_info_extractor_for_dg(init_html_info):
    # 应用解析器解析当前html信息
    soup = BeautifulSoup(init_html_info, features="lxml")
    # 获取初始页面内的所有年份-请求链接信息，存储于dict中
    curr_year_record_list = soup.find_all("div", {"class": "s_year clearfix"})[0].find_all("a")
    curr_year_link_dict = {}
    for single_record in curr_year_record_list:
        curr_year_link_dict[single_record.get_text()] = "https://data.cnki.net" + (single_record.attrs['href'])
    return(curr_year_link_dict)

    # print("\n", list[i], ":", questions[0].get_text())
    # i += 1
    # for answer in answers:
    #     print(answer.get_text())

# 输入：读取为文本信息的html信息
# 输出：可供遍历的页数记录（数字形式存储）
def page_iter_info_extractor_for_dg(link):
    url = "https://data.cnki.net/Yearbook/PartialGetCatalogResult"
    data = {"ybcode": link.split("/")[-1],
            "entrycode": "",
            "page": 1,
            "pagerow": 20}
    res = requests.post(url=url, data=data)
    html_info = res.text
    # html_info = urlopen(link).read()
    # 应用解析器解析当前html信息
    soup = BeautifulSoup(html_info, features="lxml")
    # 正则表达式提取可供遍历的页数记录
    curr_page_info = soup.find_all("span", {"class": "s_p_listl"})[0].contents[0].strip() # 为"共有记录186条\xa0\xa0共10页"样式
    numbers = re.findall("\d+", curr_page_info)  # 输出结果为列表
    return(numbers[1])

# 输入：初始链接
# 输出：存储年份-文件名-下载链接信息的结果dict
def entry_function_for_dg(init_link):
    init_html_info = urlopen(init_link).read()
    # 获取所有年份-链接信息
    year_link_dict = year_iter_info_extractor_for_dg(init_html_info)
    # 初始化存储年份-文件名-下载链接信息的结果dict
    year_file_name_download_link_dict = {}
    # 遍历每个年份
    for single_year in year_link_dict.keys():
        # 初始化当前年份结果
        year_file_name_download_link_dict[single_year] = {}
        page_num = page_iter_info_extractor_for_dg(year_link_dict[single_year])
        print(f"开始提取{single_year}对应文件名-下载链接信息，共{page_num}页信息待提取......")
        # 遍历所有页，将信息存储于结果dict中（需要采用request进行请求）
        for single_page in range(1, int(page_num)+1):
            url = "https://data.cnki.net/Yearbook/PartialGetCatalogResult"
            data = {"ybcode": year_link_dict[single_year].split("/")[-1],
                    "entrycode": "",
                    "page": single_page,
                    "pagerow": 20}
            res = requests.post(url=url, data=data)
            year_file_name_download_link_dict[single_year].update(html_extractor_for_dg(res.text))
    return(year_file_name_download_link_dict)

# 输入：已整理好的年份-文件名-下载链接信息的结果dict
# 输入2：指定结果存储文件夹目录
# 输入3：cookie文件位置
# 输出：将所有信息下载至指定文件夹内
def iter_downloader_for_dg(year_file_name_download_link_dict, result_folder_loc, cookie_loc):
    # 初始化cookie便于下载
    cookie_info = open(cookie_loc, 'r')  # 打开所保存的cookies内容文件
    cookies = {}  # 初始化cookies字典变量
    for line in cookie_info.read().split(';'):  # 按照字符：进行划分读取
        # 其设置为1就会把字符串拆分成2份
        name, value = line.strip().split('=', 1)
        cookies[name] = value  # 为字典cookies添加内容
    # 遍历每一年的所有下载链接
    for single_year in year_file_name_download_link_dict.keys():
        print(f"开始处理{single_year}相应信息.......")
        # 新建文件夹保存相应信息
        single_year_folder_loc = os.path.join(result_folder_loc, single_year)
        os.mkdir(single_year_folder_loc)
        # 遍历所有下载链接进行下载
        for file_name in year_file_name_download_link_dict[single_year].keys():
            print(f"开始下载{file_name}对应文件")
            download_address = year_file_name_download_link_dict[single_year][file_name] # 获取下载地址
            f = requests.get(download_address, cookies=cookies) # 把下载地址发送给requests模块
            # 开始下载文件并保存至本地
            with open(os.path.join(single_year_folder_loc, file_name+".xls"), "wb") as file:
                file.write(f.content)
            # 间隔1秒再进行下载，避免反爬机制介入
            # time.sleep(1)
        print(f"{single_year}所有信息下载完成")
        print("="*100)

# 入口函数
if __name__ == '__main__':
    year_file_name_download_link_dict = entry_function_for_dg("https://data.cnki.net/Yearbook/Single/N2021020056")
    # 自行指定结果存储文件夹目录、从浏览器中获取的cookie信息文件
    iter_downloader_for_dg(year_file_name_download_link_dict, "C:\\Users\\-PC\Desktop\\test", "C:\\Users\-PC\\Desktop\\test\\cookie.txt")