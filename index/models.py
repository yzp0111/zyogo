from django.db import models

# Create your models here.
from django.utils import timezone


class UserInfo(models.Model):
    uphone = models.CharField(max_length=20,verbose_name='手机号码')
    password = models.CharField(max_length=15,verbose_name='密码')
    username = models.CharField(max_length=20,verbose_name='昵称')
    isCustomer = models.BooleanField(default=True,verbose_name='顾客权限')
    isBusiness = models.BooleanField(default=False,verbose_name='商户权限')
    user_join_date = models.DateTimeField(default = timezone.now,verbose_name='创建时间')
    isActive = models.BooleanField(default=True,verbose_name='激活')

    def __str__(self):
        return self.username
    def to_dict(self):
        dic = {
            'uid': self.id,
            "uphone": self.uphone,
            "password": self.password,
            "username": self.username,
            "user_join_data": str(self.user_join_date),
            "isCustomer": self.isCustomer,
            "isBusiness":self.isBusiness,
            "isActive": self.isActive,
        }
        return dic

    class Meta:
        db_table = 'UserInfo'
        verbose_name = '用户基础信息'
        verbose_name_plural = verbose_name

class GoodsInfo(models.Model):
    goods_name = models.CharField(max_length=40,verbose_name='商品名称')
    goods_price = models.DecimalField(max_digits=7,decimal_places=2,verbose_name='商品价格')
    user = models.ForeignKey(UserInfo,verbose_name='卖家')
    picture = models.ImageField(upload_to='static/upload/goodsInfo',null=True,verbose_name='商品图片')  #图片格式并设置存储路径

    def __str__(self):
        return self.goods_name

    class Meta:
        db_table = 'GoodsInfo'
        verbose_name = '商品汇总'
        verbose_name_plural = verbose_name


class Store(models.Model):
    store_name = models.CharField(max_length=35,verbose_name='货柜名')
    windows_num = models.IntegerField(default=20,verbose_name='窗口数量')
    x_address = models.DecimalField(max_digits=15,decimal_places=12,verbose_name='经度位置-x')
    y_address = models.DecimalField(max_digits=15, decimal_places=12, verbose_name='纬度位置-y')
    store_join_data = models.DateTimeField(default = timezone.now,verbose_name='创建时间')
    isActive = models.BooleanField(default=True,verbose_name='是否可用')
    # store_repair = models.IntegerField()
    # store_overhaul = models.IntegerField()
    def __str__(self):
        return self.store_name

    def to_dict(self):
        dic = {
            'id':self.id,
            'name':self.store_name,
            'x':str(self.x_address),  #将decimal变为字符串格式,才能让json转换读取
            'y':str(self.y_address),  #将decimal变为字符串格式,才能让json转换读取
            'isActive':self.isActive,
        }
        return dic

    class Meta:
        db_table = 'Store'
        verbose_name = '货柜总表'
        verbose_name_plural = verbose_name

class Windows(models.Model):
    store = models.ForeignKey(Store,verbose_name='货柜')
    windows_id = models.IntegerField(verbose_name='窗口号')
    goods = models.ForeignKey(GoodsInfo,null=True,verbose_name='商品')
    goods_number = models.IntegerField(default=0,verbose_name='商品数量')
    staring_date = models.DateField(null=True,verbose_name='起租日期')
    end_date = models.DateField(null=True,verbose_name='到期日期')

    def __str__(self):
        window = str(self.store) + '/' + str(self.windows_id)
        return window

    def to_dict(self):
        dic = {
            'store':self.store.id,
            'windowsid':self.windows_id,
            'goods':self.goods.id,
            'goodsnumber':self.goods_number,
        }
        return dic

    class Meta:
        db_table = 'Windows'
        verbose_name = '货柜窗口详情'
        verbose_name_plural = verbose_name

class ShoppingRecord(models.Model):
    user = models.ForeignKey(UserInfo,verbose_name='买家')
    order_number = models.CharField(max_length=40,verbose_name='订单号')
    goods_name = models.CharField(max_length=40, verbose_name='商品名称')
    goods_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='商品价格')
    goods_number = models.IntegerField(verbose_name='商品数量')
    ispay = models.BooleanField(default=False, verbose_name='是否支付')

    def __str__(self):
        return self.order_number

    class Meta:
        db_table = 'ShoppingRecord'
        verbose_name = '交易记录'
        verbose_name_plural = verbose_name


#
# class Shoping_record(models.Model):
#   user_id = models.IntegerField()
#   store_id = models.IntegerField()
#   goods_id = models.IntegerField()
#   goods_number = models.IntegerField()
#   stransation_time = models.DateTimeField()
#
# class Good_change(models.Model):
#   user_id = models.IntegerField()
#   store_id = models.IntegerField()
#   wondows_id = models.IntegerField()
#   goods_id = models.IntegerField()
#   goods_change_number = models.IntegerField()
#   goods_change_time = models.DateTimeField()