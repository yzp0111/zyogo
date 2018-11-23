#coding=utf-8
import json

import time
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *

# Create your views here.

#主界面
def index_views(request):
    return render(request,'index.html')

#登入
def login_views(request):
    #主页面
    url = '/'
    #判断请求类型,GET请求时判断是否有session和cookies
    if request.method == 'GET':
        if request.META.get('HTTP_REFERER', '/')[-10:] != '/register/':
            request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        if 'uid' in request.session and 'uphone' in request.session:
            return redirect(url)
        else:
            #有cookies时,添加session,登入状态跳转主页
            if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
                uid = request.COOKIES['uid']
                uphone = request.COOKIES['uphone']
                request.session['uid'] = uid
                request.session['uphone'] = uphone
                return redirect(url)
            #不存在信息记录时跳转登入界面
            else:
                return render(request, 'login.html')
    else:
        #获取输入的账号密码
        uphone = request.POST['uphone']
        password = request.POST['password']
        #将账号密码对比数据库信息
        uList = UserInfo.objects.filter(uphone=uphone,password=password)
        #账号密码正确
        if uList:
            uid = uList[0].id
            request.session['uid'] = uid
            request.session['uphone'] = uphone
            if 'login_from' in request.session:
                resp =  redirect(request.session['login_from'])
            else:
                resp = redirect(url)
            expires = 60*60*24*30
            if "isSaved" in request.POST:
                resp.set_cookie('uid',uid,expires)
                resp.set_cookie('uphone', uphone, expires)
            return resp
        else:
            errMsg = '用户名或密码不正确'
            return render(request,'login.html',locals())

#注册账号
def register_views(request):
    #显示注册窗口
    if request.method == 'GET':
        return render(request,'register.html')
    #将注册信息提交到数据库
    else:
        dic = {
            "uphone":request.POST['uphone'],
            "password":request.POST['password'],
            "username":request.POST['username'],
        }
        UserInfo(**dic).save()
        u = UserInfo.objects.get(uphone=request.POST['uphone'])
        #添加session登入状态
        request.session['uid']=u.id
        request.session['uphone'] = u.uphone
        #注册成功后直接跳转主页面
        return redirect('/')

#验证注册表填写的手机号是否已存在
def check_uphone_views(request):
    #获取用户在注册列表填写的uphone
    uphone = request.POST['uphone']
    #从数据库查找此号码是否存在,不存在时uList为None
    uList = UserInfo.objects.filter(uphone=uphone)
    if uList:
        dic = {
            'status':'0',
            'text':'手机号码已存在',
        }
    else:
        dic = {
            'status':'1',
            'text':'可以注册',
        }
    return HttpResponse(json.dumps(dic))

#主页面登入状态显示
def check_login_views(request):
    if 'uid' in request.session and 'uphone' in request.session:
        uid = request.session['uid']
        user = UserInfo.objects.get(id=uid)
        dic = {
            'status':'1',
            'user':json.dumps(user.to_dict())
        }
    else:
        if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
            uid = request.COOKIES['uid']
            uphone = request.COOKIES['uphone']
            request.session['uid']=uid
            request.session['uphone']=uphone
            user = UserInfo.objects.get(id=uid)
            dic = {
                'status': '1',
                'user': json.dumps(user.to_dict())
            }
        else:
            dic = {
                'status': '0',
                'text': '用户尚未登入',
            }
    print('dic是',dic)
    return HttpResponse(json.dumps(dic))

#退出登入
def logout_views(request):
    url = request.META.get('HTTP_REFERER','/')
    resp = redirect(url)
    if 'uid' in request.session and 'uphone' in request.session:
        print(request.session['uid'],request.session['uphone'],'session是',request.session)
        del request.session['uid']
        del request.session['uphone']
        if 'storename' in request.session and 'storeid' in request.session:
            del request.session['storename']
            del request.session['storeid']
    if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
        resp.delete_cookie('uid')
        resp.delete_cookie('uphone')
    return resp

#获取所有货柜基础信息,放入js文件中
def get_stores_views(request):
    #筛选数据库中可用的货柜对象
    sLists = Store.objects.filter(isActive=True)
    List = []
    for sList in sLists:
        dic = sList.to_dict() #调用model模块中函数获取货柜对象的中信息,信息为字典形式
        d = json.dumps(dic) #将字典变为json可读格式
        List.append(d)  #将货柜总表中每条数据的字典加入同一列表中
    return HttpResponse(json.dumps(List))  #将列表变为json可读格式






#进入购物车页面
def cart_views(request):
    #判别是否为主页面发出的跳转请求
    #客户直接发出的地址请求
    if request.method == 'GET':
        if 'storeid' in request.session and 'storename' in request.session:
            storename = request.session['storename']
            storeid = request.session['storeid']
            # 根据session中的货柜信息,从数据库中提取对应柜台内所有串口信息
            wLists = Windows.objects.filter(store=storeid)
            List = []
            # 循环遍历每一个窗口的信息
            for wList in wLists:
                goodsinfo = GoodsInfo.objects.filter(id=wList.goods.id)[0]  # 查找此窗口对应的商品对象
                goodsprice = goodsinfo.goods_price  # 商品价格
                goodsname = goodsinfo.goods_name  # 商品名
                goodspicture = goodsinfo.picture  # 商品图片地址
                dic = wList.to_dict()  # 调用model模块中函数获取货柜对象的中信息,信息为字典形式
                dic['goodsprice'] = str(goodsprice)  # 将decimal转化成字符串格式,便于拼接字符串
                dic['goodsname'] = goodsname
                dic['goodspicture'] = '/'+str(goodspicture)  #从数据库取出的图片地址为static/upload/goodsInfo,需要在首部加下划线
                List.append(dic)  # 将货柜总表中每条数据的字典加入同一列表中

            return render(request,'cart.html',locals())   #将货柜名传给html
        else:
            return redirect('/')
    #主页面进行通过点击地图标识的跳转操作
    else:
        storename = request.POST['storename']
        storeid = request.POST['storeid']
        request.session['storename'] = storename
        request.session['storeid'] = storeid
        return redirect('/cart/')   #通过get请求再次访问购物车页面


