import json

from django.http import HttpResponse

from .models import AddressModel


# 显示地址
def showAddress(request):
    id = request.GET.get('openid', default='')
    my_address = AddressModel.objects.filter(openid=id)
    if len(my_address) == 0:
        return HttpResponse(status=201, content='暂时还没有地址哦~')
    address_data = []
    for i in my_address:
        address_data.append({'openid': i.openid, 'address': i.address})
    address_data_json = json.dumps(address_data, ensure_ascii=False)
    return HttpResponse(address_data_json, status=200)


# 删除地址
def deleteAddress(request):
    if request.method == "POST":
        id = request.POST.get('openid')
        # 待删除地址
        del_address = request.POST.get('address')
        address = AddressModel.objects.filter(openid=id, address=del_address).first()
        address.delete()
        return HttpResponse(content="删除成功", status=200)
    else:
        return HttpResponse(content="请求失败", status=598)


# 增加地址
def addAddress(request):
    if request.method == "POST":
        id = request.POST.get('openid')
        add_address = request.POST.get('address')
        if AddressModel.objects.filter(openid=id, address=add_address):
            return HttpResponse(content="当前地址已存在", status=599)
        try:
            twz = AddressModel.objects.create(openid=id, address=add_address)
            twz.save()
        except AddressModel.DoesNotExist as e:
            return HttpResponse("添加失败", status=400)
        return HttpResponse("添加成功", status=200)
    else:
        return HttpResponse("请求失败", status=598)
