__author__ = 'Paul'
from .models import *
from .power_ups import *


def ResetAll():
    all_groups = Group.objects.all()
    for group in all_groups:
        group.reset_powerups()
        group.save()

def Reset(group):
    group.reset_powerups()
    group.save()

def doAdministration(d: dict, caller: Group):
    v = d["doAdmin"]
    if v == "resetAll":
        ResetAll()
    elif v == "reset":
        try:
            group = d["group"]
            if caller.name == group:
                g = caller
            else:
                g = Group.objects.get(name=group)
            Reset(g)
        except KeyError:
            pass
    elif v == "givePO":
        try:
            group = d["group"]
            if caller.name == group:
                g = caller
            else:
                g = Group.objects.get(name=group)
            PowerUp = d["PO"]
            PO = powerup_name_to_class(PowerUp)()
            ret = PO.performUpgrade(group=g)
            if ret != "":
                g.save()
        except (KeyError, AttributeError):
            pass

