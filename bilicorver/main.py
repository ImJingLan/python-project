'''
Bilibili Video Info Downloader

Repository:https://gitee.com/imjinglan/bilicover/

CopyRight (c) ImJingLan 2021

LICENSE:MIT LICENSE

'''

import requests
import json
import os
import sys
import re

def starts():
    os.system("title BiliCover v2.0 By ImJingLan")

def mkcoverdir(PATH):#新建文件夹
    if not os.path.isdir(PATH):
        os.mkdir(PATH)

def imgdownload(url,name): #封面下载
    cover = requests.get(url)
    with open('./'+name+'/cover.jpg', 'wb') as pic:
        pic.write(cover.content)

def av2bv(av):#AV号转BV号
    info = requests.get('https://api.bilibili.com/x/web-interface/view?aid='+av).text
    info = json.loads(info)
    if info.get('code') == 0:
        vid = info['data'].get('bvid') # 返回的正确格式BV号
        return vid
    else:
        print("找不到该AV号")
        print("CODE:"+str(info.get('code'))+" MESSAGE:"+info.get('message'))#服务器返回无视频消息
        os.system("pause")
        sys.exit()

def bvcheck(vid):#检查BV号是否合法
    if vid.startswith('BV',0,2) or vid.startswith('bV',0,2) or vid.startswith('Bv',0,2) or vid.startswith('bv',0,2):# 硬检测是否为BV开头
        if len(vid) == 12:
            info = info = requests.get('https://api.bilibili.com/x/web-interface/view?bvid='+vid).text
            info = json.loads(info)
            if info.get('code') == 0:
                return True
            else:
                print("找不到该BV号")
                print("CODE:"+str(info.get('code'))+" MESSAGE:"+info.get('message'))
                os.system("pause")
                sys.exit()
                

        else:
            print('这不是一个合法的BV号, BV号应为12位字符串')
            os.system("pause")
            sys.exit()
    else:
        print('这不是一个合法的BV号，BV号应为 BV 开头')
        os.system("pause")
        sys.exit()

def copyright(x):
    if x==1:
        return "是"
    else:
        return "否"

def videoinfo(info):
    a=info['data'].get('title')+"\n"
    a=a+"AV号: av"+str(info['data'].get('aid'))+"\n"
    a=a+"BV号: "+info['data'].get('bvid')+"\n"
    a=a+'播放量: '+str(info['data']['stat'].get("view"))+"\n"
    a=a+'弹幕: '+str(info['data']['stat'].get("danmaku"))+"\n"
    a=a+'点赞: '+str(info['data']['stat'].get("like"))+"\n"
    a=a+'硬币: '+str(info['data']['stat'].get("coin"))+"\n"
    a=a+'收藏: '+str(info['data']['stat'].get("favorite"))+"\n"
    a=a+'分享: '+str(info['data']['stat'].get("share"))+"\n"
    a=a+"类型: "+info["data"].get("tname")+"\n"
    a=a+"是否原创: "+copyright(info["data"].get("copyright"))+"\n"
    a=a+"视频最高分辨率: "+str(info['data']["dimension"].get("width"))+"x"+str(info['data']["dimension"].get("height"))+"\n"
    desc = info["data"].get('desc')
    desc = desc.replace("\r","\n")
    if info['data'].get('staff'):
        a=a+"是否联合投稿: 是\n"
        staff=info['data']['staff']
        maxlen = len(staff)
        a=a+"Staffs:\n"
        for i in range(maxlen-1):
            a=a+"    "+staff[i].get('title')+": "+staff[i].get('name')+"\n"
    else:
        a=a+"是否联合投稿: 否\n"
        if info['data']['owner']:
            a=a+'UP主: '+ info['data']['owner'].get('name')+"\n"
    a=a+"\n简介:\n"+desc

    return a

if __name__ == "__main__":
    starts()
    print("请选择视频链接类型\n1.BV号    2.av号")
    status = input()

    if(status == '2'):
        av = input('av号:')
        av = re.sub('av', '', av, flags=re.IGNORECASE)
        bvid=av2bv(av)
    
    if(status == '1'):
        bvid = input("BV号:")

    if(status != '1' and status != '2'):
        print("请输入正确的类型")
        os.system("pause")
        sys.exit()

    if(bvcheck(bvid)):
        mkcoverdir(bvid)
        rawjson = requests.get("https://api.bilibili.com/x/web-interface/view?bvid="+bvid).text
        rawjson = json.loads(rawjson)
        cover = rawjson["data"].get("pic")
        imgdownload(cover,bvid)
        info = videoinfo(rawjson)
        with open("./"+bvid+"/info.txt",mode='w', encoding='utf-8') as f:
            f.write(info)
        print("文件已保存至 "+"./"+bvid+"/\n其中封面文件为cover.jpg，视频信息为info.txt")
        os.system("pause")
