# Generated by Django 4.1.7 on 2023-03-13 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_alter_item_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='list',
        ),
    ]