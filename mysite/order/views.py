from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import OrderModel


# 接收前端提发布的代取订单
def getPublishOrder(request):
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
def queryAllOrders(request):
    orders = OrderModel.objects.values().all().filter(~Q(order_status=-1)).filter(~Q(order_status=-2)).order_by('order_id')
    orderList = list(orders)
    orderList.reverse()
    return JsonResponse(orderList, safe=False)


# 接单
def takeOrder(request):
    id = request.POST.get('order_id')
    taker_openid = request.POST.get('taker_openid')
    taker_wechat = request.POST.get('taker_wechat')
    taker_time = request.POST.get('taker_time')
    taker_credit = request.POST.get('taker_credit')
    print(id,' ', taker_openid, ' ', taker_wechat, ' ', taker_time)
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
def queryOrderDetail(request):
    id = request.GET.get('order_id')
    user_openid = request.GET.get('user_openid')
    # 获取该订单
    order = OrderModel.objects.get(order_id=id)
    if user_openid not in [order.rel_openid, order.taker_openid]:
        return HttpResponse(content='没有查看权限', status=7000)
    identity = 0  # 默认身份为发布者(0)，1为接单者
    if user_openid == order.taker_openid:
        identity = 1
    privacy = [{
        "receive_name": order.receive_name,
        "receive_phone": order.receive_phone,
        "express_code": order.express_code,
    }, {
        "identity": identity,
    }
    ]
    print(privacy)
    return JsonResponse(data=privacy, safe=False, status=200)


# 接单者确认送达
def taker_confirm(request):
    id = request.POST.get('order_id')
    order = OrderModel.objects.get(order_id=id)
    # 修改订单状态为已送达(2)
    order.order_status = 2
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
