# Generated by Django 3.0.6 on 2020-06-02 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='order_id',
            field=models.CharField(max_length=18, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='publish_time',
            field=models.DateTimeField(),
        ),
    ]