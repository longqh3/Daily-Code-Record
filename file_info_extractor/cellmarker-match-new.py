# 读取cell_type对应marker，简化数据规模
cell_type_dict = {}
with open(r"C:\\Users\\-PC\Desktop\\cellmarker_test.txt", "r") as f:
    for line in f:
        cell_type, gene_list_str = line.rstrip().split("\t")
        # 若cell_type不存在于dict的keys中，则初始化该item
        if not cell_type_dict.keys().__contains__(cell_type):
            cell_type_dict[cell_type] = set()
        # 将marker信息以set形式存储于字典中
        cell_type_dict[cell_type] = cell_type_dict[cell_type].union(set(gene_list_str.split(",")))

# 读取marker对应cell_type，输出最终文件
marker_dict = {}
for cell_type in cell_type_dict.keys():
    marker_set = cell_type_dict[cell_type]
    for marker in marker_set:
        # 若marker不存在于dict的keys中，则初始化该item
        if not marker_dict.keys().__contains__(marker):
            marker_dict[marker] = []
        # 将cell_type信息以list形式存储于字典中
        marker_dict[marker].append(cell_type)

# 保证输出文件的稳定性，需要进行sort
with open(r"C:\\Users\\-PC\Desktop\\cellmarker_final.txt", 'w') as f:
    # 指定marker的输出顺序
    marker_dict_keys_sorted = sorted(marker_dict.keys())
    # 根据输出顺序逐个写出
    for marker in marker_dict_keys_sorted:
        line_str_list = [marker, ",".join(sorted(marker_dict[marker]))]
        f.write("\t".join(line_str_list)+"\n")
    f.close()