# Generated by Django 2.2.9 on 2020-10-30 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_type', models.CharField(choices=[('sync', 'sync'), ('async', 'async')], max_length=10)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('notify_payment_system_done_time', models.DateTimeField(null=True)),
                ('notify_logistics_system_done_time', models.DateTimeField(null=True)),
                ('send_email_done_time', models.DateTimeField(null=True)),
            ],
        ),
    ]
