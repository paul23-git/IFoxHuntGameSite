from django.shortcuts import render
from django.http import HttpResponse
#import logging
# Create your views here.

from .models import *
from .game_funcs import *

from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt


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
        r = HttpResponse("E:Incorrect Pass-Name combination")
        r.status_code = 403;
        return r;
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
    all_others = Group.objects.exclude(hunter=mygroup.hunter)

    try:
        target = min((haversine(mygroup.longitude,mygroup.latitude, o.longitude, o.latitude),o)
                     for o in all_others)
        others_str = target[1].send_data()
    except ValueError:
        others_str = "";
    #powerups_str = "";
    if mygroup.hunter:
        exclude = 2
    else:
        exclude = 1
    all_powerups = PowerUp.objects.exclude(who=exclude, taken=True)
    powerups_str = ';'.join([repr(p) for p in all_powerups])
    all_picked_powerups = [p for p in all_powerups if haversine(mygroup.longitude, mygroup.latitude, p.longitude, p.latitude) < 10]
    if len(all_picked_powerups) > 0:
        found_powerup = all_picked_powerups[0]
        found_powerup.taken = True;
        found_powerup.save()
    return HttpResponse(others_str + '\n' + found_powerup + '\n' + powerups_str + '\n' + '\0')
