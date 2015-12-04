from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from .models import *
from .game_funcs import *

from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt


@csrf_exempt
def index(request):
    print(" -----------------------  ")
    if request.method=="GET":
        d = request.GET
    else:
        d = request.POST
    print("input: ", d)
    try:
        inName = d["name"]
        inPass = d["pass"]
    except KeyError as e:
        return HttpResponse("")
    print(inName, inPass)
    try:
        mygroup = Group.objects.get(name=inName,password=inPass)
    except:
        return HttpResponse("")
    if request.method == "GET":
        all_others = Group.objects.exclude(hunter=mygroup.hunter)
        #others_str = ';'.join([p.send_data() for p in all_others])
        target = min((haversine(mygroup.longitude,mygroup.latitude, o.longitude, o.latitude),o)
                     for o in all_others)
        print(target)
        others_str = target[1].send_data()
        if mygroup.hunter:
            exclude = 2
        else:
            exclude = 1
        all_powerups = PowerUp.objects.exclude(who=exclude)
        powerups_str = ';'.join([repr(p) for p in all_powerups])
        return HttpResponse(others_str + '\n' + powerups_str)
    else:
        position = d["pos"]
        l = position.split(",")
        mygroup.longitude = float(l[0])
        mygroup.latitude = float(l[1])
        mygroup.altitude = float(l[2])
        mygroup.save()
        if mygroup.hunter:
            exclude = 2
        else:
            exclude = 1
        all_powerups = PowerUp.objects.exclude(who=exclude)
        try:
            d = [p for p in all_powerups if haversine(mygroup.longitude, mygroup.latitude, p.longitude, p.latitude) < 10][0]
            d.delete()
            return HttpResponse(repr(d))
        except:
            return HttpResponse("")