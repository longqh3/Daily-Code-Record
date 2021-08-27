###
# 2020网页doi信息提取与pdf下载
# 仅限定当前网页：https://academic.oup.com/ageing/issue#1081122-5880843
# 需要将网页下载至本地再进行处理（未来再进行完善）
###

### 依赖项部分
# pip install pyquery
# pip install scidownl
# pip install bs4

from pyquery import PyQuery as pq
from urllib.request import urlopen
from bs4 import BeautifulSoup

### 路径部分
# 本地网页路径
htmlPath = "C:\\Users\-PC\Desktop\Issues _ Age and Ageing _ Oxford Academic.html"
# pdf文件保存文件夹路径
pdf_folder_path = "C:\\Users\-PC\Desktop\paper_download"

### 功能部分
# 进行网页doi信息提取
def html_doi_extract(htmlPath):
    htmlfile = open(htmlPath, 'r', encoding='utf-8')
    htmlhandle = htmlfile.read()

    soup = BeautifulSoup(htmlhandle)

    allList = soup.find_all("div", {"class":"ww-citation-primary"})

    doi_list = []
    for citation_info in allList:
        doi = citation_info.find_all("a")
        doi_list.append(doi[0].get_text())
        print("已提取进入list的doi地址：", doi[0].get_text())
    print("共计提取%d个doi记录，准备进行pdf下载......"%(len(doi_list)))

    return(doi_list)

# 调用第三方scihub下载工具进行pdf下载
# 应用SciDownl工具：https://github.com/Tishacy/SciDownl
def doi_pdf_download(doi_list, out):
    # 更新scihub的下载列表
    from scidownl.update_link import *

    # Use crawling method to update available Scihub links.
    update_link(mod='c')

    # 依据提取的doi列表进行pdf下载
    from scidownl.scihub import *

    success_count = 0
    error_list = []
    for doi in doi_list:
        try:
            SciHub(doi, out).download(choose_scihub_url_index=3)
            success_count += 1
        except:
            print("%s所对应pdf文件下载失败，请人工检查对应文章情况！"%(doi))
            error_list.append(f"{doi}所对应pdf文件下载失败，请人工检查！")
            continue
    print(error_list)
    print("共计提取%d个doi记录，%d个pdf文件已下载成功！"%(len(doi_list), success_count))

if __name__ == "__main__":
    doi_list = html_doi_extract(htmlPath)
    doi_pdf_download(doi_list, pdf_folder_path)
