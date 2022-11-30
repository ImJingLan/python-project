from bs4 import BeautifulSoup
import requests,os
from urllib.parse import urlparse

def acfun_parse(parse):
    data = {
        "parse" : "https://www.acfun.cn/bangumi/" + parse,
        "t" : ""
    }
    return requests.post('https://www.leesoar.com/acfun',data=data).text

if __name__ == '__main__':
    htmlfile = acfun_parse("aa5024879")
    soup = BeautifulSoup(htmlfile, "html.parser") # 分析
    
    title = soup.select('#parse > div:nth-child(3) > a')[0].attrs # 获取标题
    print(title['href'])
