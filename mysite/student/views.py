from .models import StudentModel
from django.http import HttpResponse


# 根据学号查找学生信息
def findById(id):
    student = StudentModel.objects.get(stu_id=id)
    return student

# 更新学生认证信息
def updateAuthStatus(stu_id):
    student = findById(stu_id)
    student.auth_status = 1
    student.save()
    # return HttpResponse(content='更新认证状态', status=201)


'''
学生身份认证,接收前端传递的数据
'''


def auth(request):
    # TODO : 更新用户表的认证状态
    openid = request.POST.get('openid')
    stu_id = request.POST.get('id')
    stu_name = request.POST.get('name')
    cur_student = findById(stu_id)
    # 判断是否重复认证
    if cur_student.auth_status == 1:
        return HttpResponse(content='请勿重复认证', status=400)
    # 更新学生表认证状态
    updateAuthStatus(stu_id)

    return HttpResponse(content='认证成功', status=200)