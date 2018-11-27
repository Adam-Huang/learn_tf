#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-20 11点45分
# @Author  : Yue Huang ()
# @Link    : 
# @Version : 0.0.1



"""
    手机拍摄的照片宽高一般比较大，对其进行缩放和重命名，归一化
"""


import os
import cv2
import numpy as np

def img_rename(path):
    os.chdir(path)

    file = os.listdir('.')

    n = 1

    for i in file:
        oldname = path + file[n - 1]
        if n//10 == 0:
            newname = path + 'img0' + str(n) + '.jpg'
        else:
            newname = path + 'img' + str(n) + '.jpg'
        os.rename(oldname,newname)
        print(oldname,' -> ',newname)

        n += 1


def img_resize(path):
    os.chdir(path)
    file = os.listdir('.')

    for i in file:
        temp = cv2.imread(i)
        h,w,chnl = temp.shape
        temp = cv2.resize(temp,(w//2,h//2))
        cv2.imwrite(i,temp)


if __name__ == '__main__':
    img_rename('D:\\02-Python\\data\\two\\')
    img_resize('D:\\02-Python\\data\\two\\')
