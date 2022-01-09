# python D:\Codes\github\Daily-Code-Record\web_crawler\complex_website_info_extractor.py  --single_time 20220104 --chat_room_id 135582562975745 --data_type live

# python D:\Codes\github\Daily-Code-Record\web_crawler\complex_website_info_extractor.py  --batch_time 20220102_20220107 --chat_room_id 135582562975745 --data_type message

###
# 网页聊天室直播+留言内容下载
# 需要指定提取日期（范围）和提取数据类型
###

# 直接根据网页中朴素的get请求来进行数据获取

import pandas as pd
import requests
import json
import os
import time
import datetime

import argparse

parser=argparse.ArgumentParser(description="根据指定日期（范围）和所需数据类型完成数据提取和导出")
# parser.add_argument('--raw_RNA_mutations', '-r' ,choices=[5,10,20],default=5,type=int,help='Number of epochs.')
# Generic parameter
parser.add_argument('--single_time', type=int, help='所需提取时间，格式如20220104')
parser.add_argument('--batch_time', help='所需提取时间范围，格式如20220102_20220107')
parser.add_argument('--chat_room_id', type=int, help='聊天室ID，格式如135582562975745')
parser.add_argument('--data_type', help='所需提取数据类型，格式如live或message')
parser.add_argument('--output_folder', help='数据导出路径，默认为当前目录', default=os.path.split(os.path.realpath(__file__))[0])

args = parser.parse_args()

# 功能部分
# 当前设计思路是先初步了解数据规模，再一锅端获取所有信息
def get_info_extractor(url, params):
    # 首先获取待提取的数据规模
    ## 将页面size定为1
    params['pageSize'] = 1
    res = requests.get(url=url,params=params)
    print(f"{params['day']}待提取数据条数为{json.loads(res.text)['data']['total']}")

    # 休息1s（避免爬虫被拦截）
    time.sleep(1)

    # 最终获取所有待提取数据
    ## 修改页面size
    params['pageSize'] = json.loads(res.text)['data']['total']
    ## 发送请求
    res = requests.get(url=url,params=params)
    ## 获取有信息量的列
    data_info = pd.DataFrame(json.loads(res.text)['data']['list'])[['nickName', 'bodiesBean', 'sendTimestamp']]
    ## 处理列信息便于展示
    data_info['chatMessage'] = data_info['bodiesBean'].apply(lambda x: x['msg'] if x['type']=="txt" else x['url'])
    data_info['sendTimestamp'] = data_info['sendTimestamp'].apply(lambda x: time.strftime("%H:%M:%S",time.localtime(int(x/1000))))
    ## 得到最终信息并导出
    data_info = data_info[['sendTimestamp', 'nickName', 'chatMessage']]

    print(f"{params['day']}信息提取成功！")

    return data_info

if __name__ == "__main__":
    
    url = "https://live.azavt.com/chatroom/historyMsgPage"

    # 若为时间范围
    if args.batch_time:
        # 获取起始、终止时间、时间间隔
        date_start = datetime.date(*time.strptime(args.batch_time.split("_")[0],'%Y%m%d')[:3])
        date_end = datetime.date(*time.strptime(args.batch_time.split("_")[1],'%Y%m%d')[:3])
        delta = date_end - date_start
        # 初始化字典以存储结果信息
        result_dict = {}
        # 遍历相应时间
        for i in range(delta.days+1):
            # 获取当前时间
            current_date = date_start + datetime.timedelta(days=i)
            current_time = int(current_date.strftime('%Y%m%d'))
            # 提供针对性参数字典
            params = {"isManager": "", 
            "chatRoomId": args.chat_room_id, 
            "day": current_time, 
            "orderby": "SEND_TIMESTAMP~ASC", 
            "pageNum": 1, 
            "pageSize": 0}
            # 将结果保存于字典中
            result_dict[current_time] = get_info_extractor(url, params)

            # 休息1s
            time.sleep(1)
        
        outputFileName = os.path.join(args.output_folder, f"{args.batch_time}.message.xlsx")

        with pd.ExcelWriter(outputFileName) as writer:
            for single_date in result_dict.keys():
                result_dict[single_date].to_excel(writer, index=False, sheet_name=f"{single_date}")

    # 若为单个时间
    else:
        # 根据数据类型决定待提取数据
        if args.data_type == "message":
            params = {"isManager": "", 
            "chatRoomId": args.chat_room_id, 
            "day": args.single_time, 
            "orderby": "SEND_TIMESTAMP~ASC", 
            "pageNum": 1, 
            "pageSize": 0}

            data_info = get_info_extractor(url, params)

            outputFileName = os.path.join(args.output_folder, f"{args.single_time}.message.xlsx")
            data_info.to_excel(outputFileName, index=False)