# Generated by Django 3.1 on 2021-09-29 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0005_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_detail',
            name='mobile',
            field=models.IntegerField(null=True),
        ),
    ]