# Generated by Django 2.2.1 on 2019-05-30 10:14

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now_add=True)),
                ('pub_id', core.models.AutoPubIDField(blank=True, editable=False, max_length=20, unique=True, verbose_name='public id')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='email address')),
                ('phone', models.CharField(max_length=64, verbose_name='phone')),
                ('name', models.CharField(max_length=128, verbose_name='name of user')),
                ('sign_pub_key', models.CharField(max_length=255, unique=True, verbose_name='verify key')),
                ('api_token', models.CharField(max_length=255, null=True, unique=True, verbose_name='api token')),
            ],
            options={
                'verbose_name': 'my_user',
            },
        ),
    ]
