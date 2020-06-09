from django.db import models

class AddressModel(models.Model):
    class Meta:
        db_table = 'tb_address'
    # 自增id
    id = models.AutoField(primary_key=True)
    # 用户openid
    openid = models.CharField(max_length=50)
    # 地址
    address = models.CharField(max_length=50)

    def __str__(self):
        return 'openid:' + str(self.openid) + ' 地址:' + str(self.address)

