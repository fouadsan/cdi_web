# Generated by Django 3.2 on 2021-04-26 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('content', models.TextField()),
                ('image', models.ImageField(upload_to='images')),
                ('since', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=150, unique=True)),
                ('description', models.TextField()),
                ('image_one', models.ImageField(upload_to='images')),
                ('image_two', models.ImageField(upload_to='images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'section',
                'verbose_name_plural': 'sections',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('occupation', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='images')),
            ],
        ),
    ]