from django.shortcuts import render
from django.http import HttpResponse
import datetime
#import logging
# Create your views here.

from .models import *
from .game_funcs import *
from .admin_funcs import *
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q


@csrf_exempt
def index(request):
    if request.method=="GET":
        d = request.GET
    else:
        d = request.POST
    try:
        inName = d["name"]
        inPass = d["pass"]
    except KeyError as e:
        r = HttpResponse("Invalid config")
        r.status_code = 403;
        return  r;


    try:
        mygroup = Group.objects.get(name=inName,password=inPass)
    except:
        r = HttpResponse("Incorrect Pass-Name combination")
        r.status_code = 403;
        return r;

    if inName == ADMIN_GROUP and "doAdmin" in d:
        r = HttpResponse(doAdministration(d,mygroup))
        r.status_code = 200;
        return r




    found_powerup = "";
    if request.method == "POST":
        try:
            position = d["pos"]
            l = position.split(",")
            mygroup.longitude = float(l[0])
            mygroup.latitude = float(l[1])
            mygroup.altitude = float(l[2])
            mygroup.save()
        except (KeyError, IndexError):
            pass

    if mygroup.hunter:
        exclude = 2
    else:
        exclude = 1

    all_powerups = PowerUp.objects.exclude(who=exclude).exclude(taken=True).filter(Q(specific_group="") | Q(specific_group=mygroup.name))
    powerups_str = ';'.join([repr(p) for p in all_powerups])

    all_picked_powerups = [p for p in all_powerups if haversine(mygroup.longitude, mygroup.latitude, p.longitude, p.latitude) < 20]
    found_powerup_msg = ""
    if len(all_picked_powerups) > 0:
        found_powerup = all_picked_powerups[0]
        dodelete = True;
        found_powerup_msg = found_powerup.message
        try:
            PO_name = powerup_get_name(int(found_powerup.PU_id))
            PO = powerup_name_to_class(PO_name)()
            ret = PO.performUpgrade(mygroup)
            if ret[0]:
                found_powerup_msg += " " + ret[1]
                mygroup.save();
            else:
                dodelete = False
        except (ValueError, TypeError, IndexError):
            pass
        finally:
            if dodelete:
                found_powerup.taken = True;
                found_powerup.save()
    others_str = ""
    if mygroup.has_targetting:
        all_others = Group.objects.exclude(hunter=mygroup.hunter).filter(visibility__lt=datetime.datetime.now()).filter(is_active=True)
        try:
            target = min((haversine(mygroup.longitude,mygroup.latitude, o.longitude, o.latitude),o)
                         for o in all_others)
            others_str = target[1].send_data(mygroup.accuracy_mod)
        except ValueError:
            pass
    return HttpResponse(others_str + '\r\n' + found_powerup_msg  + '\r\n' + powerups_str + '\r\n' + '\0')
