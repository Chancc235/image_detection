#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, sys

path1 = 'D:\Blur\模糊检测data'  # 所需修改文件夹所在路径
dirs = os.listdir(path1)

i = 0
for dir in dirs:

    if os.path.exists(path1 + '/' +str(dir)):
        os.chdir(path1)
        os.rename(dir, str(i)+'.png')
    i += 1
