import sys

sys.path.append("..")

from .models import StudentModel
from django.http import HttpResponse
from user.models import UserModel


# 根据学号查找学生信息
def findById(id):
    student = StudentModel.objects.get(stu_id=id)
    return student


# 更新学生认证信息
def updateAuthStatus(stu_id):
    student = findById(stu_id)
    student.auth_status = 1
    student.save()


# 更新用户表的认证信息，并同步学号
def updateUserInfo(openid, stu_id):
    user = UserModel.objects.get(openid=openid)
    user.stu_id = stu_id
    user.auth_status = 1
    print(user)
    user.save()

# 该用户是否认证
def findByOpenid(openid):
    user = UserModel.objects.get(openid=openid)
    return user.auth_status == 1


# 学生身份认证,接收前端传递的数据
def auth(request):
    openid = request.POST.get('openid')
    stu_id = request.POST.get('id')
    cur_student = findById(stu_id)
    # 判断是否重复认证
    if cur_student.auth_status == 1:
        return HttpResponse(content='该学号已被绑定!', status=400)
    if findByOpenid(openid):
        return HttpResponse(content='请勿重复认证!', status=400)
    # 更新学生表认证状态
    updateAuthStatus(stu_id)
    updateUserInfo(openid, stu_id)
    return HttpResponse(content='认证成功', status=200)
