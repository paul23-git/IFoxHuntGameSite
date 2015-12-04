#!/usr/bin/env python
import os
import sys
from django.core.management import execute_from_command_line

def makemigrations(name):
    n = sys.argv[0]
    execute_from_command_line([n, "makemigrations", name])

def sqlmigrate(name, num_string):
    n = sys.argv[0]
    execute_from_command_line([n, "sqlmigrate", name, num_string])
def migrate():
    n = sys.argv[0]
    execute_from_command_line([n, "migrate"])

def shell():
    n = sys.argv[0]
    execute_from_command_line([n, "shell"])
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IFoxHuntGameSite.settings")

    makemigrations("IFoxHuntGame")
    migrate()
    #shell()
    #exit()
    #print(sys.argv)
    a = sys.argv;


    execute_from_command_line(a)
