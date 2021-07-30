import os
import argparse
# description参数可以用于描述脚本的参数作用，默认为空
parser=argparse.ArgumentParser(description="For a given tar-zipped file, create a new folder with its own name and add suffixes into all deflated files. ")
parser.add_argument('--tar_zipped_file','-t',required=True,help='Specify location of tar-zipped file.')
parser.add_argument('--file_suffix','-s',required=True,help='Specify your demand for file suffix rename.')

args=parser.parse_args()
print(args)
print(args.toy,args.num_epochs,args.num_layers)

def createNewFolder(file_location):
    # 获取root文件夹路径
    root_folder_loc = os.path.split(file_location)[0]
    # 获取子文件夹名称和路径
    subfolder_name = os.path.split(file_location)[0].split(".")[0]
    subfolder_loc = os.path.join(root_folder_loc, subfolder_name)
    # 新建存放解压后文件的文件夹
    os.system(f"mkdir -p {subfolder_loc}")
    return subfolder_loc

def tarInfoScan(file_location, file_suffix):
    # 读取tar文件内相应信息
    tar_info = os.popen('tar -ztvf /home/lqh/software/eSNV-Detect_1.0.tar.gz').readlines()
    # TODO 未来考虑支持文件夹内文件重命名
    # 以列表形式获取其内每一个文件信息
    tar_file_list_before = [single_info.split()[-1] for single_info in tar_info]
    # 添加suffix后


if __name__ == "__main__":
    # 新建文件夹
    subfolder_loc = createNewFolder(args.tar_zipped_file)
    # 读取tar压缩文件信息


# tar -zxvf /root/etc.tar.gz -C /etc/shadow # 解压到指定文件夹