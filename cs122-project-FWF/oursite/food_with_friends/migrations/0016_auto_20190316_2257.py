# Generated by Django 2.1.7 on 2019-03-16 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_with_friends', '0015_auto_20190316_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preferences',
            name='strength_of_pref',
            field=models.FloatField(max_length=10),
        ),
    ]