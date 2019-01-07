#coding:utf-8
import csv
import urllib
import requests
import bs4
import random
import time
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from lxml import etree
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# 导入model
from .models import *

URL = 'http://sz.ganji.com/zufang/pn'  # 赶集网深圳租房页面
ADDR = 'http://sz.ganji.com/'          # 赶集网的域名，用来拼接补全域名

def ganji_house_data():    

    List = [                    
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)'},
        {'Content-type': 'text/html;charset=UTF-8','User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'}                
    ]
    headers = random.choice(List)

    # headers = {
    #     'Content-type': 'text/html;charset=UTF-8',
    #     'User-Agent': 
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    # }      

    start_page = int(input("请输入起始页:"))
    end_page = int(input("请输入终止页:"))
    
    # 创建一个csv文件
    with open('赶集网2.csv', 'w', encoding = 'utf-8') as f:

        # f为file对象，delimiter = ',' 表示为分隔符
        csv_writer = csv.writer(f, delimiter = ',')
        print('数据读取中......')
                     
        for pg in range(start_page,end_page+1):
            # 拼接完整URL地址             
            page = URL + str(pg)+'/'  
            print('************************（∩＿∩）*****************************')                   
            print(page)
            print('\n'+"第%d页爬取成功" % pg+'\n') 

            # 获取页面            
            data = requests.get(page,headers=headers)
            data.encoding = 'utf-8'
            # BeautifulSoup（python的一个库）网页解析器，第一个参数是要抓取的html文本        
            soup = bs4.BeautifulSoup(data.text, "html.parser")

            # 获取页面
            res = requests.get(page,headers=headers)
            res.encoding = "utf-8"
            html = res.text 

            parseHtml = etree.HTML(html)
            urls = parseHtml.xpath('//dd[@class="dd-item title"]/a/@href')
            
            count = 0
            # i = 2
            # while i <= 40:
            #     u =  '#f_mew_list > div.f-main.f-clear.f-w1190 > div.f-main-left.f-fl.f-w980 > div.f-main-list > div > div:nth-of-type('+str(i)+') > dl > dd.dd-item.title > a' 
            #     print(u)
            #     i = i+1
            #     urls  = soup.select(u)
            #     print(urls)

            #     if not urls:               
            #         break
                
            for url in urls:
                time.sleep(1)
                count += 1   
                if url[0:6] != 'https:':
                    url = 'https:'+url 

                print(url)
                print('\n'+"正在获取资源，遍历第%s次"%count+'\n')

                # _url = url['href'] 
                                                                                  
                try:
                    result = requests.get(url,headers=headers)
                    r = bs4.BeautifulSoup(result.text, "html.parser")                    
                except:
                    continue

                                  
                            
                # 标题
                title =r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > p > i')                                  
                try:
                    title =title[0].text.strip()                    
                except:                        
                    continue
                print('标　　题:',title)   

                # 更新时间
                lasttime = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > div.card-status.f-clear > ul > li')
                try:
                    lasttime = lasttime[0].text.strip()
                except:
                    lasttime = '无'
                print('更新时间:',lasttime)
                
                # 价格
                price = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > div.er-card-pay > div > span.price')
                try:
                    price = int(price[0].text.strip())
                except:
                    continue
                print('价　　格:',price)

                # 押金
                payment = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > div.er-card-pay > div > span.unit')
                try:
                    payment = payment[0].text.strip()
                except:
                    payment = '无'
                print('押　　金:',payment)
                    
                # 出租类型:整租／合租
                lease_type = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list.f-clear > li:nth-of-type(2) > span.content')
                try:
                    lease_type = lease_type[0].text.strip().split()[0]                                           
                except:
                    lease_type = '无'
                print('出租类型:',lease_type)                                  
                    
                # 户型        
                room = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list.f-clear > li:nth-of-type(1) > span.content')
                try:
                    room = room[0].text.strip()
                except:
                    room = '无'
                print('户　　型:',room)

                # 面积           
                area = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list.f-clear > li:nth-of-type(2) > span.content')
                try:
                    area = area[0].text.strip().split()[1]
                except:
                    area = '无' 
                print('面　　积:',area)

                # 装修         
                finish = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list.f-clear > li:nth-of-type(5) > span.content')
                try:
                    finish = finish[0].text.strip()
                except:
                    finish = '无'
                print('装　　修:',finish)              

                # 朝向
                chaoxiang = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list.f-clear > li:nth-of-type(3) > span.content')
                try:
                    chaoxiang = chaoxiang[0].text.strip()
                except:
                    chaoxiang = '无'                    
                print('朝　　向:',chaoxiang)

                #楼层
                louceng = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list.f-clear > li:nth-of-type(4) > span.content')
                try:
                    louceng = louceng[0].text.strip()
                except:
                    louceng = '无'                    
                print('楼　　层:',louceng)
                
                # 小区
                xiaoqu = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list-two.f-clear > li:nth-of-type(1) > span.content > a > span')
                try:
                    xiaoqu = xiaoqu[0].text.strip()
                except:
                    xiaoqu = '无'
                print('小　　区:',xiaoqu)
                
                # 周边地铁
                subway = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list-two.f-clear > li.er-item.er-item-cursor.f-fl > div > span')
                try:
                    subway = subway[0].text.strip()
                except:
                    subway = '无'
                print('周边地铁:',subway)

                # 区县
                county = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list-two.f-clear > li:nth-of-type(3) > span.content')
                try:
                    county = county[0].text.strip().split('-')[0]  
                except:
                    county = '无'
                print('区　　县:',county)

                # 街道           
                street  = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list-two.f-clear > li:nth-of-type(3) > span.content')
                try:
                    street = street [0].text.strip().split('-')[1]                   
                except:
                    street = '无'
                print('街　　道:',street)              
                
                # 详细地址
                address = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-top > ul.er-list-two.f-clear > li:nth-of-type(3) > span.content')        
                try:
                    address = address[0].text.strip().split('-')[2]   
                except:
                    address = '无'
                print('详细地址:',address)                        
                
                # 电话号码
                numphone = r.select('#full_phone_show > div.phone > a')        
                try:
                    numphone = numphone[0].text.strip()
                except:
                    numphone = '无'
                print('电话号码:',numphone)

                # 发售人
                on_sale = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-info.f-fr > div.card-user > div > div > div.name > a')       
                try:
                    on_sale = on_sale[0].text.strip()
                except:
                    on_sale = '无'
                print('出售用户:',on_sale)

                # 详情介绍
                introduce = r.select('#js-house-describe > div > div')
                try:
                    a = introduce[0].text.strip().replace('<span>','')
                    b = a.replace('</span>','')
                    c = b.replace('</br>','')
                    d = c.replace('<p>','')
                    e = d.replace('</p>','')
                    d = e.replace('\xa0','')
                    introduce = d.replace('0,','')
                except:                    
                    introduce = '无' 
                print('详情介绍:',introduce)                
                print('*******************我是美丽的分隔符小可爱（＊≧▽≦＊）*********************')
                print()          
                                
                # 获取图片             
                
                # picture = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-img.f-fl.js-basic-imgs-big.basic-imgs > div > div.small-img > ul > li > a > img')
                picture = r.select('#f_detail > div.f-card.f-er-card.f-w1190.f-clear.f-b30 > div.card-img.f-fl.js-basic-imgs-big.basic-imgs > div > div.small-img > ul > li')
                # print(picture)
                picture_name = ""
                for image in picture:
                    # print(img['lazy_src'])
                    img_url = image['data-image']
                     
                    # print(img_url)                   
                    name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
                    # print(name)
                    pathName = "./app/static/images/downloads/" + name + ".jpg"
                    result = urllib.request.urlopen("https:" + img_url)
                    data = result.read()

                    with open(pathName, 'wb') as code:
                        code.write(data)
                    picture_name = picture_name +";"+ name                        
                                        
                
                # 将房名、地址、价格和URL等写进result.csv
                csv_writer.writerow([
                    title,          # 标　　题
                    lasttime,       # 更新时间
                    price,          # 价　　格
                    payment,        # 押　　金
                    lease_type,     # 出租类型:整租／合租
                    room,           # 户　　型
                    area,           # 面　　积
                    finish,         # 装　　修
                    chaoxiang,      # 朝　　向
                    louceng,        # 楼　　层             
                    xiaoqu,         # 小　　区
                    subway,         # 周边地铁
                    county,         # 区　　县
                    street,         # 街　　道
                    address,        # 详细地址               
                    numphone,       # 电话号码
                    on_sale,        # 出售用户
                    introduce,      # 详情介绍                   
                    url,            # 访问链接
                    picture_name    # 图片文件名
                ])
                yz_house = Houses.query.filter_by(title=title).first()
                if xiaoqu != '无' or not yz_house:
                    house = Houses(
                        title=title,
                        price=price,
                        pay_method=payment,
                        last_time=lasttime,
                        louceng=louceng,
                        chaoxiang=chaoxiang,
                        subway=subway,
                        rent_pattern=lease_type,
                        room_type=room,
                        room_area=area,
                        decoration_method=finish,
                        district=county,
                        region=street,
                        village=xiaoqu,
                        detailed_address=address,
                        contactnum=numphone,
                        contacts=on_sale,
                        house_description1=introduce,
                        url=url,
                        picture_name=picture_name
                    )
                    db.session.add(house)
                    db.session.commit()
                else:
                    print('插入重复或数据缺失')
                    continue
                          
                
        print('数据读取完毕......')     

if __name__ == '__main__':
    ganji_house_data()