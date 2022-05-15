import discord
from discord.ext import commands
import psutil
import matplotlib.pyplot as plt
from PIL import Image

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print("Logged on as", bot.user)

async def on_message(message):
    if message.author.id == bot.user.id:
        return
    if "di" in message.content.lower():
        li = message.content.split(" ")
        for word in li:
            if "di" in word.lower():
                await message.channel.send(word[2:])
    if "quoi" in message.content.lower():
        li = message.content.split(" ")
        li = [I.lower for I in li]
        pos = li.index("quoi")
        for I in range(pos, len(li)):
            if I in ["?", ":", "!", "."]:
                await message.channel.send("feur")


@bot.command(help='Responds pong to ping')
async def ping(ctx):
    await ctx.channel.send("pong")

@bot.command(name="say", help='Responds with the args')
async def text(ctx, arg):
    await ctx.send(arg)

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

bot.run("OTc0OTQ3Nzc0Nzg3MzY3MDEz.GJQ8hB.kZ4xt9ky5oTcEIXBfze4aAiv2EsDe8ubi6rKvQ")
