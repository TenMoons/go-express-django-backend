# Generated by Django 3.0.6 on 2020-05-27 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='update_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
