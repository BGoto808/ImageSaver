from http.client import HTTPException
import discord
from discord.ext import commands
import json
import uuid
from datetime import datetime
import re
import os
#from keep_alive import keep_alive

bot = commands.Bot(command_prefix=".")

# Obtain token and ID info from config.json
with open('config.json') as f:
    data = json.load(f)
    token = data["TOKEN"]
    id = data["ID"]

# Initialize bot
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Downloading :)'))
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
    
    command = ""                # User's command line input
    msg_count = 0               # Amount of messages to look through
    today = datetime.utcnow()   # Current time in UTC

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

        # Adjust current time to user specified one
        try:
            today = await adjust_time(ctx, number, unit)
        except:
            await ctx.channel.send("Parameter not accepted")

        # Try to retrieve messages, will send success or failure message
        await retrieve_messages(ctx, int(msg_count), today, True)

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

    image_count = 0          # How many images were detected in chat
    test = datetime.utcnow()

    # If timestamp is selected, retrieves after specified timestamp
    if (time_flag):
        async for message in ctx.channel.history(limit = 1000,
                                                 before = test, 
                                                 after = timestamp):
            image_count += await obtain_image(message)

    # If message count (or default) selected, retrieves by number of messages
    else:
        # Iterates through messages in text channel up until limit is hit
        # +2 to account for user command and bot output
        async for message in ctx.channel.history(limit = amount + 2):
            image_count += await obtain_image(message)

    await ctx.channel.send("Found " + str(image_count) + " images within given range\n"
                           "Image(s) saved in Downloads folder")

# Obtain image from message
async def obtain_image(message):

    # Count how many images in a Discord message attachment
    counter = 0

    # If there is an image attached to a message
    if (len(message.attachments) > 0):

        # Iterate through every image in attachment
        for images in message.attachments:

            # User directory path, saves images in Downloads folder
            parent_directory = os.path.expanduser('~/Downloads/')
            imageName = parent_directory + str(uuid.uuid4()) + '.png'
            await message.attachments[counter].save(imageName)

            counter += 1

    return counter

# Replace current datetime with adjusted one
async def adjust_time(ctx, number, unit):

    temp_time = datetime.utcnow()           # Modified datetime

    # Year
    if (unit == "y"):
        await ctx.channel.send("Finding images within last " + number + " year(s)")
        temp_time = temp_time.replace(year = temp_time.year - int(number))

    # Month
    elif (unit == "m"):
        await ctx.channel.send("Finding images within last " + number + " month(s)")

        if (temp_time.month >= int(number)):
            temp_time = temp_time.replace(month = temp_time.month - int(number))
        else:
            temp_time = temp_time.replace(year  = temp_time.year  - 1,
                                          month = temp_time.month - int(number) + 12)

    # Day
    elif (unit == "d"):
        await ctx.channel.send("Finding images within last " + number + " day(s)")
        
        if (temp_time.day >= int(number)):
            temp_time = temp_time.replace(day = temp_time.day - int(number))
        else:
            temp_time = temp_time.replace(month = temp_time.month - 1,
                                          day = temp_time.day - int(number) + 28)

    # Hour
    elif (unit == "h"):
        await ctx.channel.send("Finding images within last " + number + " hour(s)")

        if (temp_time.hour >= int(number)):
            temp_time = temp_time.replace(hour = temp_time.hour - int(number))
        else:
            temp_time = temp_time.replace(day  = temp_time.day  - 1,
                                          hour = temp_time.hour - int(number) + 24)

    # Minute
    elif (unit == "i"):
        await ctx.channel.send("Finding images within last " + number + " minute(s)")

        if (temp_time.minute >= int(number)):
            temp_time = temp_time.replace(minute = temp_time.minute - int(number))
        else:
            temp_time = temp_time.replace(hour   = temp_time.hour   - 1,
                                          minute = temp_time.minute - int(number) + 60)

    # Second
    elif (unit == "s"):
        await ctx.channel.send("Finding images within last " + number + " second(s)")

        if (temp_time.second >= int(number)):
            temp_time = temp_time.replace(second = temp_time.second - int(number))
        else:
            temp_time = temp_time.replace(minute = temp_time.minute - 1,
                                          second = temp_time.second - int(number) + 60)

    else:
        await ctx.channel.send("Error: Unit not found")

    return temp_time 

#keep_alive()
bot.run(token)