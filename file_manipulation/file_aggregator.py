import os

import argparse

parser=argparse.ArgumentParser(description="整合文件夹内所有文件为一个文件")
# parser.add_argument('--raw_RNA_mutations', '-r' ,choices=[5,10,20],default=5,type=int,help='Number of epochs.')
# Generic parameter
parser.add_argument('--folder_path', help='合并的目标文件夹路径')
parser.add_argument('--output_file_path', help='输出文件路径')

args = parser.parse_args()

# 合并由新闻联播爬虫获取到的每日信息
# https://github.com/xiaoyu2er/xwlb
def xwlb_aggregator(folder_path, output_file_path):

    with open(output_file_path, 'w', encoding="utf-8") as f:
        # 获取所有子文件
        for root,dirs,files in os.walk(folder_path):
            for filename in files:
                print(f"开始处理{filename}文件内相应信息")
                # 单个子文件路径
                file_path = os.path.join(root, filename)
                # 打开子文件并保存相应信息
                with open(file_path, 'r', encoding="utf-8") as t:
                    f.write(t.read()+"\n")
    print("信息处理完成！")


if __name__ == "__main__":
    xwlb_aggregator(args.folder_path, args.output_file_path)