# 下面这个get_windows_views方法不使用了,
# 获取柜台窗口的商品信息
def get_windows_views(request):
    storeid = request.session['storeid']
    #根据session中的货柜信息,从数据库中提取对应柜台内所有串口信息
    wLists = Windows.objects.filter(store=storeid)
    List = []
    #循环遍历每一个窗口的信息
    for wList in wLists:
        goodsinfo = GoodsInfo.objects.filter(id=wList.goods.id)[0]  #查找此窗口对应的商品对象
        goodsprice = goodsinfo.goods_price  #商品价格
        goodsname = goodsinfo.goods_name  #商品名
        goodspicture = goodsinfo.picture  #商品图片地址
        dic = wList.to_dict()  #调用model模块中函数获取货柜对象的中信息,信息为字典形式
        dic['goodsprice'] = str(goodsprice)  #将decimal转化成字符串格式,让json可读
        dic['goodsname'] = goodsname
        dic['goodspicture'] = str(goodspicture)
        d = json.dumps(dic)  #将字典变为json可读格式
        List.append(d)  #将货柜总表中每条数据的字典加入同一列表中
    return HttpResponse(json.dumps(List))  #将列表变为json可读格式

#获取客户端提交的购物车信息,与服务器中信息匹对,无误后提供支付页面
def balance_views(request):
    if 'uid' in request.session and 'uphone' in request.session:
        totle_value = float(request.POST['totle_value'])  #前端计算的商品总价
        dic = request.POST['dic']  #前端返回的购物车商品信息
        list = json.loads(dic)['items']
        print(list)
        storeid = request.session['storeid']  #从session获取货柜id
        value = 0
        D = []  #用来存放价格变动的商品
        #遍历购物车中所有商品
        for pay_goods in list:
            goodsnum = int(pay_goods['input'])  #购物车中商品数量
            goodsinfo = GoodsInfo.objects.filter(goods_name=pay_goods['name'])[0] #获取商品对象
            #判断商品价格是否变动,如果变动,将商品名加入列表D中,pay_goods['price']为'￥xxx'
            different_goods = GoodsInfo.objects.filter(goods_name=pay_goods['name']).exclude(goods_price=float(pay_goods['price'][1:]))
            if different_goods:
                D.append(different_goods[0].goods_name)
            # 获取商品所在的窗口对象,要求商品数量大于等于购物车选购量
            wininfo = Windows.objects.filter(goods=goodsinfo,goods_number__gte=goodsnum)
            if wininfo:
                value += goodsinfo.goods_price * goodsnum
            else:
                data = {
                    'isOk':0,
                    'text':'%s商品数量不足,重新选购'%goodsinfo.goods_name
                }
                return HttpResponse(json.dumps(data))
        if value == totle_value:
            request.session['cart_list'] = list
            data = {
                'isOk':1,
                'text':'商品总金额为%.2f元,是否提交订单'%value
            }
            return HttpResponse(json.dumps(data))
        else:
            g = ''
            for d in D:
                g = g+d+'/'
            data = {
                'isOk': 0,
                'text': '%s商品价格发生调整,请重新确认选购'%g
            }
            return HttpResponse(json.dumps(data))
    else:
        data = {
            'isOk': 0,
            'text': '请先登入账号'
        }
        return HttpResponse(json.dumps(data))

#顾客确认要下单后,先行扣减数据库中商品,确保顾客付款后能有足够商品取出
def pay_for_views(request):
    uphone = request.session['uphone']
    order_number = str(uphone[8:])+str(time.time()//1)  #生成订单号字符串,由手机号后４位和当前时间的时间戳组成
    pay_list = request.session['cart_list']
    storename = request.session['storename']
    storeid = request.session['storeid']
    store = Store.objects.get(store_name=storename,id=storeid)
    uid = request.session['uid']
    user = UserInfo.objects.get(id=uid,uphone=uphone)
    for gds in pay_list:
        goods_price = gds['price'][1:]
        goods_name=gds['name']
        goods = GoodsInfo.objects.filter(goods_name=goods_name)
        wd = Windows.objects.get(goods=goods,store=store)
        goods_number = float(gds['input'])
        #判断商品数量是否满足
        if wd.goods_number >= goods_number:
            #扣减窗口中商品数量
            wd.goods_number -= goods_number
            #添加购物记录/待支付订单
            ShoppingRecord.objects.create(user=user,order_number=order_number,goods_name=goods_name,goods_price=goods_price,goods_number=goods_number)
            wd.save()
        #某商品数量不足时,回退已操作商品数量
        else:
            SRs = ShoppingRecord.objects.filter(order_number=order_number)
            for SR in SRs:
                goods = GoodsInfo.objects.filter(goods_name=SR.goods_name)
                wd = Windows.objects.get(goods=goods, store=store)
                wd.goods_number += SR.goods_number
                wd.save()
            SRs = ShoppingRecord.objects.filter(order_number=order_number).delete()
            return HttpResponse('结算失败,请重新下单')
    return HttpResponse('假装给了你一个支付链接')


