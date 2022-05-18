import discord
from discord.ext import commands
import psutil
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
import dateutil

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print("Logged on as", bot.user)

@bot.event
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
        cond = True
        for I in li[li.index("quoi") + 1:]:
            if I.isalpha():
                cond = False
        if cond:
            await message.channel.send("feur")


@bot.command(help='Responds pong to ping')
async def ping(ctx):
    await ctx.channel.send("pong")

@bot.command(name="say", help='Responds with the args and delete the command')
async def text(ctx, arg):
    await ctx.message.delete()
    await ctx.send(arg)

@bot.command(help='Clear the precedent message')
async def clear(ctx, amount: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)

@bot.command(help='Change the activity of the bot')
async def activity(ctx, game):
    print("activity changed")
    await ctx.message.delete()
    await bot.change_presence(activity=discord.Game(game))

@bot.command(help='Responds with the temp of the CPU of your computer who host the bot')
async def cpu(ctx):
    await ctx.message.delete()
    fig_cpu = plt.figure()
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
                       value=f"{psutil.cpu_percent()}%",
                       inline=False)
    stats = [[], [], [], [], [], [], []]
    tempDates = []
    with open('CPUtemp.csv', 'r', newline='') as Temp:
        file_reader = csv.reader(Temp)
        for line in file_reader:
            for I in range(1, len(line)):
                stats[I - 1].append(float(line[I]))
            tempDates.append(dateutil.parser.parse(line[0]))
        Temp.close()
    plt.gca().xaxis.set_major_formatter()
    for I in range(1, len(stats)):
        plt.plot(tempDates, stats[I], label=f"Core {I}")
        plt.legend(["Core n°" + str(I)])
    plt.plot(tempDates, stats[0], label="Package")
    plt.legend("Package")
    plt.plot(tempDates, stats[-1], label="Use")
    plt.legend("Use")
    plt.gcf().autofmt_xdate()
    plt.legend(loc='center left')
    plt.savefig("/var/www/html/temp/temp2.png")
    file = discord.File("/var/www/html/temp/temp2.png", filename="temp2.png")
    embedvar.set_image(url="attachment://temp2.png")
    await ctx.send(file=file, embed=embedvar)
    fig_cpu.clear()

@bot.command(help='Responds with the usage of RAM')
async def ram(ctx):
    await ctx.message.delete()
    fig_ram = plt.figure()
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
    tempDates, stat = [], []
    with open('RAMtemp.csv', 'r', newline='') as Temp:
        file_reader = csv.reader(Temp)
        for line in file_reader:
            stat.append(float(line[1]))
            tempDates.append(dateutil.parser.parse(line[0]))
        Temp.close()
    plt.gca().xaxis.set_major_formatter()
    plt.plot(tempDates, stat, label=f"RAM utilisée")
    plt.legend("Ram utilisée")
    plt.gcf().autofmt_xdate()
    plt.legend(loc='center left')
    plt.savefig("/var/www/html/temp/temp.png")
    file = discord.File("/var/www/html/temp/temp.png", filename="temp.png")
    embedvar.set_image(url="attachment://temp.png")
    await ctx.send(file=file, embed=embedvar)
    fig_ram.clear()


bot.run("OTc0OTQ3Nzc0Nzg3MzY3MDEz.G55BO3.Wj0NRUMt9Bm15ek7txFAi-DDa_JnZRvWUVBOnY")