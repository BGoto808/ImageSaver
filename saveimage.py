import discord
from discord.ext import commands
import json
import uuid
from datetime import datetime

bot = commands.Bot(command_prefix=".")

with open('config.json') as f:
    data = json.load(f)
    token = data["TOKEN"]
    id = data["ID"]

@bot.event
async def on_ready():
    print("Bot is ready")

# Test command
@bot.command(
    help = "Testing ping-pong command",
    brief = "Prints pong to the channel"
)
async def ping(ctx):
    await ctx.channel.send("pong")

@bot.command(
    help = "Saves image(s) in text channel. Arguments: \n"
            "-t: Saves images based on time (e.g. '-t 5d' saves images in last 5 days) \n"
            "-m: Saves images based on number of messages (e.g. '-m 5' saves images within last 5 messages)", 
    brief = "Saves image(s) in text channel"
)
async def save(ctx, *args):
    
    command = ""

    for arg in args:
        command = command + " " + arg

    # Removing space at beginning of command line argument
    command = command[1:]

    if (command[0:2] == "-t"):
        ## Save image based on time
        await ctx.channel.send("Saving images in the last ")
        today = datetime.now()

    elif (command[0:2] == "-m"):
        ## Save images based on amount of messages
        msg_count = command[3:]
        await ctx.channel.send("Saving images within the last " + msg_count + " messages")
        await retrieve_messages(ctx, int(msg_count))

    elif (command[0:2] == ""):
        ## Save last image
        await ctx.channel.send("Saving last image")
        await retrieve_messages(ctx, 1)

    else:
        await ctx.channel.send("Error: Invalid argument!")

# Retrieve messages in text-channel
async def retrieve_messages(ctx, amount):

    # Iterates through messages in text channel up until limit is hit
    # +2 to account for user command and bot output
    async for message in ctx.channel.history(limit=amount+2):

        # If there is an image attached to a message
        if (len(message.attachments) > 0):
            counter = 0

            # Iterate through every image in attachment
            for images in message.attachments:
                imageName = str(uuid.uuid4()) + '.png'
                await message.attachments[counter].save(imageName)
                counter += 1

bot.run(token)