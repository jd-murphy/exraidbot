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






TOKEN = environ['TOKEN'] 
BOT_PREFIX = ("!")

INSTINCT_EMOJI = "<:emoji_name:456205777389092895>" # <:emoji_name:456205777389092895> # instinct
MYSTIC_EMOJI = "<:emoji_name:456205778022563851>" # <:emoji_name:456205778022563851> # mystic
VALOR_EMOJI = "<:emoji_name:456205778395725834>" # <:emoji_name:456205778395725834> # valor

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
mentionResponses = [
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
        'I\'m ready to party',
        'Wassup?',
        'Howdy!',
        'I\'m heading to Walmart, want anything?',
        'Hey, cutie',
        'Gig em!',
        'I\'m still here',
        'At your beck and call.',
        'It\'s a great day to be a bot!',
        'Checkitoutcheckitoutcheckitoutcheckitout',
        'Can you hear me now?',
        'Yer a wizard, Harry.',
        'Have you tried turning it off and on again?',
        '**POGO IS LIFE**',
        '*@ExRaidBot is typing...*',
        'Some **BODY** once told me...', 
        'I got you, fam',
        'What happens on Discord, stays on Discord.',
        'E.X. raid bot phone home',
        'Bot. James Bot.',
        'Pikachu! I choose you!',
        'I hereby bestow shiny Magikarp luck upon you.',
        '#winning',
        'Omg I can\'t even',
        '*insert witty bot response*',
        'Talk to me.',
        'Okay, Let\'s start over. Hi, I\'m bot.',
        '*Hakuna Matata*',
        'Anybody want a peanut?',
        'You keep using that word. I do not think it means what you think it means.',
        'Yoo-Hoo! Big summer blowout!',
        'Just keep swimming.',
        'Fish are friends, not food.',
        '*A wild Squirtle appeared!*',
        '**Gotcha!**',
        '**Critical catch!**',
        '*A wild Totodile appeared!*', 
        '*A wild Eevee appeared!*',
        '*A wild Jigglypuff appeared!*',
        '*A wild Charmander appeared!*',
        'Some people would say I\'m just a bot...',
        'beep boop',
        'Shh. Be vewy vewy quiet. I\'m hunting wabbits!',
        'I knew I shoulda taken that left turn at Albuquerque...',
        'Cash me outside, howbow dah',
        'RIP Harambe',
        'Saturdays are for cracking open a cold one with the bots.',
        '01101001 00100000 01101000 01100101 01100001 01110010 01110100 00100000 01100100 01101001 01110011 01100011 01101111 01110010 01100100'
    ]



client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')
@client.command()
async def help():
    msg = ("implement help command ya dummy")
    await client.say(msg)
        



@client.event
async def on_ready():
    loadGyms()
    await client.change_presence(game=Game(name="Pokemon Go, duh"))
    print("Logged in as " + client.user.name)
   



@client.command()
async def share():
    link = "https://goo.gl/forms/gbTUkEkzaMxAbgFy1" # change this so not google sheets
    await client.say("Copy and paste this sign up link to share with others who are not on Discord.\n" + link)




@client.command(pass_context=True,
                description='Get a location pin for the gym.', 
                brief='Get a location pin for the gym.')
async def pin(context, gym_name):    
    matches = []
    for key, value in GYMS.items():
        if gym_name.lower() in key.lower():
            name = key
            gym = value
            matches.append([name, gym])

    print('matches contains ' + str(len(matches)) + ' results')
    if len(matches) > 1:
        
        gymsString = ''
        i = 1
        print("matching gyms: \n")
        for k in matches:
            print(k[0] + " " + k[1])
            gymsString += (str(i) + ".  " + k[0] + "\n")
            i+=1
        
        await client.send_message(context.message.channel, 'Were you looking for one of these gyms?\n' + gymsString + "\nType **$pin [number]** to get your pin")

        def check(msg):
            return msg.content.startswith('$pin')

        message = await client.wait_for_message(author=context.message.author, check=check)
        num = message.content[len('$pin'):].strip()
        print('num: ' + str(num))
        await client.send_message(message.channel, matches[int(num)-1][0] + "\n" + matches[int(num)-1][1])
    else:        
        await client.say(matches[0][0] + "\n" + matches[0][1])
 



def loadGyms():
    with open("gyms.txt", mode="r") as infile:
        reader = csv.reader(infile)
        for row in reader:
            k = row[0]
            v = row[2]
            GYMS[k] = v
    print(GYMS['Dixie Chicken'])
    




















@client.event
async def on_message(message):

    if message.attachments:
        print('message with attachment from:')
        print(message.author)
        print('message.attachments:')
        print(message.attachments)

        for x in message.attachments:
            print('url found in message.attachments:')
            print(x['url'])
            url = x['url']
            async def processImage(_url):
                

                r = requests.get(_url, stream = True)
                
                text = pytesseract.image_to_string(Image.open(r.raw))

                await client.send_message(message.channel, message.author.mention + "Here is the preprocessed image_to_string() result: \n\n" + text)
               

                for month in months:
                    if month in text:
                        text = (text[text.find(month):text.find('Get directions')])
                        break

                text = text.split('\n')
                output = []
                for chunk in text:
                    if not chunk.isspace() and chunk is not '' and chunk is not None:
                        output.append(chunk)

                print('\n\n----- output -----')
                print(message.author)
                print("Date: " + output[0])
                print("Gym: " + output[1])
                print("\n\n")


                raidLocation = output[1]
                raidTime = output[0]
                raidTime = raidTime.split(' ')
                raidTime = (raidTime[0] + ' ' + raidTime[1] + ' ' + raidTime[2] + ' ' + raidTime[3])
                ##########################

                await client.send_message(message.channel, message.author.mention + " Your pass for \n**" + raidLocation + "**\n**" + raidTime + "** was uploaded. " + random.choice(emoji) )




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
            await client.send_message(message.channel, (random.choice(mentionResponses)))



    await client.process_commands(message)
        































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
        await asyncio.sleep(120)



# client.loop.create_task(emit())
client.loop.create_task(list_servers())
client.run(TOKEN)
