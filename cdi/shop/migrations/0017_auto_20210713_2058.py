# Generated by Django 3.1.6 on 2021-07-13 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_cartorder_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='order_status',
            field=models.CharField(choices=[('process', 'In Process'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='process', max_length=150),
        ),
    ]
