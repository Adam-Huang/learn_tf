#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-26 11点01分
# @Author  : Yue Huang ()
# @Link    : 
# @Version : 0.0.1

import cv2
import numpy as np
import deal_border as db
import find_border as fb
import os


"""
    整理图书拍摄图片中，书脊分割的过程，传入图片大小建议为2K左右
"""

g_h,g_w = 0,0
m_h,m_w = 0,0


def getBookSpine(filename,pathname = '../../data/one/',isShow_src = False,
                 canny_threshold1 = 50,canny_threshold2 = 100,
                 kernel_d = np.ones((4,4),np.uint8),kernel_e = np.ones((8,8),np.uint8),isShow_de = False,isSave_de = False,
                 isShow_src_m = False,
                 isShow_line = False,
                 isSave_result = True
                 ):
    """
    参数解释：
    pathname：  文件路径，要以'/'结尾
    filename：  文件名，不需要后缀，默认为.jpg
    canny_threshold1&canny_threshold2：canny算法的阈值
    isShow_src：是否需要展示原图，以及原图的canny结果

    kernel_d：膨胀核
    kernel_e：腐蚀核

    """
    src = cv2.imread(pathname + filename + '.jpg')
    blurred = cv2.GaussianBlur(src,(3,3),0)
    gray = cv2.cvtColor(blurred,cv2.COLOR_RGB2GRAY)
    edge = cv2.Canny(gray,canny_threshold1,canny_threshold2)
    global g_h,g_w,m_h,m_w
    g_h,g_w = edge.shape

    if isShow_src == True:
        cv2.imshow('src',src)
        cv2.imshow('edge',edge)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    dilation = cv2.dilate(edge,kernel_d,iterations=1)
    erosion = cv2.erode(dilation,kernel_e,iterations=1)

    if isShow_de == True:
        cv2.imshow('dilation',dilation)
        cv2.imshow('erosion',erosion)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    if isSave_de == True:
        cv2.imwrite(filename + 'erosion' + '.jpg',erosion)

    y1,y2 = db.getROI_y(erosion)
    y1,y2 = db.Merge2ROI(y1,y2)
    index = db.findMaxROI(y1,y2)
    x1,x2 = db.getROI_x(erosion[y1[index]:y2[index]])
    src_main = src[y1[index]:y2[index],x1[0]:x2[-1]]
    edge_main = edge[y1[index]:y2[index],x1[0]:x2[-1]]
    m_h,m_w = edge_main.shape

    if isShow_src_m == True:
        cv2.imshow('src_main',src_main)
        cv2.waitKey(0)
        cv2.destroyAllWindows()    

    line_lists = fb.detect_bookedge(edge_main)
    new_list = fb.del_restline(fb.get_lineSlop(line_lists,m_h))

    if isShow_line == True:
        for i in range(len(new_list)):
            #print(new_list[i])
            cv2.line(src_main,(new_list[i][0][0],new_list[i][0][1]),(new_list[i][1][0],new_list[i][1][1]),(0,0,255),3)
        cv2.imshow('src_main',src_main)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    rect_lists = fb.get_bookspine(src_main,edge_main,new_list)
    if isSave_result == True:
        new_dir = filename + '_zero'
        os.mkdir(new_dir)
        for i in range(len(rect_lists)):
            wirtename = './' + new_dir + '/' + 'img_' + str(i) + '.jpg'
            cv2.imwrite(wirtename,rect_lists[i])
    return rect_lists

if __name__ == '__main__':
    import os
    path = 'D:\\02-Python\\data\\two\\'
    os.chdir(path)
    files = os.listdir('.')
    for file in files:
        filename = file.split('.')[0]
        getBookSpine(filename = filename,pathname = path)
