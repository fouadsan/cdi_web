# Generated by Django 3.1.6 on 2021-07-10 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20210710_1359'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartorder',
            options={'verbose_name_plural': '8. Orders'},
        ),
        migrations.AlterModelOptions(
            name='cartorderitems',
            options={'verbose_name_plural': '9. Order Items'},
        ),
    ]