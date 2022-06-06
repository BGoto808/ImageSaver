import discord
import json
import uuid

client = discord.Client()

with open('config.json') as f:
    data = json.load(f)
    token = data["TOKEN"]
    id = data["ID"]

@client.event
async def on_ready():
    print("Bot is ready")

@client.event 
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith(".save"):
        # Name image a random string of characters
        imageName = str(uuid.uuid4()) + '.jpg'

        try:
            await message.attachments[0].save(imageName)
        except IndexError:
            await message.channel.send("Error: No attachments!")
        else:
            await message.channel.send("Saved " + imageName)


client.run(token)