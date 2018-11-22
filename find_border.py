#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-16 10点21分
# @Author  : Yue Huang ()
# @Link    : 
# @Version : 0.0.1

"""
    一种像素级图书边缘检测算法，基于的是Canny边缘检测后的效果
"""

def detect_bookedge(img):
    """
    图书边缘查找算法，从视觉上看，图书多是向左倾斜放置的，且角度不应偏离y轴45度以上
    参数:
        边缘检测后的图像
    返回值：
        所有在图书边缘上的点所构成的list
    """
    h,w = img.shape
    y = h//2
    line_lists = []
    for i in range(w):
        if img[y,i] > 200:
            bUpFind = True
            bDownFind = True
            up_x,down_x = i,i
            line = [[y,i]]
            protect_break_up = 0
            protect_break_down = 0
            for j in range(1,h//3):
                if bUpFind:
                    for k in range(-1,2):
                        if up_x+k < 1 or up_x+k > w-2:
                            bUpFind = False
                            break
                        #越界，直接返回
                        
                        if img[y-j,up_x+k] > 200:
                            up_x += k
                            line.insert(0,[y-j,up_x])
                            if k == 1:
                                protect_break_up += 1
                            else:
                                protect_break_up = 0

                            if protect_break_up > 2:
                                #连续3次是在第三位置找到的，可以认为此时找到的已经是错误的线了，应立刻停止
                                bUpFind = False
                            break
                        else:
                            if k == 1:
                                bUpFind = False

                if bDownFind:
                    for k in range(-1,2):
                        if down_x-k < 1 or down_x-k > w-2:
                            bDownFind = False
                            break
                        ##返回
                        
                        if down_x-k < w-1 and img[y+j,down_x-k] > 200:
                            down_x -= k
                            line.append([y+j,down_x])
                            if k == 1:
                                protect_break_down += 1
                            else:
                                protect_break_down = 0

                            if protect_break_down > 2:
                                #连续3次是在第三位置找到的，可以认为此时找到的已经是错误的线了，应立刻停止
                                bDownFind = False
                            break
                        else:
                            if k == 1:
                                bDownFind = False

                if bDownFind == False and bUpFind == False:
                    break

            if len(line) > h//6:
                line_lists.append(line)

    return line_lists


def get_lineSlop(line_lists,h):
    """
    通过这个直线首尾两点确定一条直线
    返回值：
          直线与图片上下边缘相交点的坐标
          斜率 k
    """
    new_lists=[]
    for i in range(len(line_lists)):
        k = (line_lists[i][-1][1] - line_lists[i][0][1])/(line_lists[i][-1][0] - line_lists[i][0][0])
        b = line_lists[i][-1][1] - k*line_lists[i][-1][0]
        start_ = (int(b),0)
        end_ = (int(k*h+b),h)
        new_lists.append([start_,end_,k])
    return del_restline(new_lists)


def get_lineRegression(line_lists):
    """
    用一元线性回归的方法找到这个直线的最佳拟合，然后再找到其与图片上下边缘的交点坐标
    """
    pass


def del_restline(lists):
    """
    有些空隙大，会被认为是两条直线，删除相距比较近的线，简化一下
    """
    nnlist=[]
    bPass = False
    for i in range(len(lists) - 1):
        if bPass == False:
            if (lists[i+1][0][0] - lists[i][0][0] < 10) and (abs(lists[i+1][-1] - lists[i][-1]) < 0.01):
                nnlist.append([((lists[i+1][0][0] + lists[i][0][0])//2,lists[i+1][0][1]),
                           ((lists[i+1][1][0] + lists[i][1][0])//2,lists[i+1][1][1]),
                          (lists[i+1][-1] + lists[i][-1])/2])
                bPass = True
            else:
                nnlist.append(lists[i])
        else:
            bPass = False
            
    nnlist.append(lists[-1])
    
    return nnlist

def get_bookspine(edgeimg,newlists):
    """
    直线找到书的轮廓后需要排除书架以及其他干扰，
    输入是canny后的图像和上述new_lists
    返回是矩形区域
    """    
    h,w = edgeimg.shape
    step = h//12
    rect_lists = []
    line_list = []
    crosspoint_lists=[]
    for j in range(len(newlists)):
        crosspoint = []
        for i in range(1,12):
            y = step*i
            x = y * newlists[j][-1] + newlists[j][0][0]
            crosspoint.append(max(int(x),0))
            ##求出所有的交点
        crosspoint_lists.append(crosspoint)
        if len(crosspoint_lists) > 1:
            sum_list = []
            ##先判断是否有交叉，有交叉就删除斜率较小的那个
            for i in range(1,12):
                #if crosspoint_lists[j][i] - crosspoint_lists[j - 1][i] < 1:
                #    break
                temp = edgeimg[step*i,crosspoint_lists[j - 1][i-1]:crosspoint_lists[j][i - 1]]
                if temp.sum() > 255*2:
                    sum_list.append(1)
                else:
                    sum_list.append(0)
            if sum(sum_list) > 3:
                line_list.append((j-1,j))
                left = max(min(newlists[j-1][0][0],newlists[j-1][1][0]),0)
                lefte = max(newlists[j][0][0],newlists[j][1][0])
                rect_lists.append([left,0,lefte,h])
    
    return rect_lists

if __name__ == '__main__':
    import cv2

    edge_ = cv2.imread('edge_1.jpg',cv2.IMREAD_GRAYSCALE)
    h,w = edge_.shape
    lines = detect_bookedge(edge_)
    new_list = del_restline(get_lineSlop(lines,h))
    #rect_lists = get_bookspine(edge_,new_list)
    
