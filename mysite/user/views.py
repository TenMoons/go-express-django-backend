import requests
from .models import UserModel
from django.http import HttpResponse, JsonResponse
from .config import APPID, SECRET


# 根据openid查找用户信息
def findByOpenid(id):
    user = UserModel.objects.get(openid=id)
    return user


# 根据openid获取信用值
def getCreditByOpenid(request):
    print(request.GET.get('openid'))
    user = findByOpenid(request.GET.get('openid'))
    return HttpResponse(content=user.credit, status=200)



# 获取用户openid并在tb_user表中创建对应记录
def get_openid(request):
    code = request.POST.get('code')
    wechat_name = request.POST.get('wechat_name')
    print('code=', code)
    print('wechat_name=', wechat_name)
    url = "https://api.weixin.qq.com/sns/jscode2session"
    url += "?appid=" + APPID
    url += "&secret=" + SECRET
    url += "&js_code=" + code
    url += "&grant_type=authorization_code"
    r = requests.get(url)
    openid = r.json().get('openid', '')
    print('openid=', openid)

    # 查询用户是否已存在
    user = findByOpenid(openid)
    data = {
        "openid": openid,
        "credit": user.credit
    }
    # 向数据库表中增加数据
    if user is None:
        new_user = UserModel()
        new_user.openid = openid
        new_user.wechat_name = wechat_name
        new_user.save()
        data = {
            "openid": openid,
            "credit": new_user.credit
        }
    return JsonResponse(data, safe=False, status=200)
