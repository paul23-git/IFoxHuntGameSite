from django.db import models
from datetime import time
from datetime import datetime
import random
import IFoxHuntGame.game_funcs as game_funcs
import math

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Group(models.Model):
    name = models.CharField("name",max_length=200)
    password = models.CharField("password",max_length=200)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    altitude = models.FloatField(default=0)
    hunter = models.BooleanField(default=True)
    accuracy_mod = models.FloatField(default=1)
    conceal_mod = models.FloatField(default=1)
    visibility = models.DateTimeField(default=datetime(2015,12,11))
    distance_show = models.DateTimeField(default=datetime(2015,12,11))
    is_active = models.BooleanField(default = True )
    has_targetting = models.BooleanField(default = False)
    def reset_powerups(self):
        self.accuracy_mod = 1;
        self.conceal_mod = 1;
        self.distance_show=datetime(2015,12,11);
        self.visibility=datetime(2015,12,11);
        self.has_targetting = False;

    def __repr__(self):
        return str(self.name)+ ","\
               + str(self.password) + "," \
               + str(self.longitude) + "," \
               + str(self.latitude) + "," \
               + str(self.altitude) + "," \
               + str(self.hunter)
    def send_data(self, group_accuracy):
        dis = game_funcs.BASE_INACCURACY / group_accuracy * self.conceal_mod
        longitude, latitude = game_funcs.offsetCoordinates(self.longitude, self.latitude, random.random() * dis, 2 *math.pi* random.random())
        return str(self.name)+ ","\
               + str(longitude) + "," \
               + str(latitude) + "," \
               + str(self.altitude) + "," \
               + str(self.hunter)

class PowerUp(models.Model):
    PU_id = models.PositiveIntegerField(default=0)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    altitude = models.FloatField(default=0)
    who = models.IntegerField(default=0)
    taken = models.IntegerField(default=0)
    message = models.TextField(default="Congrats you got a powerup!")
    database_string = models.TextField(default="", blank=True)
    specific_group = models.TextField(default="", blank=True)
    def __repr__(self):
        return str(self.id) + "," \
               + str(self.longitude) + "," \
               + str(self.latitude) + "," \
               + str(self.altitude) + "," \
               + str(self.PU_id)+ ","\
               + str(self.who)+"," \
               + str(self.message)