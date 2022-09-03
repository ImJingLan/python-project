from bs4 import BeautifulSoup
import requests,os
from urllib.parse import urlparse


def request_download(uurl,path):
    import requests
    r = requests.get(uurl)
    with open(path, 'wb') as f:
        f.write(r.content)


def auto_create_path(FilePath):
	if os.path.exists(FilePath):   ##目录存在，返回为真
	    print()
	else:
	    os.makedirs(FilePath) 

def get_prefix(url):
    a = urlparse(url)
    file_path = a.path
    file_name = os.path.basename(a.path)
    _,file_suffix = os.path.splitext(file_name)
    return file_suffix

link = 'https://www.fabiaoqing.com' #网站一般采用相对路径，此处准备前缀将其转换为绝对路径

url = input("Link:") # 输入集合地址

htmlfile = requests.get(url).text ##获取网页源码

soup = BeautifulSoup(htmlfile, "html.parser") # 分析

if(soup.select('#bqb > div:nth-child(1) > h1')[0].get_text()): #如果存在标题即合集存在

    title = soup.select('#bqb > div:nth-child(1) > h1')[0].get_text() # 获取标题

    auto_create_path("./"+title) # 创建相应文件夹

    print(title+"\n开始下载.........")


    src = soup.select('#bqb > div:nth-child(1) > div.image.pic-content > div > div > div')[0].find_all('a') # 获取所有表情单页的相对地址
    lengh = len(src) #获取数组长度（个数）

    for i in range(lengh):
        imgsrc1 = link+src[i].get("href") # 获取当前单页绝对地址
        htmlfile = requests.get(imgsrc1).text ##获取网页源码

        soup = BeautifulSoup(htmlfile, "html.parser") # 分析
        imgsrc = soup.select('.biaoqingpp')[0].get("src") #通过分析网页可得图片存储在 class 为 biaoqingpp 的 <img> 标签中 ，使用选择器选择

        request_download(imgsrc,'./'+title+"/"+title+"_"+str(i+1)+get_prefix(imgsrc)) # 下载

        print(str(i+1) + "/"+ str(lengh) + " Download Success!") #输出进度


else:
    print("pass")
