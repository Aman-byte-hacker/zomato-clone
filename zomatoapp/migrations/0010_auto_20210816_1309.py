# Generated by Django 3.1.5 on 2021-08-16 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zomatoapp', '0009_userproduct_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userproduct',
            name='status',
            field=models.CharField(choices=[('order accepted', 'accepted'), ('Food is being prepared', 'preparing'), ('out for delievery', 'out for delievery'), ('Delieverd', 'done')], default='accepted', max_length=200),
        ),
    ]
