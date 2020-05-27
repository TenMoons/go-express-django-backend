# Generated by Django 3.0.6 on 2020-05-27 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('order_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('rel_openid', models.CharField(max_length=50, unique=True)),
                ('rel_wechat', models.CharField(max_length=50)),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('receive_name', models.CharField(max_length=40)),
                ('receive_phone', models.IntegerField()),
                ('receive_address', models.CharField(max_length=100)),
                ('express_station', models.CharField(max_length=50)),
                ('express_code', models.CharField(max_length=20)),
                ('express_fee', models.FloatField()),
                ('express_size', models.CharField(max_length=40)),
                ('end_time', models.DateTimeField()),
                ('remark', models.CharField(max_length=200, null=True)),
                ('order_status', models.IntegerField(default=0)),
                ('taker_openid', models.CharField(max_length=50, null=True, unique=True)),
                ('taker_wechat', models.CharField(max_length=50, null=True)),
                ('taker_time', models.DateTimeField(null=True)),
                ('finish_time', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'tb_order',
            },
        ),
    ]
