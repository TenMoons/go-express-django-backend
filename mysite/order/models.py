from django.db import models

class OrderModel(models.Model):
    class Meta:
        db_table = 'tb_order'
    # 18位订单编号
    order_id = models.CharField(primary_key=True, max_length=18)
    # 发布者openid
    rel_openid = models.CharField(max_length=50)
    # 发布者微信名
    rel_wechat = models.CharField(max_length=50)
    # 发布者信用积分
    rel_credit = models.IntegerField(null=True)
    # 发布时间
    publish_time = models.DateTimeField()
    # 收件人姓名
    receive_name = models.CharField(max_length=40)
    # 收件人手机号
    receive_phone = models.CharField(max_length=11)
    # 收货地址
    receive_address = models.CharField(max_length=100)
    # 快递站点
    express_station = models.CharField(max_length=50)
    # 取件码
    express_code = models.CharField(max_length=20)
    # 跑腿费
    express_fee = models.FloatField()
    # 快递大小
    express_size = models.CharField(max_length=40)
    # 截止时间
    end_time = models.DateTimeField()
    # 备注
    remark = models.CharField(max_length=200, null=True)
    # 订单状态 0 -创建, 1 -已接单, 2 -已送达, 3 -已完成（发布者确认送达）, 4 -已评价, -1 -发布者取消, -2 -系统取消
    order_status = models.IntegerField(default=0)
    # 接单者openid
    taker_openid = models.CharField(max_length=50, null=True)
    # 接单者微信名
    taker_wechat = models.CharField(max_length=50, null=True)
    # 接单者信用积分
    taker_credit = models.IntegerField(null=True)
    # 接单时间
    taker_time = models.DateTimeField(null=True)
    # 完成时间，若取消，则为取消时间
    finish_time = models.DateTimeField(null=True)
    # 送达凭证，由接单者确认送达后上传
    confirm_photo = models.CharField(max_length=255, null=True)

    def __str__(self):
        return '订单id:' + str(self.order_id) + '发布者openid:' + str(self.rel_openid) + \
               '发布者微信名:' + str(self.rel_wechat) + '发布时间:' + str(self.publish_time) + \
            '收件人姓名:' + str(self.receive_name) + '收货地址:' + str(self.receive_address) + \
            '接单人openid:' + str(self.taker_openid) + '接单时间:' + str(self.taker_time)
