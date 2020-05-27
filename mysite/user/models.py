from django.db import models

# 用户表
class UserModel(models.Model):
    class Meta:
        db_table = 'tb_user'
    # 自增id
    id = models.AutoField(primary_key=True)
    # openid
    openid = models.CharField(max_length=50, unique=True)
    # 微信名
    wechat_name = models.CharField(max_length=50)
    # 学号
    stu_id = models.CharField(max_length=9, unique=True, null=True)
    # 信用值
    credit = models.IntegerField(default=90)
    # 认证状态
    auth_status = models.BooleanField(default=False)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 更新时间
    update_time = models.DateTimeField(auto_now=True)
    # 删除时间
    delete_time = models.DateTimeField(null=True)
    # # 外键约束
    # user = models.ForeignKey(StudentModel, on_delete=models.CASCADE)

    def __str__(self):
        return 'openid：' + str(self.openid) + ' 微信名：' + str(self.wechat_name)