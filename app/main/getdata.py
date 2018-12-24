import urllib
import os

import datetime
import requests
import bs4
from urllib.parse import urljoin
import csv

# 设置定时执行
from threading import Timer

from ..models import *

def get_lastdata():
    headers = {
        'Content-type': 'text/html;charset=UTF-8',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }   

    url_shouye = "https://sz.58.com/chuzu/"

    data = requests.get("https://sz.58.com/chuzu/", headers=headers)

    # data.encoding = "gbk"
    soup = bs4.BeautifulSoup(data.text, "html.parser")
    # url地址
    urls  = soup.select('body > div.mainbox > div > div.content > div.listBox > ul > li > div.des > h2 > a')  
    
    for url in urls:
        
        _url = "http:"+ url['href']
        # print(_url)
        # url_finally  = resolve(_url)
        headers = {
            'Content-type': 'text/html;charset=UTF-8',
            'User-Agent': 
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        try:
            result = requests.get(_url,headers=headers)
            r = bs4.BeautifulSoup(result.text, "html.parser")
        except:
            continue

        # 标题
        title =r.select('body > div.main-wrap > div.house-title > h1')
        # 浏览时间
        browsing_time = str(r.select('.house-update-info'))
        time_list = browsing_time.split('em')
        j = 1        
        lasttime = '' # 最后访问的时间        
        for i in time_list:            
            if j == 1:
                lasttime = i[-9:-5]
            j+=1

        # 价格
        price = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > div > span.c_ff552e > b')
        #支付规格
        pay = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > div > span.c_333 ')
        # pay = str(pay)[21:25]         
        # 租赁方式
        rent_pattern = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-of-type(1) > span:nth-of-type(2)')
        # 房屋类型
        rent_type = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-of-type(2) > span.strongbox')
        type_list = str(rent_type).split('>')        
        k = 1        
        type_room = '' # 房间户型        
        type_area = '' # 面积大小        
        finish = '' #装修风格      
        for i in type_list:            
            if k == 2:
                type_room = i[0:4]                            
                type_area = i[40:45]              
                finish = i[-11:-7].replace('\xa0','')                
            k+=1 

        # 朝向
        orientation = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-of-type(3) > span.strongbox')
        
        # 所在小区
        address = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-of-type(4) > span:nth-of-type(2) > a')
        # 区域
        district = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-of-type(5) > span:nth-of-type(2) > a:nth-of-type(1)')
        # 所在地'pay':pay[0].text.strip()
        region = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-of-type(5) > span:nth-of-type(2) > a:nth-of-type(2)')
        # 详细地址
        detailed_address = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-of-type(6) > span.dz')        
        #电话号码
        numphone = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-fraud-tip > div.house-chat-phone > span')        
        #发售人
        on_sale = r.select('#bigCustomer > p.agent-name.f16.pr > a')       
        #房屋描述
        house_description1 = r.select('body > div.main-wrap > div.house-detail-desc > div.main-detail-info.fl > div.house-word-introduce.f16.c_555 > ul > li:nth-of-type(2) > span.a2 > p:nth-of-type(1) > span > span:nth-of-type(1)')
        house_description2 = r.select('body > div.main-wrap > div.house-detail-desc > div.main-detail-info.fl > div.house-word-introduce.f16.c_555 > ul > li:nth-of-type(2) > span.a2 > p:nth-of-type(1) > span > span:nth-of-type(2)')      
        picture = r.select('#housePicList > li > img')
        picture_name = ""
        for img in picture:
            print('爬取中')
            # print(img['lazy_src'])
            imgurl = img['lazy_src']
            name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            defaultpath=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            pathName = defaultpath+"/static/images/downloads/" + name + ".jpg"
            result = urllib.request.urlopen("http:" + imgurl)
            data = result.read()
            with open(pathName, 'wb') as code:
                code.write(data)
            picture_name = picture_name +";"+ name
        try:
            last_data = {
                'url':_url,
                "title": title[0].text.strip(),
                'price': price[0].text.strip(),
                'paymethod':pay[0].text.strip(),
                'rent_pattern': rent_pattern[0].text.strip(),
                'village': address[0].text.strip(),
                'district': district[0].text.strip(),
                'region': region[0].text.strip(),
                'detailed_address':detailed_address[0].text.strip(),
                'orientation':orientation[0].text.strip().replace('\xa0',''),
                'numphone':numphone[0].text.strip(),
                'issuer':on_sale[0].text.strip(),
                'house_description1':house_description1[0].text.strip(),
                'house_description2':house_description2[0].text.strip().replace('、',''),
                'lasttime':lasttime,
                'room_type': type_room ,
                'room_area' : type_area ,
                'decoration_method' : finish,
                'picture_name':picture_name[1:],
            }
            house = Houses(
                url=_url,
                title=title[0].text.strip(),
                price=price[0].text.strip(),
                paymethod=pay[0].text.strip(),
                rent_pattern= rent_pattern[0].text.strip(),
                village= address[0].text.strip(),
                district= district[0].text.strip(),
                region= region[0].text.strip(),
                detailed_address=detailed_address[0].text.strip(),
                orientation=orientation[0].text.strip().replace('\xa0',''),
                numphone=numphone[0].text.strip(),
                issuer=on_sale[0].text.strip(),
                house_description1=house_description1[0].text.strip(),
                house_description2=house_description2[0].text.strip().replace('、',''),
                lasttime=lasttime,
                room_type= type_room ,
                room_area = type_area ,
                decoration_method = finish,
                picture_name=picture_name[1:],
                
            )
            db.session.add(house)
        except:
            continue
        print(last_data)


if __name__=="__main__":    

    get_lastdata()

