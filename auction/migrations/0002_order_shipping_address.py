# Generated by Django 3.0.5 on 2020-04-15 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
