from django.db import models

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
    def __repr__(self):
        return str(self.name)+ ","\
               + str(self.password) + "," \
               + str(self.longitude) + "," \
               + str(self.latitude) + "," \
               + str(self.altitude) + "," \
               + str(self.hunter)
    def send_data(self):
        return str(self.name)+ ","\
               + str(self.longitude) + "," \
               + str(self.latitude) + "," \
               + str(self.altitude) + "," \
               + str(self.hunter)

class PowerUp(models.Model):
    PU_id = models.PositiveIntegerField(default=0)
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    altitude = models.FloatField(default=0)
    who = models.IntegerField(default=0)
    taken = models.IntegerField(default=0)
    def __repr__(self):
        return str(self.PU_id)+ ","\
               + str(self.longitude) + "," \
               + str(self.latitude) + "," \
               + str(self.altitude) + "," \
               + str(self.who)