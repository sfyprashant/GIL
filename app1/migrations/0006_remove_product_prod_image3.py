# Generated by Django 4.2.9 on 2024-03-07 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_cancellation_comment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='prod_image3',
        ),
    ]
