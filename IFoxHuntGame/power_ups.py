import sys
from typing import Tuple
import datetime
from django.db import models

#from .models import *



class PowerUps:
    @classmethod
    def get_id(cls):
        powerup_get_id(cls.__name__)
    @classmethod
    def get_name(cls):
        return cls.__name__
    def performUpgrade(self, group, *args, **kwargs) -> Tuple[bool,str]:
        return (False,"")

class AccuracyPowerUp(PowerUps):
    def performUpgrade(self, group, *args, **kwargs) -> Tuple[bool,str]:
        if group.hunter:
            group.accuracy_mod /= 1.5
            return (True,"Your GPS is now twice as good")
        else:
            group.conceal_mod *= 1.5
            return (True,"You scramble the hunter's gps")
        return (False,"");
class VisibilityPowerUp(PowerUps):
    def performUpgrade(self, group, *args, **kwargs) -> Tuple[bool,str]:
        group.visibility = datetime.now() + datetime.timedelta(minutes=5)
        return (True, "You hide your movement for 5 minutes")





def powerup_get_name( id) -> str:
    return names[id]
def powerup_get_id(name):
    return id_to_name_map(name)
def powerup_name_to_class(str) -> PowerUps:
    return getattr(sys.modules[__name__], str)



names = [PowerUps.get_name(), AccuracyPowerUp.get_name(), VisibilityPowerUp.get_name()]
id_to_name_map =dict(p for p in enumerate(names))