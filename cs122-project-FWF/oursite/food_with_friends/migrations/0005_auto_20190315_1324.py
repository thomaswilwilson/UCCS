# Generated by Django 2.1.5 on 2019-03-15 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_with_friends', '0004_auto_20190315_1239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='id',
        ),
        migrations.AlterField(
            model_name='group',
            name='group_id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
    ]
