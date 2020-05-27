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
    return user


'''
获取用户openid并在tb_user表中创建对应记录
'''


def get_openid(request):
    code = request.POST.get('code')
    wechat_name = request.POST.get('wechat_name')
    print('code=', code)
    print('wechat_name=', wechat_name)
    print('APPID=', APPID)
    url = "https://api.weixin.qq.com/sns/jscode2session"
    url += "?appid=" + APPID
    url += "&secret=" + SECRET
    url += "&js_code=" + code
    url += "&grant_type=authorization_code"
    r = requests.get(url)
    openid = r.json().get('openid', '')

    # 向数据库表中增加数据
    user = UserModel()
    user.openid = openid
    user.wechat_name = wechat_name
   # user.save()
    print('openid=', openid)
    print(user)
    return HttpResponse(content=openid, status=200)


## 订单编号+发布者openid+发布者微信名+发布时间+收件人姓名+收件人手机号+取件地址+取件码+跑腿费+快递大小+截止时间+备注+订单状态+接单者openid+接单者编号+接单时间+完成时间