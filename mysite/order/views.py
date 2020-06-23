import base64
import datetime
import hmac
import json
import time
from hashlib import sha1

from django.db.models import Q
from django.http import HttpResponse, JsonResponse

from .config import QINIU_ACCESS_KEY, QINIU_SECRET_KEY, QINIU_BUCKET_NAME
from .models import OrderModel
from qiniu import Auth


# 接收前端提发布的代取订单
def get_publish_order(request):
    # 接收数据
    order_id = request.POST.get('order_id')
    rel_openid = request.POST.get('rel_openid')
    rel_wechat = request.POST.get('rel_wechat')
    publish_time = request.POST.get('publish_time')
    receive_name = request.POST.get('receive_name')
    receive_phone = request.POST.get('receive_phone')
    receive_address = request.POST.get('receive_address')
    express_station = request.POST.get('express_station')
    express_code = request.POST.get('express_code')
    express_fee = request.POST.get('express_fee')
    express_size = request.POST.get('express_size')
    end_time = request.POST.get('end_time')
    remark = request.POST.get('remark')
    rel_credit = request.POST.get('rel_credit')

    order = OrderModel()
    order.order_id = order_id
    order.rel_openid = rel_openid
    order.rel_wechat = rel_wechat
    order.publish_time = publish_time
    order.receive_name = receive_name
    order.receive_phone = receive_phone
    order.receive_address = receive_address
    order.express_station = express_station
    order.express_code = express_code
    order.express_fee = express_fee
    order.express_size = express_size
    order.end_time = end_time
    order.remark = remark
    order.order_status = 0
    order.rel_credit = rel_credit
    # 保存到数据库表
    order.save()
    print(order)

    return HttpResponse(content='发布成功', status=200)


# 查询所有订单返回给前端
def query_all_orders(request):
    all_orders = OrderModel.objects.all()
    print(all_orders)
    current_time = datetime.datetime.now()
    for o in all_orders:
        if o.end_time < current_time:
            o.order_status = -1  # 超时无人接单，系统自动取消
            o.save()
    orders = OrderModel.objects.values().all().filter(~Q(order_status=-1)).filter(~Q(order_status=-2)).order_by(
        'order_id')
    orderList = list(orders)
    orderList.reverse()
    print(orderList)
    return JsonResponse(orderList, safe=False)


# 接单
def take_order(request):
    id = request.POST.get('order_id')
    taker_openid = request.POST.get('taker_openid')
    taker_wechat = request.POST.get('taker_wechat')
    taker_time = request.POST.get('taker_time')
    taker_credit = request.POST.get('taker_credit')
    print(id, ' ', taker_openid, ' ', taker_wechat, ' ', taker_time)
    # 根据order_id查找订单
    order = OrderModel.objects.get(order_id=id)
    # 修改订单状态1：已接单
    order.order_status = 1
    order.taker_openid = taker_openid
    order.taker_wechat = taker_wechat
    order.taker_time = taker_time
    order.taker_credit = taker_credit
    order.save()
    print(order)
    return HttpResponse(status=200)


# 查询指定order_id的订单详情信息，并判断当前用户是否有查看详情的权利
def query_order_detail(request):
    id = request.GET.get('order_id')
    user_openid = request.GET.get('user_openid')
    # 获取该订单
    order = list(OrderModel.objects.values().all().filter(order_id=id))
    thisOrder = order[0]
    print(order)
    if user_openid not in [thisOrder['rel_openid'], thisOrder['taker_openid']]:
        thisOrder['receive_name'] = '*' * len(thisOrder['receive_name'])
        thisOrder['receive_phone'] = '*' * len(thisOrder['receive_phone'])
        thisOrder['express_code'] = '*' * len(thisOrder['express_code'])
        return JsonResponse(data=order, safe=False, status=201)
    return JsonResponse(data=list(order), safe=False, status=200)


# 接单者确认送达
def taker_confirm(request):
    id = request.POST.get('order_id')
    time = request.POST.get('finish_time')
    print(time)
    order = OrderModel.objects.get(order_id=id)
    # 修改订单状态为已送达(2)
    order.order_status = 2
    order.finish_time = time
    order.save()
    return JsonResponse(data=order.order_status, safe=False, status=200)


# 发布者确认送达
def rel_receipt(request):
    id = request.POST.get('order_id')
    order = OrderModel.objects.get(order_id=id)
    # 修改订单状态为已完成(3)
    order.order_status = 3
    order.save()
    return JsonResponse(data=order.order_status, safe=False, status=200)


# 发布者取消订单
def rel_cancel(request):
    id = request.POST.get('order_id')
    order = OrderModel.objects.get(order_id=id)
    # 修改订单状态为发布者取消订单(-1)
    order.order_status = -1
    order.save()
    return JsonResponse(data=order.order_status, safe=False, status=200)


# 好评，增加信用值
def rel_evaluate_positive(request):
    id = request.POST.get('order_id')
    order = OrderModel.objects.get(order_id=id)
    order.order_status = 4
    if order.rel_credit != 100:
        order.rel_credit = order.rel_credit + 5
    order.save()
    ret = [{
        "order_status": order.order_status,
        "credit": order.rel_credit
    }]
    return JsonResponse(data=ret, safe=False, status=200)


# 差评，减少信用值
def rel_evaluate_negative(request):
    id = request.POST.get('order_id')
    order = OrderModel.objects.get(order_id=id)
    order.order_status = 4
    if order.rel_credit != 0:
        order.rel_credit = order.rel_credit - 10
    order.save()
    return JsonResponse(data=order.order_status, safe=False, status=200)


