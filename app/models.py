"""
此中包含了所有需要创建的模型类
使用数据库进行管理
"""

# 导入db以便在实体类中使用
from . import db

class Users(db.Model):
    '''
        用户信息表
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phonenumber = db.Column(db.String(30),unique=True)
    email = db.Column(db.String(120), unique=True)
    selfinfo = db.Column(db.Text(1000),default='请输入您的个人简介')
    imgpath = db.Column(db.String(120),default=r'/static/images/uploads/default.jpg')
    isActive = db.Column(db.Boolean, default=True)

    def __init__(self, name, email,password,phonenumber,imgpath,selfinfo):
        # 用于实例对象进行赋值
        self.name = name
        self.email = email
        self.phonenumber = phonenumber
        self.password=  password
        self.imgpath = imgpath
        self.selfinfo = selfinfo

    def __repr__(self):
        return f'<User:{self.name}>'

    def to_dic(self):
        dic = {
            'id':self.id,
            'name':self.name,
            'password':self.password,
            'phonenumber':self.phonenumber,
            'email':self.email,
            'selfinfo':self.selfinfo
        }
        return dic

class Houses(db.Model):
    '''
        房屋信息表
    '''
    __tablename__ = 'houses'
    # ID
    id = db.Column(db.Integer, primary_key=True)
    # 标题
    title = db.Column(db.String(200))
    # 更新时间
    last_time = db.Column(db.String(100))
    # 价格
    price = db.Column(db.Integer)
    # 支付方式
    pay_method = db.Column(db.String(100))
    # 出租方式
    rent_pattern = db.Column(db.String(200))
    # 房屋样式
    room_type = db.Column(db.String(100))
    # 房屋面积
    room_area = db.Column(db.String(200))
    # 装修方式
    decoration_method = db.Column(db.String(200))
    # 朝向
    chaoxiang = db.Column(db.String(100))
    # 楼层
    louceng = db.Column(db.String(100))
    # 所在区域
    district = db.Column(db.String(200))
    # 所在地
    region = db.Column(db.String(200))
    # 小区
    village = db.Column(db.String(200))
    # 详细地址
    detailed_address = db.Column(db.String(200))
    # 周边地铁
    subway = db.Column(db.String(200))
    #  电话
    contactnum = db.Column(db.String(15))
    # 经纪人
    contacts = db.Column(db.String(200))
    # 描述1
    house_description1 = db.Column(db.Text(10000))
    # 链接地址
    url = db.Column(db.Text(2000))
    # 照片名字
    picture_name = db.Column(db.Text(2000), default=r'default')
    # 多对多关系
    history_users = db.relationship('Users',secondary='history',lazy='dynamic',backref=db.backref('history_houses',lazy='dynamic'))
    favor_users = db.relationship('Users',secondary='favor',lazy='dynamic',backref=db.backref('favor_houses',lazy='dynamic'))

    def __init__(self, title,last_time,chaoxiang,louceng,subway,price,pay_method,rent_pattern,room_type,room_area,decoration_method,district,region,village,contacts,detailed_address,contactnum,house_description1,url,picture_name):
        # 用于实例对象进行赋值
        self.title = title
        self.price = price
        self.pay_method = pay_method
        self.last_time=last_time
        self.louceng = louceng
        self.chaoxiang=chaoxiang
        self.subway = subway
        self.rent_pattern = rent_pattern
        self.room_type = room_type
        self.room_area = room_area
        self.decoration_method = decoration_method
        self.district = district
        self.region = region
        self.village = village
        self.detailed_address = detailed_address
        self.contactnum = contactnum
        self.contacts = contacts
        self.house_description1 = house_description1
        self.url = url
        self.picture_name = picture_name

        

    def __repr__(self):
        return f'<User:{self.title}>'

    def to_dic(self):
        dic = {
            'id':self.id,
            'title':self.title,
            'price':self.price,
            'last_time':self.last_time,
            'louceng':self.louceng,
            'chaoxiang':self.chaoxiang,
            'subway':self.subway,
            'pay_method':self.pay_method,
            'rent_pattern':self.rent_pattern,
            'room_type':self.room_type,
            'decoration_method':self.decoration_method,
            'district':self.district,
            'region':self.region,
            'village':self.village,
            'detailed_address':self.detailed_address,
            'contactnum':self.contactnum,
            'contacts':self.contacts,
            'house_description1':self.house_description1,
            'url':self.url
        }
        return dic

class History(db.Model):
    '''
        查询记录表
    '''
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    house_id = db.Column(db.Integer,db.ForeignKey('houses.id'))
    pub_date = db.Column(db.DateTime,nullable=False)




    def __init__(self, user_id,house_id,pub_date):
        # 用于实例对象进行赋值
        self.user_id = user_id
        self.house_id = house_id
        self.pub_date = pub_date


class Favor(db.Model):
    '''
        用户收藏
    '''
    __tablename__ = 'favor'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    house_id = db.Column(db.Integer,db.ForeignKey('houses.id'))
    pub_date = db.Column(db.DateTime,nullable=False)

    def __init__(self, user_id, house_id, pub_date):
        # 用于实例对象进行赋值
        self.user_id = user_id
        self.house_id = house_id
        self.pub_date = pub_date


