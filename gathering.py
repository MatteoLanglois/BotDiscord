import psutil
import csv
import datetime as dt


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
    x = dt.datetime.now()
    core.insert(0, x)
    with open(filename, 'a', newline='') as Temp:
        writer = csv.writer(Temp)
        writer.writerow(core)
        Temp.close()

def RAMGathering(filename):
    core = [(psutil.virtual_memory().total - psutil.virtual_memory().available) / 10**9]
    x = dt.datetime.now()
    core.insert(0, x)
    with open(filename, 'a', newline='') as Temp:
        writer = csv.writer(Temp)
        writer.writerow(core)
        Temp.close()

def Gathering(filename, file2):
    if csvcount(filename) < 48:
        TempGathering(filename)
    elif csvcount(filename) == 48:
        autodelete(filename)
        TempGathering(filename)
    if csvcount(file2) < 48:
        RAMGathering(file2)
    elif csvcount(file2) == 48:
        autodelete(file2)
        RAMGathering(file2)

Gathering("/home/matteo/Documents/Discord/BotDiscord/CPUtemp.csv",
          "/home/matteo/Documents/Discord/BotDiscord/RAMtemp.csv")

