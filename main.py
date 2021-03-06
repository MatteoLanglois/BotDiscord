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
    print(f"Logged on as {bot.user} in {len(bot.guilds)} server.s!")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.id == bot.user.id:
        return
    elif "di" in message.content.lower():
        li = message.content.split(" ")
        for word in li:
            if "di" in word.lower():
                await message.channel.send(word[2:])*
    elif "quoi" in message.content.lower():
        li = message.content.split(" ")
        li = [I.lower() for I in li]
        cond = True
        for I in li[li.index("quoi") + 1:]:
            if I.isalpha():
                cond = False
        if cond:
            await message.channel.send("feur")


async def is_admin(ctx):
    admin = discord.utils.get(ctx.guild.roles, name="Admin")
    return admin in ctx.author.roles

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
@commands.check(is_admin)
async def activity(ctx, type, game):
    await ctx.message.delete()
    if type.lower() == "game":
        await bot.change_presence(activity=discord.Game(name=game))
    elif type.lower() == "listening":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=game))
    elif type.lower() == "watching":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=game))
    else:
        await ctx.send("Type not found")

@activity.error
async def activity_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing argument")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have the right to use this command")


@bot.command(help='Responds with the temp of the CPU of your computer who host the bot')
async def cpu(ctx):
    await ctx.message.delete()
    fig_cpu = plt.figure()
    embedvar = discord.Embed(
        title = "CPU stats", color=0xff4030
    )
    temp = psutil.sensors_temperatures()
    embedvar.add_field(name="Temp??rature du package processeur :",
                       value=f"Package : {temp['coretemp'][0][1]}??")
    embedvar.add_field(name="Temp??rature de chaque coeur :",
                       value=f"\n - Core n??0 : {temp['coretemp'][1][1]}??" \
                             f"\n - Core n??1 : {temp['coretemp'][2][1]}??" \
                             f"\n - Core n??2 : {temp['coretemp'][3][1]}??" \
                             f"\n - Core n??3 : {temp['coretemp'][4][1]}??" \
                             f"\n - Core n??4 : {temp['coretemp'][5][1]}??" \
                             f"\n - Core n??5 : {temp['coretemp'][5][1]}??")
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
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    for I in range(1, len(stats)):
        plt.plot(tempDates, stats[I], label=f"Core {I}")
        plt.legend(["Core n??" + str(I)])
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
    embedvar.add_field(name="RAM Utilis??e :",
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
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.plot(tempDates, stat, label=f"RAM utilis??e")
    plt.legend("Ram utilis??e")
    plt.gcf().autofmt_xdate()
    plt.legend(loc='center left')
    plt.savefig("/var/www/html/temp/temp.png")
    file = discord.File("/var/www/html/temp/temp.png", filename="temp.png")
    embedvar.set_image(url="attachment://temp.png")
    await ctx.send(file=file, embed=embedvar)
    fig_ram.clear()


bot.run("OTc0OTQ3Nzc0Nzg3MzY3MDEz.GvOvq8.YlDLZQJzK_ouSYH9tuqQaB8X5zI7aAco7GhQ94")