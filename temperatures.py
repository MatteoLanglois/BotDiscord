#!/usr/bin/python
import psutil
import csv
import datetime as dt
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def csvcount(filename):
    with open(filename, 'r') as f:
        i = len(f.readlines())
        f.close()
    return i


def autodelete(filename):
    # Function which delete the first line of the csv file
    with open(filename, 'r') as f:
        lines = f.readlines()
        f.close()
    with open(filename, 'w') as f:
        f.writelines(lines[1:])
        f.close()

def TempGathering(filename):
    temp = psutil.sensors_temperatures()
    core = [temp['coretemp'][I][1] for I in range(0, 6)]
    core.append(psutil.cpu_percent())
    x = dt.datetime.now().strftime('%H:%M:%S')
    core.insert(0, dt.datetime.strptime(x, '%H:%M:%S'))
    with open(filename, 'a', newline='') as Temp:
        writer = csv.writer(Temp)
        writer.writerow(core)
        Temp.close()


def Gathering(filename):
    if csvcount(filename) < 48:
        TempGathering(filename)
    elif csvcount(filename) == 48:
        autodelete(filename)
        TempGathering(filename)


Gathering("/home/matteo/Documents/Discord/BotDiscord/CPUtemp.csv")


#job_cpu = scheduler.add_job(Gathering, 'interval', minutes=1, args=('CPUtemp.csv',))

