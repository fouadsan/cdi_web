# Generated by Django 3.2 on 2021-05-05 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogmodel',
            options={'ordering': ('-timestamp',), 'verbose_name_plural': '1. BlogModels'},
        ),
        migrations.AlterModelOptions(
            name='commentmodel',
            options={'ordering': ('-timestamp',), 'verbose_name_plural': '2. CommentModels'},
        ),
    ]
