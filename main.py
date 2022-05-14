import discord
import wmi


class Managing(discord.Client):
    async def on_ready(self):
        print(f"Logged in as\n {self.user.name}\n {self.user.id}")
        await client.get_channel(450700356385636353).send("Bot is ready")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content == "Ping":
            await message.channel.send("Pong")

        if message.content.startswith("!hello"):
            await message.channel.send("Hello! {0.author.mention}".format(message))


client = Managing()
client.run("OTc0OTQ3Nzc0Nzg3MzY3MDEz.GJQ8hB.kZ4xt9ky5oTcEIXBfze4aAiv2EsDe8ubi6rKvQ")
