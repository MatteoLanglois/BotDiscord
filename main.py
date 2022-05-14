import discord
import psutil

class Managing(discord.Client):
    async def on_ready(self):
        print(f"Logged in")
        await client.get_channel(450700356385636353).send("Bot is ready")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content == "Ping":
            await message.channel.send("Pong")

        if message.content.startswith("!temp"):
            temp = psutil.sensors_temperatures()
            if "full" in message.content:
                txt = f"Temperature du processeur :\n Package : {temp['coretemp'][0][1]}°"\
                          f"\n - Core n°0 : {temp['coretemp'][1][1]}°"\
                          f"\n - Core n°1 : {temp['coretemp'][2][1]}°"\
                          f"\n - Core n°2 : {temp['coretemp'][3][1]}°"\
                          f"\n - Core n°3 : {temp['coretemp'][4][1]}°"\
                          f"\n - Core n°4 : {temp['coretemp'][5][1]}°"\
                          f"\n - Core n°5 : {temp['coretemp'][5][1]}°"
            else:
                txt = f"Temperature du processeur : {temp['coretemp'][0][1]}°"
            await message.channel.send(txt)

        if message.content.startswith("!use"):
            await message.channel.send(f"Utilisation du processeur : {psutil.cpu_percent() * 10}%")


client = Managing()
client.run("OTc0OTQ3Nzc0Nzg3MzY3MDEz.GJQ8hB.kZ4xt9ky5oTcEIXBfze4aAiv2EsDe8ubi6rKvQ")
