# Generated by Django 3.2.23 on 2023-12-24 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_remove_trade_user_custom_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='row_number',
            field=models.IntegerField(editable=False),
        ),
    ]