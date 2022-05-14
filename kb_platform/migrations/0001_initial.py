# Generated by Django 3.2.12 on 2022-05-11 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('acc_num', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('acc_pwd', models.PositiveIntegerField()),
                ('acc_type', models.PositiveSmallIntegerField()),
                ('acc_name', models.CharField(max_length=20)),
                ('total', models.IntegerField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_date', models.DateField(auto_now_add=True)),
                ('trans_price', models.IntegerField()),
                ('trans_content', models.CharField(max_length=30)),
                ('trans_type', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('user_pwd', models.CharField(max_length=20)),
                ('user_name', models.CharField(max_length=10)),
                ('user_birth', models.DateField()),
            ],
        ),
    ]
