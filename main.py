import discord
from discord.ext import commands
import psutil
import matplotlib.pyplot as plt
import csv
import datetime as datetime
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Thread

bot = commands.Bot(command_prefix='$')

scheduler = BackgroundScheduler()

def TempGathering():
    print("a")
    temp = psutil.sensors_temperatures()
    core = [temp['coretemp'][I][1] for I in range(0, 6)]
    core.append(psutil.cpu_percent() * 10)
    core.insert(0, datetime.datetime.now())
    with open('CPUtemp.csv', 'a', newline='') as Temp:
        writer = csv.writer(Temp)
        writer.writerow(core)
        print(core)
        Temp.close()

def SchCPU():
    scheduler.add_job(TempGathering, 'interval', minutes=0.1, replace_existing=True, max_instances=20)

@bot.event
async def on_ready():
    print("Logged on as", bot.user)


async def on_message(message):
    if message.author.id == bot.user.id:
        return
    elif "di" in message.content.lower():
        li = message.content.split(" ")
        for word in li:
            if "di" in word.lower():
                await message.channel.send(word[2:])
    elif "quoi" in message.content.lower():
        li = message.content.split(" ")
        li = [I.lower() for I in li]
        pos = li.index("quoi")
        for I in range(pos, len(li)):
            if I in ["?", ":", "!", "."]:
                await message.channel.send("feur")


@bot.command(help='Responds pong to ping')
async def ping(ctx):
    await ctx.channel.send("pong")

@bot.command(name="say", help='Responds with the args and delete the command')
async def text(ctx, arg):
    await ctx.send(arg)
    await ctx.message.delete()

@bot.command(help='Responds with the temp of the CPU of your computer who host the bot')
async def cpu(ctx):
    embedvar = discord.Embed(
        title = "CPU stats", color=0xff4030
    )
    temp = psutil.sensors_temperatures()
    embedvar.add_field(name="Température du package processeur :",
                       value=f"Package : {temp['coretemp'][0][1]}°")
    embedvar.add_field(name="Température de chaque coeur :",
                       value=f"\n - Core n°0 : {temp['coretemp'][1][1]}°" \
                             f"\n - Core n°1 : {temp['coretemp'][2][1]}°" \
                             f"\n - Core n°2 : {temp['coretemp'][3][1]}°" \
                             f"\n - Core n°3 : {temp['coretemp'][4][1]}°" \
                             f"\n - Core n°4 : {temp['coretemp'][5][1]}°" \
                             f"\n - Core n°5 : {temp['coretemp'][5][1]}°")
    embedvar.add_field(name="Utilsation du processeur :",
                       value=f"{psutil.cpu_percent() * 10}%",
                       inline=False)
    await ctx.send(embed=embedvar)

@bot.command(help='Responds with the usage of RAM')
async def ram(ctx):
    embedvar = discord.Embed(
        title="RAM Stats", color=0x478030
    )
    embedvar.add_field(name="RAM Totale :",
                       value=f"{round(psutil.virtual_memory().total / 10**9, 1)}Go",
                       inline=False)
    embedvar.add_field(name="RAM Disponible :",
                       value=f"{round(psutil.virtual_memory().available / 10**9, 1)}Go",
                       inline=False)
    embedvar.add_field(name="RAM Utilisée :",
                       value=f"{round((psutil.virtual_memory().total - psutil.virtual_memory().available) / 10**9, 1)}Go"
                             f"/{psutil.virtual_memory().percent}%",
                       inline=False)
    plt.pie([psutil.virtual_memory().available, psutil.virtual_memory().total - psutil.virtual_memory().available],
            labels=["RAM Disponible", "RAM Utilisée"])
    plt.savefig("/var/www/html/temp/temp.png",  bbox_inches='tight')

    embedvar.set_image(url="https://les-roseaux.dev/temp/temp.png")
    await ctx.send(embed=embedvar)

@bot.command(help='Responds with graph of CPU Stats')
async def CPU_usage(ctx):
    embedvar = discord.Embed(
        title="CPU stats", color=0xff4030
    )
    stats = [[], [], [], [], [], [], [], []]
    with open('CPUtemp.csv', 'r', newline='') as Temp:
        file_reader = csv.reader(Temp)
        for line in file_reader:
            for I in range(len(line)):
                stats[I].append(float(line[I]))
    for stat in stats[1:6]:
        print(len(stat), len(stats[0]))
        plt.plot(stat, stats[0])
    plt.savefig("/var/www/html/temp/temp2.png", bbox_inches='tight')
    embedvar.set_image(url="https://les-roseaux.dev/temp/temp2.png")
    await ctx.send(embed=embedvar)

CPU_temp = Thread(target=SchCPU)
CPU_temp.start()

bot.run("OTc0OTQ3Nzc0Nzg3MzY3MDEz.GJQ8hB.kZ4xt9ky5oTcEIXBfze4aAiv2EsDe8ubi6rKvQ")
