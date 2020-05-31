import requests
from .models import UserModel
from django.http import HttpResponse
from .config import APPID, SECRET

'''
根据openid查找用户
'''


# 根据openid查找用户信息
def findByOpenid(openid):
    user = UserModel.objects.get(openid=openid)
    print(user)
    return user


'''
获取用户openid并在tb_user表中创建对应记录
'''


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
    #  user = findByOpenid(openid)
    # 向数据库表中增加数据
    # if user is None:
    user = UserModel()
    user.openid = openid
    user.wechat_name = wechat_name
    user.save()
    print(user)
    return HttpResponse(content=openid, status=200)
