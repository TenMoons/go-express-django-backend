from django.db import models

# 学生信息表
class StudentModel(models.Model):
    class Meta:
        db_table = 'tb_student'
    # 自增id
    id = models.AutoField(primary_key=True)
    # 学号
    stu_id = models.CharField(max_length=9, unique=True)
    # 姓名
    stu_name = models.CharField(max_length=40)
    # 认证状态
    auth_status = models.BooleanField(default=False)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)
    # 删除时间
    delete_time = models.DateTimeField(null=True)

    def __str__(self):
        return '学号:' + str(self.stu_id) + '姓名:' + str(self.stu_name) + '认证状态' + str(self.auth_status)