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
    # 保存到数据库表
    order.save()
    print(order)

    return HttpResponse(content='发布成功', status=200)


# 查询所有订单返回给前端
def queryAllOrders(request):
    orders = OrderModel.objects.values().all().order_by('order_id')
    orderList = list(orders)
    orderList.reverse()
    print(orderList)
    return JsonResponse(orderList, safe=False)


