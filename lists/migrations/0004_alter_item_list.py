# Generated by Django 4.1.7 on 2023-03-13 00:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_item_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='list',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='lists.list'),
        ),
    ]