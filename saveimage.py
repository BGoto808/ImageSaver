from http.client import HTTPException
import discord
from discord.ext import commands
import json
import uuid
from datetime import datetime
import re

bot = commands.Bot(command_prefix=".")

# Obtain token and ID info from config.json
with open('config.json') as f:
    data = json.load(f)
    token = data["TOKEN"]
    id = data["ID"]

# Initialize bot
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

# Save image function
@bot.command(
    help = "Saves image(s) in text channel. Arguments: \n"
            "-t: Saves images based on time (e.g. '-t 5d' saves images in last 5 days) \n"
            "    {YEAR = y, MONTH = m, DAY = d, HOUR = h, MINUTE = i, SECOND = s}\n"
            "-m: Saves images based on number of messages (e.g. '-m 5' saves images within last 5 messages)\n",
    brief = "Saves image(s) in text channel"
)
async def save(ctx, *args):
    
    # Reset values
    command = ""
    msg_count = 0
    today = datetime.utcnow()

    # Record entire command
    for arg in args:
        command = command + " " + arg

    # Removing space at beginning of command line argument
    command = command[1:]

    # Check command line arguments for parameters
    # -t: Save image based on time
    if (command[0:2] == "-t"):
        # Get number and unit from command line argument
        number = command[3:-1]
        unit = command[-1]

        today = await adjust_time(ctx, number, unit)

        # Try to retrieve messages, will send success or failure message
        try: 
            await ctx.channel.send("Finding images after " + str(today))
            await retrieve_messages(ctx, int(msg_count), today, True)
        except IndexError:
            await ctx.channel.send("No image found")

    # -m: Save images based on amount of messages
    elif (command[0:2] == "-m"):
        msg_count = command[3:]
        await ctx.channel.send("Saving images within the last " + msg_count + " messages")
        await retrieve_messages(ctx, int(msg_count), today, False)

    # Default: Save last image
    elif (command[0:2] == ""):
        await ctx.channel.send("Saving last image")
        await retrieve_messages(ctx, 1, today, False)

    else:
        await ctx.channel.send("Error: Invalid argument!")

# Retrieve messages in text-channel
async def retrieve_messages(ctx, amount, timestamp, time_flag):

    # If timestamp is selected, retrieves after specified timestamp
    if (time_flag):
        async for message in ctx.channel.history(after = timestamp):
            await obtain_image(message)

    # If message count (or default) selected, retrieves by number of messages
    else:
        # Iterates through messages in text channel up until limit is hit
        # +2 to account for user command and bot output
        async for message in ctx.channel.history(limit = amount + 2):
            await obtain_image(message)

# Obtain image from message
async def obtain_image(message):

    # Count how many images in a Discord message attachment
    counter = 0

    # If there is an image attached to a message
    if (len(message.attachments) > 0):

        # Iterate through every image in attachment
        for images in message.attachments:
            imageName = str(uuid.uuid4()) + '.png'
            await message.attachments[counter].save(imageName)
            counter += 1

# Replace current datetime with user adjusted one
async def adjust_time(ctx, number, unit):

    today = datetime.utcnow()

    if (unit == "y"):
        today = today.replace(year = today.year - int(number))
    elif (unit == "m"):

        if (today.month >= int(number)):
            today = today.replace(month = today.month - int(number))
        else:
            today = today.replace(year  = today.year  - 1)
            today = today.replace(month = today.month - int(number) + 12)

    elif (unit == "d"):
        today = today.replace(day = today.day - int(number))
    elif (unit == "h"):

        if (today.hour >= int(number)):
            today = today.replace(hour = today.hour - int(number))
        else:
            today = today.replace(day  = today.day  - 1)
            today = today.replace(hour = today.hour - int(number) + 24)

    elif (unit == "i"):

        if (today.minute >= int(number)):
            today = today.replace(minute = today.minute - int(number))
        else:
            today = today.replace(hour   = today.hour   - 1)
            today = today.replace(minute = today.minute - int(number) + 60)

    elif (unit == "s"):

        if (today.second >= int(number)):
            today = today.replace(second = today.second - int(number))
        else:
            today = today.replace(minute = today.minute - 1)
            today = today.replace(second = today.second - int(number) + 60)

    else:
        await ctx.channel.send("Error: Unit not found")

    return today

bot.run(token)