#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-16 09点53分
# @Author  : Yue Huang ()
# @Link    : 
# @Version : 0.0.1

"""
    定义了一些找出ROI的方法，针对的是腐蚀后的图片
"""

def getROI_x(img):
    """
    检测x方向上为空的列，可以找到y方向上可能的间隔
    img 为膨胀腐蚀后的image
    """
    x1=[]
    x2=[]
    #初始化2个列表，x1,y1 为ROI区域左上角；x2y2为ROI区域右下角
    firstzero1 = False
    if img[:,0].sum() > 255*10:
        #如果第一行有值，表明ROI可能跨越本图片，需要从边缘开始提取
        x1.append(0)
        firstzero1 = True 
    
    h,w = img.shape
    for i in range(w):
        if img[:,i].sum() < 255*10:
            if firstzero1 == True:
                #print(i)
                x2.append(i)
                firstzero1 = False
        else:
            if firstzero1 == False:
                #print(i)
                x1.append(i)
                firstzero1 = True
    #同理，如果最后一行有值，表明ROI可能跨越本图片，需要从边缘开始提取
    if img[:,w-1].sum() > 255*10:
        x2.append(w-1)
    return x1,x2

def getROI_y(img):
    """
    检测y方向上为空的列，可以找到x方向上可能的间隔
    img 为膨胀腐蚀后的image
    """
    y1=[]
    y2=[]
    #初始化2个列表，x1,y1 为ROI区域左上角；x2y2为ROI区域右下角
    firstzero1 = False
    if img[0,:].sum() > 255*10:
        #如果第一行有值，表明ROI可能跨越本图片，需要从边缘开始提取
        y1.append(0)
        firstzero1 = True 
    
    h,w = img.shape
    for i in range(h):
        if img[i,:].sum() < 255*10:
            if firstzero1 == True:
                #print(i)
                y2.append(i)
                firstzero1 = False
        else:
            if firstzero1 == False:
                #print(i)
                y1.append(i)
                firstzero1 = True
    #同理，如果最后一行有值，表明ROI可能跨越本图片，需要从边缘开始提取
    if img[h-1,:].sum() > 255*10:
        y2.append(h-1)
    return y1,y2

def DelNeighborLine(x1,x2,threshold=19):
    """
    如果x轴上，两个起点离的太近，就认为这是一个物体，不是边界
    """
    n_x1=[x1[0]]
    n_x2=[]
    for i in range(len(x1)-1):
        if x1[i+1] - x1[i] > threshold:
            n_x1.append(x1[i+1])
            n_x2.append(x2[i])
    n_x2.append(x2[len(x1)-1])
    return n_x1,n_x2

def MergeNeighborLine(x1,x2,threshold=19):
    """
    如果一个范围太窄的边界，
    就说这个边界其实不应该存在，是上下两个范围的一部分，所以将其融合起来
    """
    n_x1=[]
    n_x2=[]
    passone = False
    for i in range(len(x1)):
        if x2[i] - x1[i] > threshold:
            if passone == False:
                n_x1.append(x1[i])
            else:
                passone = False
            n_x2.append(x2[i])
        else:
            n_x2.pop()
            passone = True
    return n_x1,n_x2


def DelSamllROI(x1,x2,threshold = 5):
    """
    如果有些ROI连5个像素点都达不到，就有可能是边缘的干扰，要删除
    但是这个算法也有风险，比如主体周围的干扰？
    """
    y1 = []
    y2 = []
    for i in range(len(x2)):
        if x2[i] - x1[i] > threshold:
            y1.append(x1[i])
            y2.append(x2[i])
    return y1,y2
    
def findMaxROI(x1,x2):
    """
    图书识别这个应用场景下，图书书脊纹理复杂，在膨胀之后往往能打通连通域，
    可以直接找到最大的ROI，基本上就是图书主体所在的位置了
    """
    max_temp=0
    index = -1
    for i in range(len(x2)):
        if x2[i]-x1[i] > max_temp:
            max_temp = x2[i] - x1[i]
            index = i
    return index

def Merge2ROI(x1,x2,threshold = 2):
    """
    实际应用中发现，有时候（书教少），x方向y轴上分割太窄了，所以要将两个ROI合并
    """
    n_x1=[]
    n_x2=[]
    bPass = False
    for i in range(len(x1) - 1):
        if x1[i + 1] - x2[i] < threshold:
            if bPass != True:
                n_x1.append(x1[i])
            bPass = True
        else:
            if bPass != True:
                n_x1.append(x1[i])
            else:
                bPass = False
            n_x2.append(x2[i])
    if bPass != True:
        n_x1.append(x1[-1])
    n_x2.append(x2[-1])
    
    return n_x1,n_x2


if __name__ == '__main__':
    y1 = [182, 190, 251, 298, 491, 717, 801, 811, 847, 852, 1071, 1074, 1094]
    y2 = [188, 246, 294, 490, 715, 745, 802, 838, 848, 853, 1073, 1091, 1169]
    x1,x2 = Merge2ROI(y1,y2)
    print(x1,x2)
