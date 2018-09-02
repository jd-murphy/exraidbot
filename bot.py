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
import ocr_op


# ExRaidBot for BCS Pokemon Go - developed with love for this awesome community by  @Aydenandjordan  7/25/2018 
# developer: *slaps roof of this file* this bad boy could fit so much more f*@%king documentation in it..



TOKEN = environ['TOKEN'] 
BOT_PREFIX = ("!")

INSTINCT_EMOJI = "<:emoji_name:456205777389092895>" # <:emoji_name:456205777389092895> # instinct    These are the wrong emoji ids. get ids for 3ts
MYSTIC_EMOJI = "<:emoji_name:456205778022563851>" # <:emoji_name:456205778022563851> # mystic
VALOR_EMOJI = "<:emoji_name:456205778395725834>" # <:emoji_name:456205778395725834> # valor

MYSTIC_ROLE_ID = "276922105441026048"
VALOR_ROLE_ID = "276922104169889794"
INSTINCT_ROLE_ID = "276922106107658241"



RAIDS = ['Empty list']
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
    msg = ("Hey there, Trainer! \nThis bot allows you to sign up for your EX Raid. Just take a screenshot of your EX Raid pass and upload it in #ex_raids and I'll take care of the rest. " + \
    "If you want to see all the upcoming raids just type   **!raids**   To see who all is signed up for a specific raid, type   **!raiders [gym name]**   For example, if you are hava a pass for Winged Elm you can type   **!raiders winged**   and get a list of all the people who are signed up. "  + \
    "You can also share a link to help people sign up if they aren't on this discord server. You can just use the command   **!share**   to get the link! \nGood luck at your raid, Trainer!  " + random.choice(emoji))
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

                if message.author.name == "AlikyGong" or message.author.name == "GongAliky" or message.author.name == "DaddysLittleGirl":
                    admin = discord.utils.get(message.server.members, id=environ['adminID'])
                    await client.send_message(admin, " Check if screenshot was uploaded correctly from " + message.author.name + ". screenshot may be in another language ->\n" + url)


                async def processImage(_url):
                    
                    r = requests.get(_url, stream = True)
                   
                    result = ocr_op.processScreenshot(r.raw)
                  
                    if result["status"] == "success":
                        print("successfully processed screenshot")
                        print(result["status"])
                        print(result["date"])
                        print(result["gym"])
                    else:
                        admin = discord.utils.get(message.server.members, id=environ['adminID'])
                        await client.send_message(admin, " Trouble processing screenshot correctly from " + message.author.name + " Results are -> " + str(result) + " ->\n" + url)
                   
                    userTeam = "not set"
                    newSS = {}

                    try:
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

                        newSS = {
                            "discord_name": message.author.name,
                            "team": userTeam,
                            "gym_name": result["gym"],
                            "date_extracted": result["date"],
                            "unprocessed_image_to_string": result["rawText"],
                            "image_url": url
                        }
                    
                    except Exception as e: 
                        print("Exception (Most likely by design, Hook boi screenshot upload) -> " + str(e))
                        if message.author.name == "Hook boi":
                            trainerInfo = message.content
                            print("Hook boi posted screenshot. here is the trainer info from the webhook -> ")
                            print(trainerInfo)

                            info = trainerInfo.split(":")

                            newSS = {
                                "discord_name": info[1],
                                "team": info[3],
                                "gym_name": result["gym"],
                                "date_extracted": result["date"],
                                "unprocessed_image_to_string": result["rawText"],
                                "image_url": url
                            }




                    pyrebase_worker.upload(newSS)
                    await client.add_reaction(message, "\U0001F44D")




            
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
            userInfo += ("Name: " + itemDict["discord_name"] + "\nGym: " + itemDict["gym_name"] + \
                        "\nDate: " + itemDict["date_extracted"] + "\nUploaded: " + itemDict["dateUploaded"][0:10] + " ```")
                        # userInfo += ("\nDate Uploaded -> " + itemDict["dateUploaded"] + "\nUser's Discord Name -> " + itemDict["discord_name"] + "\nUser's Team -> " + itemDict["team"] + \
                        # "\nExtracted gym name -> " + itemDict["gym_name"] + "\nExtracted date -> " + itemDict["date_extracted"] + "\nUnprocessed text from image_to_string ->\n" + itemDict["unprocessed_image_to_string"] + "\n\nImage URL -> "  + itemDict["image_url"] + "\n ```")
            items += userInfo
            if len(items) > 1000:
                await client.send_message(context.message.author, " OCR data ->\n" + items)
                items = ""
        await client.send_message(context.message.author, " OCRdata ->\n" + items)




