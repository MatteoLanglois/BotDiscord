import psutil
import csv
import datetime

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

def TempGathering():
    temp = psutil.sensors_temperatures()
    core = [temp['coretemp'][I][1] for I in range(0, 6)]
    core.append(psutil.cpu_percent() * 10)
    core.insert(0, datetime.datetime.now())
    with open('CPUtemp.csv', 'a', newline='') as Temp:
        writer = csv.writer(Temp)
        writer.writerow(core)
        print(core)
        Temp.close()


if csvcount("CPUtemp.csv") < 48:
    TempGathering()
elif csvcount("CPUtemp.csv") == 48:
    autodelete("CPUtemp.csv")
    TempGathering()