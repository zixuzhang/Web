# -*- coding: utf-8 -*-
import re

# 全文搜索
def fulltext_search1(files,search_name):
    # 匹配文件的个数
    count = files.count()
    # 匹配关键字的总个数
    match_count = 0
    # 包含每个文件的id和file对象的二为维列表
    files_list = []
    for file in files:
        text = file.text
        filename = file.filename
        # 生成文章中的匹配关键字位置的列表
        where_list = [k.start() for k in re.finditer(re.compile(search_name), text)]
        # 文件名的匹配个数
        where_filename = [j.start() for j in re.finditer(re.compile(search_name), filename)]
        # 计算关键字匹配的总个数
        match_count = match_count + len(where_list) + len(where_filename)
        # 生成相关文件的文件信息，包含匹配个数、文件自身、文件id
        l = [len(where_list)+len(where_filename), file, str(file.id)]
        files_list.append(l)
    # 按照文件匹配个数进行反向排序
    files_list.sort(reverse=True)
    return files_list, count, match_count

# 显示全部
def fulltext_search_all(files):
    files_list = []
    count = files.count()
    match_count = 0
    for file in files:
        l = [0, file, file._id]
        files_list.append(l)
    return files_list, count, match_count

# 文件名搜索
def filename_search(files):
    files_list = []
    count = files.count()
    match_count = 0
    for file in files:
        l = [0, file, str(file.id)]
        files_list.append(l)
    return files_list, count, match_count







def fulltext_search(files,search_name):
    count = files.count()
    # 匹配关键字的上下文
    str_list =[]
    # 总匹配个数
    match_count = 0
    files_list = []
    for file in files:
        text = file.text
        # 生成文章中的匹配关键字位置的列表
        where_list = [k.start() for k in re.finditer(re.compile(search_name), text)]
        # 生成匹配关键字上下文的列表
        str_list.append(where_list)
        for i in where_list:
            str_list.append(text[i - 40:i + 40])
        match_count = match_count + len(where_list)
        l = [len(where_list), file, str_list]
        files_list.append(l)
        # files_list.sort(reverse=True)
    return files_list, count, match_count





















# # 匹配关键字个数
# 			count = files.count()
# 			match_count = 0
# 			# 包含每个文件的id和file对象的二位列表
# 			files_list = []
# 			for file in files:
# 				text = file.text
# 				#生成文章中的匹配关键字位置的列表
# 				where_list = [k.start() for k in re.finditer(re.compile(search_name),text)]
# 				#生成匹配关键字个数的列表
# 				# count_list.append(len(where_list))
# 				match_count = match_count + len(where_list)
# 				l = [len(where_list), file, file._id]
# 				files_list.append(l)
# 			files_list.sort(reverse=True)
# 			# files = fs.find({'text': re.compile(search_name)})
