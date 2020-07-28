from django.db import models


class Group(models.Model):
    group_id = models.AutoField(primary_key = True)
    address = models.CharField(max_length=200)
    delivery_time_max = models.PositiveIntegerField()
    num_people = models.PositiveSmallIntegerField('size of group')
    p_tables = models.PositiveSmallIntegerField()
    name_count = models.PositiveSmallIntegerField()
    conversion = models.CharField(max_length = 10000, default=None)

    
class Preferences(models.Model):
    group = models.PositiveIntegerField()
    individual = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=100)
    strength_of_pref = models.FloatField(max_length=10)
    food_preference = models.CharField(max_length=100)
    budget = models.PositiveIntegerField(default=None)
