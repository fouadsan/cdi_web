# Generated by Django 3.2 on 2021-05-10 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20210507_1704'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'get_latest_by': '-created_at', 'verbose_name_plural': '3. Products'},
        ),
    ]