@client.command(pass_context=True)
async def raiders(context, gym):
    print("raiders")
    # print("calling pyrebase_worker.getData()....")
    # data = pyrebase_worker.getData()
    
    # items = []
    # _gymName = "not set"
    # _date = "not set"

    # for item in data.each():
    #     itemDict = item.val()
    #     userInfo = ""
    #     if _gymName == "not set":
    #         if gym.lower() in itemDict["gym_name"].lower():
    #             _gymName = itemDict["gym_name"]
    #             _date = itemDict["date_extracted"]

    #     userInfo += (itemDict["discord_name"] + "   " + itemDict["team"])

    #     items.append([itemDict["gym_name"], userInfo])


    # embed=discord.Embed(color=0x00a6dd)
    # embed.set_author(name=(_gymName + "  " + _date))

    # for item in items:
    #     if gym.lower() in item[0].lower():
            
    #         embed.add_field(name="Raider:", value=item[1], inline=True)
            
    # await  client.send_message(context.message.channel, embed=embed)
    await  client.send_message(context.message.channel, "You can view all raids and all raiders at this link! \n http://bit.ly/ViewRaids")





# @client.command(pass_context=True)
# async def rollcall(context, *gym):
#     print("rollcall")
#     print("calling pyrebase_worker.getData()....")
#     data = pyrebase_worker.getData()
#     gymString = " ".join(gym)
#     gymNameArray = gymString.lower().split(" ")
#     print("Gym name: ")
#     print(gym)
#     if "the" in gymNameArray: gymNameArray.remove("the")
#     if "park" in gymNameArray: gymNameArray.remove("park")
#     if "church" in gymNameArray: gymNameArray.remove("church")
#     print("Gym name filtered: ")
#     gym = " ".join(gymNameArray)
#     print(gym)
#     if len(gym) > 0:
    
#         items = []
#         _gymName = "not set"
#         _date = "not set"

#         for item in data.each():
#             itemDict = item.val()
#             userInfo = ""
#             if _gymName == "not set":
#                 if gym.lower() in itemDict["gym_name"].lower():
#                     _gymName = itemDict["gym_name"]
#                     _date = itemDict["date_extracted"]

#             userInfo += (itemDict["discord_name"] + "?" + itemDict["team"])

#             items.append([itemDict["gym_name"], userInfo])



#         for item in items:
#             if gym.lower() in item[0].lower():
                
#                 try:
#                     discordName = item[1].split('?')
#                     print("discordName = " + discordName[0])
#                     user = discord.utils.get(context.message.server.members, name=discordName[0])
#                     print("user")
#                     print(str(user))
#                     print("Roll call: " + user.name)
#                     await client.send_message(context.message.channel, user.mention + " testing out !rollcall for raid: " + gym)
#                 except Exception as e:
#                     print("member not found: " + item[1] + " Error -> " + str(e)) 
                
#         admin = discord.utils.get(context.message.server.members, id=environ['adminID'])
#         # await  client.send_message(context.message.channel, "You can also view all raids and all raiders at this link! \n http://bit.ly/ViewRaids")
#         await client.send_message(admin, "Roll call for " + gym + " was called!")
#     else:
#         client.send_message(context.message.channel, context.message.author.mention + " Hmmm, I couldn't find a gym result. try searching without the words 'the', 'park', or 'church' ")









@client.command(pass_context=True)
async def raids(context):
    print("raids")
    print("calling pyrebase_worker.getData()....")
    data = pyrebase_worker.getData()
    
   
    upcomingRaids = []
    _gymName = "not set"
    _date = "not set"

    for item in data.each():
        itemDict = item.val()
        raidInfo = ""

        if itemDict["gym_name"] != "not found":
            raidInfo += itemDict["gym_name"] + "  "
            raidInfo += itemDict["date_extracted"]
            upcomingRaids.append(raidInfo)

    raidsSet = set(upcomingRaids)
    upcomingRaids = list(raidsSet)



    embed=discord.Embed(color=0x00a6dd)
    embed.set_author(name=("Upcoming EX Raids currently in the database"))

    for raid in upcomingRaids:
        embed.add_field(name="Raid:", value=raid, inline=True)
            
    await  client.send_message(context.message.channel, embed=embed)
    await  client.send_message(context.message.channel, "You can also view all raids and all raiders at this link! \n http://bit.ly/ViewRaids")


    




@client.command(pass_context=True)
async def share(context):
    await  client.send_message(context.message.channel, "Here is a link you can share for signing up for EX Raids.\n http://bit.ly/EXRaidsBCS")



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
