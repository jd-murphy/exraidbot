from __future__ import print_function
import os
import random
import requests
import asyncio
import csv
import discord
from discord.ext.commands import Bot
from discord import Game
import pytesseract    #   requires heroku buildpack!!!!!!!
from PIL import Image
import aiohttp
import json
from os import environ
from twilio.rest import Client
from discord import Status
import pyrebase_worker





TOKEN = environ['TOKEN'] 
BOT_PREFIX = ("!")

INSTINCT_EMOJI = "<:emoji_name:456205777389092895>" # <:emoji_name:456205777389092895> # instinct
MYSTIC_EMOJI = "<:emoji_name:456205778022563851>" # <:emoji_name:456205778022563851> # mystic
VALOR_EMOJI = "<:emoji_name:456205778395725834>" # <:emoji_name:456205778395725834> # valor

MYSTIC_ROLE_ID = "276922105441026048"
VALOR_ROLE_ID = "276922104169889794"
INSTINCT_ROLE_ID = "276922106107658241"

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

RAIDS = ['Empty list']
GYMS = {}
emoji = [
        ':100:',
        ':ok_hand:',
        ':sunglasses:',
        ':yum:',
        ':stuck_out_tongue_closed_eyes:',
        ':grinning:',
        ':heart_eyes:',
        ':money_mouth:',
        ':hugging:',
        ':robot:',
        ':clap:',
        ':call_me:',
        ':see_no_evil:',
        ':tada:',
        ':space_invader:',
        ':cool:',
        ':innocent:',
        ':thumbsup:',
    ]




client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')
@client.command()
async def help():
    msg = ("This bot is in testing. Look forward to some awesome Ex Raid features coming soon! " + random.choice(emoji))
    await client.say(msg)
        



@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Pokemon Go, duh"))
    print("Logged in as " + client.user.name)
   



@client.event
async def on_message(message):

    if message.attachments:
        if message.channel.id == "355402329899401217" or message.channel.id == "276921948058025984":
            print('message with attachment from:')
            print(message.author.name)
            print('in channel:')
            print(message.channel.name)
            print('message.attachments:')
            print(message.attachments)

            for x in message.attachments:
                print('url found in message.attachments:')
                print(x['url'])
                url = x['url']

                if message.author.name == "AlikyGong":
                    admin = discord.utils.get(message.server.members, id=environ['adminID'])
                    await client.send_message(admin, " Please add AlikyGong to the database, the screenshot may be in Spanish ->\n" + url)

                async def processImage(_url):
                    
                    r = requests.get(_url, stream = True)
                    rawText = pytesseract.image_to_string(Image.open(r.raw))

                    text = rawText
                    userTeam = "not set"

                    for role in message.author.roles:
                        print('Role: ' + role.name + "   ID: " + role.id)
                        if role.id == MYSTIC_ROLE_ID:
                            userTeam = "Mystic"
                            print('set team: ' + role.name)
                        if role.id == VALOR_ROLE_ID:
                            userTeam = "Valor"
                            print('set team: ' + role.name)
                        if role.id == INSTINCT_ROLE_ID:
                            userTeam = "Instinct"
                            print('set team: ' + role.name)

                    extracted_gym_name = (text[(text.find('a previous victory at')+21):text.find('Please visit the Gym')])

                    extracted_gym_name = extracted_gym_name.replace("!", "")
                    extracted_gym_name = extracted_gym_name.replace("\n", " ")

                    text = text.replace('|', 'l')
                    extractedDate = "not set"
                    
                    for month in months:
                        print(text.find(month))
                        if text.find(month) > -1:
                            extractedDate = text[text.find(month):text.find(month)+len(month)+25]
                            print("original extracted date -> " + extractedDate)
                            strNoMonth = text[len(month):]
                            print(strNoMonth)
                            strNoMonth = strNoMonth.strip()
                            startTime = strNoMonth[:strNoMonth.find('M')+1]
                            print(startTime)
                            extractedDate = month + " " + startTime
                            print("extracted this for date ->    " + extractedDate)
                            break

                    newSS = {
                        "discord_name": message.author.name,
                        "team": userTeam,
                        "gym_name": extracted_gym_name.strip(),
                        "date_extracted": extractedDate,
                        "unprocessed_image_to_string": rawText,
                        "image_url": url
                    }
                    
                    pyrebase_worker.upload(newSS)
                    await client.add_reaction(message, "\U0001F44D")





                    #  This allows user input        ---------        Do Not Delete        ---------        just commented out for testing
                    # def setInfo(msg):
                    #     return msg.content.startswith('$set')
                    # msg = await client.wait_for_message(author=message.author, check=setInfo)
                    # await client.add_reaction(msg, '\U0001F44D') 
                    # info = msg.content[len('$set'):].strip()
                    # info = info.split(" ")
                    # startTime = info[0]
                    # await client.send_message(message.channel, message.author.mention + " Your information:\nRaid location -> " + raidLocation + "\nRaid time -> " + raidTime + "\nDesired start time -> " + startTime)
                    #  This allows user input        ---------        Do Not Delete        ---------        just commented out for testing

            
            await processImage(url)
        



        if client.user in message.mentions:
            if 'thanks' in message.content.lower() or 'thank you' in message.content.lower():
                await client.send_message(message.channel, "Anything for you kid.")
            else:
                await client.send_message(message.channel, random.choice(emoji))



    await client.process_commands(message)
        










