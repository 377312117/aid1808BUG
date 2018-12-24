#coding:utf-8
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import csv
import urllib
import datetime
import bs4
import os

URL = 'https://sz.58.com/chuzu/' #赶集网深圳租房页面
ADDR = 'https://sz.58.com/'  # 赶集网的域名，用来拼接补全域名

if __name__ == '__main__':
    start_page = 1  # 开始爬取的页面
    end_page = 2  # 结束页面
    price = 5       # 参考价格
    # 创建一个csv文件
    with open('result.csv', 'w', encoding = 'utf8') as f:
        # f为file对象，delimiter = ','表示为分隔符
        # csv_writer = csv.writer(f, delimiter = ',')
        print('数据读取中...............')
        while start_page <= end_page:
            start_page += 1
            print('get:{0}'.format(URL.format(page = start_page, price = price)))
            # 获取页面
            data = requests.get(URL.format(page = start_page, price = price))
            # BeautifulSoup（python的一个库）网页解析器，第一个参数是要抓取的html文本           
            # html = BeautifulSoup(response.text, 'html.parser')            
            
            soup = bs4.BeautifulSoup(data.text, "html.parser")
            urls  = soup.select('body > div.mainbox > div > div.content > div.listBox > ul > li > div.des > h2 > a')  
            if not urls:               
                break


            count = 0
            for url in urls:
                count += 1
                print("获取资源第%s次"%count)
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
                try:
                    title =title[0].text.strip()
                except:
                    title = ['无']

                # 浏览时间
                browsing_time = str(r.select('.house-update-info'))
                time_list = browsing_time.split('em')
                j = 1        
                lasttime = ' ' # 最后访问的时间        
                for i in time_list:            
                    if j == 1:
                        lasttime = i[-9:-5]
                    j+=1
                
                # 价格
                price = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > div > span.c_ff552e > b')
                try:
                    price = price[0].text.strip()
                except:
                    title = ['无']
                
                #支付规格
                pay = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > div > span.c_333 ')
                try:
                    pay = pay[0].text.strip()
                except:
                    pay = ['无']
                       
                # 租赁方式
                rent_pattern = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-of-type(1) > span:nth-of-type(2)')
                try:
                    rent_pattern = rent_pattern[0].text.strip()
                except:
                    rent_pattern = ['无']

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
                try:
                    orientation = [0].text.strip().replace('\xa0','')
                except:
                    orientation = ['无']
                
                # 所在小区
                address = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-of-type(4) > span:nth-of-type(2) > a')
                try:
                    address = address[0].text.strip()
                except:
                    address = ['无']
                # 区域
                district = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-of-type(5) > span:nth-of-type(2) > a:nth-of-type(1)')
                try:
                    district = district[0].text.strip() 
                except:
                    district = ['无']              
                

                region = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-of-type(5) > span:nth-of-type(2) > a:nth-of-type(2)')
                try:
                    region = region[0].text.strip(),
                except:
                    region = ['无']
                
                # 详细地址
                detailed_address = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-of-type(6) > span.dz')        
                try:
                    detailed_address = detailed_address[0].text.strip()  
                except:
                    detailed_address = ['无']           
                
                #电话号码
                numphone = r.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-fraud-tip > div.house-chat-phone > span')        
                try:
                    numphone = numphone[0].text.strip()
                except:
                    numphone = ['无']

                #发售人
                on_sale = r.select('#bigCustomer > p.agent-name.f16.pr > a')       
                try:
                    on_sale = on_sale[0].text.strip()
                except:
                    on_sale = ['无']

                #房屋描述
                house_description1 = r.select('body > div.main-wrap > div.house-detail-desc > div.main-detail-info.fl > div.house-word-introduce.f16.c_555 > ul > li:nth-of-type(2) > span.a2 > p:nth-of-type(1) > span > span:nth-of-type(1)')
                house_description2 = r.select('body > div.main-wrap > div.house-detail-desc > div.main-detail-info.fl > div.house-word-introduce.f16.c_555 > ul > li:nth-of-type(2) > span.a2 > p:nth-of-type(1) > span > span:nth-of-type(2)')      
                # print(house_description1)
                # print(house_description2)
                try:
                    house_description1 = house_description1[0].text.strip()                    
                except:                   
                    house_description1 = ['无']
                try:
                    house_description2 = house_description2[0].text.strip().replace('、',' ')                    
                except:
                    house_description2 = ['无']
                    
                
                picture = r.select('#housePicList > li > img')
                picture_name = ""
                for img in picture:
                    # print(img['lazy_src'])
                    img_url = img['lazy_src']
                    name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
                    defaultpath=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    pathName = defaultpath+"/static/images/downloads/" + name + ".jpg"
                    result = urllib.request.urlopen("http:" + img_url)
                    data = result.read()
                    with open(pathName, 'wb') as code:
                        code.write(data)
                    picture_name = picture_name +";"+ name


                # 拼接上前面准备好的ADDR
                # house_url = urljoin(ADDR, house.select('.title > a')[0]['href'])                
                
                #将房名、地址、价格和URL写进result.csv
                # csv_writer.writerow([
                #     title,
                #     price,
                #     pay,
                #     rent_pattern,
                #     type_room ,
                #     type_area ,
                #     finish,                    
                #     address,
                #     district,
                #     region,
                #     detailed_address,
                #     orientation,
                #     numphone,
                #     on_sale,
                #     house_description1,
                #     house_description2,
                #     _url,
                #     #picture_name
                # ])  
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
               
        print('数据读取完毕.................')     

