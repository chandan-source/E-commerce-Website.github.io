# Generated by Django 3.1 on 2021-08-27 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