@client.command(pass_context=True)
async def pyrebaseGetOCR(context):
    print("pyrebaseGetOCR")
    if context.message.author.id == environ['adminID']:
        print("admin id confirmed")
        print("calling pyrebase_worker.getData()....")
        data = pyrebase_worker.getData()
       
        items = ""
        for item in data.each():
            itemDict = item.val()
            userInfo = "``` "
            userInfo += ("\nDate Uploaded -> " + itemDict["dateUploaded"] + "\nUser's Discord Name -> " + itemDict["discord_name"] + "\nUser's Team -> " + itemDict["team"] + \
                        "\nExtracted gym name -> " + itemDict["gym_name"] + "\nExtracted date -> " + itemDict["date_extracted"] + "\nUnprocessed text from image_to_string ->\n" + itemDict["unprocessed_image_to_string"] + "\n\nImage URL -> "  + itemDict["image_url"] + "\n ```")
            items += userInfo
        await client.send_message(context.message.author, " Here is the list of ocr data ->\n" + items)




@client.command(pass_context=True)
async def raiders(context):
    print("raiders")
    print("calling pyrebase_worker.getData()....")
    data = pyrebase_worker.getData()
    
    items = []
    for item in data.each():
        itemDict = item.val()
        userInfo = "``` "
        userInfo += (itemDict["discord_name"] + "   " + itemDict["team"] + \
                    "\n" + itemDict["gym_name"] + "   " + itemDict["date_extracted"] + " ```")
        items.append([itemDict["gym_name"], userInfo])
    
    for item in items:
        raidGroup = ""
        startingEntry = items.pop()
        raidGroup += startingEntry[1]
        for entry in items:
            if entry[0] == startingEntry[0]:
                individual =  (items.pop(items.index(entry)))
                raidGroup += individual[1]
        await client.send_message(context.message.channel, " Here is the list of raiders ->\n" + raidGroup)















async def emit():
    await client.wait_until_ready()
    while not client.is_closed:
        print("get request to /api/bot-report")
        r = requests.get('https://node-bot-dashboard.herokuapp.com/api/bot-report', {"bot":"@ExRaidBot", "status":"online"})
        print("response")
        print(str(r))
        await asyncio.sleep(4)
    



async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)



# client.loop.create_task(emit())
client.loop.create_task(list_servers())
client.run(TOKEN)
