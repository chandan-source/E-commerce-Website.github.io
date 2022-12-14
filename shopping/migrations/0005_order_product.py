# Generated by Django 3.1 on 2021-09-15 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shopping', '0004_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='order_product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100, null=True)),
                ('house_no', models.CharField(max_length=100, null=True)),
                ('area_name', models.CharField(max_length=100, null=True)),
                ('city_state', models.CharField(max_length=100, null=True)),
                ('landmark', models.CharField(blank=True, max_length=100, null=True)),
                ('pincode', models.CharField(max_length=100, null=True)),
                ('mobile1', models.IntegerField(null=True)),
                ('mobile2', models.IntegerField(null=True)),
                ('status', models.CharField(choices=[['order_confirmed', 'order_confirmed'], ['shipped', 'shipped'], ['out_for_delivery', 'out_for_delivery'], ['delivered', 'delivered']], max_length=100, null=True)),
                ('payment_status', models.CharField(default='not done', max_length=100, null=True)),
                ('payment_id', models.CharField(max_length=100, null=True)),
                ('amount', models.IntegerField(null=True)),
                ('pro', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopping.product')),
                ('usr', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