# 查询当前用户全部订单
def query_my_all_orders(request):
    user_id = request.GET.get('user_openid')
    existorders = OrderModel.objects.values().all().filter(order_status__gte='0')  # 过滤已被取消的订单
    myorders_rel = existorders.filter(rel_openid=user_id).order_by('order_id')  # filter(rel_openid=user_id )all()
    myorders_tak = existorders.filter(taker_openid=user_id).order_by('order_id')
    myorderList = list(myorders_rel)
    for item in myorders_tak:
        myorderList.append(item)
    # myorderList.append(myorders_tak)
    myorderList.reverse()
    print(myorderList)
    print(user_id)
    return JsonResponse(myorderList, safe=False)


# 查询当前用户接收的订单
def query_my_take(request):
    user_id = request.GET.get('user_openid')
    existorders = OrderModel.objects.values().all().filter(order_status__gte='0')  # 过滤已被取消的订单
    myorders_tak = existorders.filter(taker_openid=user_id).order_by('order_id')  # filter(taker_openid = user_id)all()
    takeorderList = list(myorders_tak)
    # myorderList.append(myorders_tak)
    takeorderList.reverse()
    print(takeorderList)
    print(user_id)
    return JsonResponse(takeorderList, safe=False)


# 查询当前用户待派送订单
def query_my_send(request):
    user_id = request.GET.get('user_openid')
    myorders_rel = OrderModel.objects.values().filter(rel_openid=user_id).order_by(
        'order_id')  # filter(rel_openid=user_id )all()
    myorders_tbs = myorders_rel.filter(order_status='1').order_by('order_id')
    tbsorderList = list(myorders_tbs)
    # myorderList.append(myorders_tak)
    tbsorderList.reverse()
    print(tbsorderList)
    print(user_id)
    return JsonResponse(tbsorderList, safe=False)


# 查询当前用户待收货订单
def query_my_receive(request):
    user_id = request.GET.get('user_openid')
    myorders_rel = OrderModel.objects.values().filter(rel_openid=user_id).order_by(
        'order_id')  # filter(rel_openid=user_id )all()
    myorders_tbr = myorders_rel.filter(order_status='2').order_by('order_id')
    tbrorderList = list(myorders_tbr)
    # myorderList.append(myorders_tak)
    tbrorderList.reverse()
    print(tbrorderList)
    print(user_id)
    return JsonResponse(tbrorderList, safe=False)


# 查询当前用户已完成订单
def query_my_finish(request):
    user_id = request.GET.get('user_openid')
    myorders_rel = OrderModel.objects.values().filter(rel_openid=user_id).order_by(
        'order_id')  # filter(rel_openid=user_id )all()
    myorders_fin = myorders_rel.filter(order_status='3').order_by('order_id')
    finorderList = list(myorders_fin)
    # myorderList.append(myorders_tak)
    finorderList.reverse()
    print(finorderList)
    print(user_id)
    return JsonResponse(finorderList, safe=False)


# 查询当前用户发布的订单(未被接收,我发布的）
def query_my_publish(request):
    user_id = request.GET.get('user_openid')
    myorders_rel = OrderModel.objects.values().filter(rel_openid=user_id).order_by(
        'order_id')  # filter(rel_openid = user_id)all()
    myorders_tbtak = myorders_rel.filter(order_status='0').order_by('order_id')
    relorderList = list(myorders_tbtak)
    # myorderList.append(myorders_tak)
    relorderList.reverse()
    print(relorderList)
    print(user_id)
    return JsonResponse(relorderList, safe=False)


# 查询有关用户订单的数量返回给前端
def query_my_order_count(request):
    user_id = request.GET.get('user_openid')
    # 订单状态 0 -创建, 1 -已接单, 2 -已送达, 3 -已完成（发布者确认送达）, 4 -已评价, -1 -发布者取消, -2 -系统取消
    countList = []
    myorders_rel = OrderModel.objects.values().filter(rel_openid=user_id)
    myorders_tbs = list(myorders_rel.filter(order_status='1'))
    countList.append(len(myorders_tbs))  # 待派送
    # print(len(myorders_tbs))
    myorders_tbr = list(myorders_rel.filter(order_status='2'))
    countList.append(len(myorders_tbr))  # 待收货
    # myorders_fin = list(myorders_rel.filter(order_status='3'))
    # countList.append(len(myorders_fin))
    myorders_tak = list(OrderModel.objects.values().filter(taker_openid=user_id).order_by(
        'order_id'))  # filter(taker_openid = user_id)all()
    countList.append(len(myorders_tak))  # 我接收的
    myorderList = list(myorders_rel.filter(order_status='0'))
    countList.append(len(myorderList))  # 已创建
    print(countList)
    print(user_id)
    return JsonResponse(countList, safe=False)


# 返回upload file token
def get_token(request):
    q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
    my_policy = {
        'scope': QINIU_BUCKET_NAME,
        'deadline': 3600,
    }
    token = q.upload_token(QINIU_BUCKET_NAME, key=None,
                           expires=3600, policy=my_policy)
    print(token)
    return JsonResponse(token, status=200, safe=False)


# 设置订单送达凭证
def set_confirm_photo(request):
    url = request.POST.get('url')
    id = request.POST.get('order_id')
    print(url)
    order = OrderModel.objects.get(order_id=id)
    order.confirm_photo = url
    order.order_status = 2 # 已送达
    order.save()
    return HttpResponse(status=200)
