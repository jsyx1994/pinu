#coding:utf-8
from math import radians, cos, sin, asin, sqrt

def calc_dis(lng1, lat1, lng2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    try:
        lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    except TypeError:
        return -1000
    # haversine公式
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371.012 # 地球平均半径，单位为公里
    return c * r * 1000
    '''
    a=float(raw_input())
    b=float(raw_input())
    c=float(raw_input())
    d=float(raw_input())
    print cal_dis(a,b,c,d)
    '''
