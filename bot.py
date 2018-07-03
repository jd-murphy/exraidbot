from __future__ import print_function
import os
import random
import requests
import asyncio
import csv
import discord
from discord.ext.commands import Bot
from discord import Game
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
# this bot made for the bcs pogo community with love


# testing text extraction 
import pytesseract    #   requires heroku buildpack!!!!!!!
# from tesseract import image_to_string
from PIL import Image
import aiohttp
import json
# testing text extraction

from os import environ
import boto3




TOKEN = 'NDM5OTQxODU5MTQyNDAyMDU4.Df2S-Q.m1JHaVAljyyosk6eF0Eoe2GM9IY'
BOT_PREFIX = ("!")
AWS_ACCESS_KEY_ID = environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = environ['AWS_SECRET_ACCESS_KEY']
# s3Client = boto3.client('s3')
s3Resource = boto3.resource('s3')

# Setup the Sheets API1join 
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# Call the Sheets API

SPREADSHEET_ID = '15rbINq27Qt5lN-xl2FutRyzE93o4dH381mpStNGKCLc' #mine
PIN_SPREADSHEET_ID = '1ocKnXUDbgy-9ty0tFE7gAx3PR1cY9dne5wfjPu9dymI'

INSTINCT_EMOJI = "<:emoji_name:456205777389092895>" # <:emoji_name:456205777389092895> # instinct
MYSTIC_EMOJI = "<:emoji_name:456205778022563851>" # <:emoji_name:456205778022563851> # mystic
VALOR_EMOJI = "<:emoji_name:456205778395725834>" # <:emoji_name:456205778395725834> # valor


# testing text extraction
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
# testing text extraction


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
    msg = ("To interact with the bot, type in the commands shown below in  **bold letters**\n    *Pro Tips!* :wink:\n" + \
        "        *Don't* type the square brackets.\n        *Do* type the exclamation point.\n\n" + \
        "**!raids**    To see a list of upcoming Ex Raids. Use the numbers from this list for the other commands, such as: \n      **!raiders 1** \n      **!join 2** \n      **!leave 3**\n\n" + \
        "**!raiders [number]**    To see a list of people signed up for the Ex Raid.\n\n" +  \
        # "**!join [number]**    Sign up for an Ex Raid.\n\n" + \
        "**!join [number] [trainer name] [start time] [team]**    Sign up for an Ex Raid.\n\n" + \
        "**!leave [number]**    Remove your name from the sheet for a raid.\n\n" + \
        "**!createNewExRaid [gym name]**    Create a new sheet for an Ex Raid that is not on the list.\n\n" + \
        "**!pin [gym name]**    Get a location pin for the gym. Please type one word unique to the gym name *OR* more than one word in quotation marks, such as: \n      **!pin fellowship**\n      **!pin \"sky cutter\" **\n\n" + \
        ":point_right:    Type   **!raids**   to get started! ")
    await client.say(msg)
        

        

@client.event
async def on_ready():
    resetRaids()
    loadGyms()
    await client.change_presence(game=Game(name="Pokemon Go, duh"))
    print("Logged in as " + client.user.name)





def resetRaids():
    RAIDS.clear()
    sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = sheet_metadata.get('sheets', '')
    for sheet in sheets:
        RAIDS.append(sheet.get("properties", {}).get("title"))





@client.command(description='Returns a list of all current EX Raids.', 
                brief='Returns a list of all current EX Raids.')
async def raids():
    RAIDS.clear()
    try:
        sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get('sheets', '')
        for sheet in sheets:
            RAIDS.append(sheet.get("properties", {}).get("title"))
            # sheet.get("properties", {}).get("title") 
            # sheet.get("properties", {}).get("sheetId")     # need str() to print this out
        msg = printRaids()
    except Exception as e:
        msg = "  (raids - Exception) " + str(e) + " \nHang on, we'll get this taken care of.\n\n <@361223731986825218>  HAAAALLLLPPPP!!!"
    await client.say(msg)





def printRaids():
    raidsString = ""
    raidsString = "Upcoming Ex Raids: " + "\n"
    i = 0
    for key in RAIDS: 
        i+=1
        raidsString+= (str(i) + ".     " + str(key) + "\n")
    return raidsString





@client.command(pass_context=True, 
                description='Lists all trainers that are signed up for a Raid.', 
                brief='Lists all trainers that are signed up for a Raid.')
async def raiders(context, number):
    resetRaids()
    try: 
        num = int(number)
        if (0 < num) and (num <= len(RAIDS)):
            if (RAIDS[num-1]) == 'Form Responses':
                RANGE_NAME = RAIDS[num-1] + "!C3:F100"
            else:
                RANGE_NAME = RAIDS[num-1] + "!A3:D100"

            result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
            values = result.get('values', [])
            if not values:
                msg = 'No data found.'
                print('No data found.')
            else:
                msg = ''
                # msg = 'Trainers attending ' + RAIDS[num-1] + ": \n"
                for cell in values:
                    if cell[0]:
                        try:
                            msg += (cell[0] + "\t")
                        except:
                            pass
                    else:
                        try:
                            msg += (cell[1] + "\t")
                        except:
                            pass

                    try:
                        msg += (cell[2] + "\t")
                    except:
                        pass
                    try:
                        if cell[3]:
                            team = cell[3].lower()
                            if team == 'instinct':
                                msg += INSTINCT_EMOJI
                            if team == 'mystic':
                                msg += MYSTIC_EMOJI
                            if team == 'valor':
                                msg += VALOR_EMOJI
                    except:
                        pass
                
                    msg += "\r\n"



                    # # pin = getPinForGym(gym_name) this needs to replace the hardcoded link below     ***********************
                    # for key, value in GYMS.items():
                    #     if (RAIDS[num-1]).lower() in key.lower():
                    #         gymPin = value


                    gymPin = "https://www.google.com/maps?q=30.616412,-96.3463220"



                    raidersString = msg
                    embed=discord.Embed(title="GPS pin for the gym", url=gymPin, color=0x2af8f6)
                    embed.set_author(name=(RAIDS[num-1]))
                    embed.add_field(name='Trainers signed up for this raid: ', value=raidersString, inline=True)
                    



        else:
            msg = "Try entering a number between 1 and " + str(len(RAIDS))
    except Exception as e:
        msg = "  (raiders - Exception) " + str(e) + " \nHang on, we'll get this taken care of.\n\n <@361223731986825218>  HAAAALLLLPPPP!!!"
    await client.say(embed=embed)






    




# new join
@client.command(pass_context=True, 
                description='Adds your name to the spreadsheet for a Raid.', 
                brief='Adds your name to the spreadsheet for a Raid.')
async def join(context, number):
    resetRaids()
    num = int(number)
    if (0 < num) and (num <= len(RAIDS)):
        # context.message.author.name
        raid = RAIDS[num-1]
        encodedRaid = raid.replace(' ', '+')
        encodedDiscordUserName =  context.message.author.name.replace(' ', '+')
        link = "https://docs.google.com/forms/d/e/1FAIpQLSe91_7jTnj2HDFO7FchoFNBgaGnSrtRa72jTs9Fck4XmeP2wA/viewform?usp=pp_url&entry.854648901=" + encodedRaid + "&entry.498196543=" + encodedDiscordUserName
        print('\n\n\nHere is the link ->\n', link)
        print('\nhere is the context.message.author.name -> ', context.message.author.name)
        # msg = ' Here is your link to sign up for ' + raid + "\n" + link
        embed=discord.Embed(title="Click here to sign up!", url=link, color=0x00ccf1)
        embed.set_author(name="Follow this link to sign up for your raid.\nThis link is for " + context.message.author.name + " only.")
 
        await client.send_message(context.message.channel, "Check yo DMs " + context.message.author.mention)
        # await client.add_reaction(context.message, '\U0001F44D')
        await client.send_message(context.message.author, embed=embed)

                


# @client.event
# async def on_reaction_add(reaction, user):
#     channel = reaction.message.channel
#     print(reaction.emoji)
#     await client.send_message(channel, '{} has added {} to the the message {}'.format(user.name,reaction.emoji,reaction.message.content))       
   



@client.command()
async def share():
    link = "https://goo.gl/forms/gbTUkEkzaMxAbgFy1"
    await client.say("Copy and paste this sign up link to share with others who are not on Discord.\n" + link)



# old join 
# @client.command(pass_context=True, 
#                 description='Adds your name to the spreadsheet for a Raid.', 
#                 brief='Adds your name to the spreadsheet for a Raid.')
# async def join(context, number, trainerName, startTime, team):
#     resetRaids()
#     try: 
#         num = int(number)
#         if (0 < num) and (num <= len(RAIDS)):
#             values = [
#                 [
#                     context.message.author.name,
#                     trainerName,
#                     startTime,
#                     team
#                 ]
#             ]
#             resource = {
#                 "majorDimension": "ROWS",
#                 "values": values
#                 }
#             range = RAIDS[num-1] + "!A1:D1"
#             service.spreadsheets().values().append(
#                 spreadsheetId=SPREADSHEET_ID,
#                 range=range,
#                 body=resource,
#                 valueInputOption="USER_ENTERED"
#                 ).execute()

#             msg = ", you have been added to " + RAIDS[num-1] + " " + random.choice(emoji)
#         else:
#             msg = "Try entering a number between 1 and " + str(len(RAIDS))
#     except Exception as e:
#         msg = "  (join - Exception) " + str(e) + " \nHang on, we'll get this taken care of.\n\n <@361223731986825218>  HAAAALLLLPPPP!!!"
#     await client.say(context.message.author.mention + msg)
   


@client.command(pass_context=True,
                description='Removes your name from the spreadsheet for a Raid.', 
                brief='Removes your name from the spreadsheet for a Raid.')
async def leave(context, number):
    resetRaids()
    try: 
        num = int(number)
        if (0 < num) and (num <= len(RAIDS)):
            sheetRange = RAIDS[num-1] + "!A1:A"
            result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,range=sheetRange).execute()
            sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
            sheets = sheet_metadata.get('sheets', '')
            print("\n\nsheets")
            print(sheets)
            title = sheets[num-1].get("properties", {}).get("title")
            print("\n\ntitle")
            print(title)
            sheet_id = sheets[num-1].get("properties", {}).get("sheetId")
            print("\n\nsheet_id")
            print(sheet_id)
            deleteItem = context.message.author.name

            rows = result.get('values')
            j=0
            for i in rows:
                j+=1
                print(i)
                try:
                    if i[0]:
                        print('found something! '+ i[0])

                        if i[0] == deleteItem:
                            print("\n\nGONNA DELETE THIS MOFUCKA: " + i[0])
                            print('row ' + str(j))
                            
                            
                            body = {
                                    "requests": [{
                                        "deleteDimension": {
                                            "range": {
                                            "sheetId": sheet_id,
                                            "dimension": "ROWS",
                                            "startIndex": j - 1,
                                            "endIndex": j
                                            }
                                        }
                                    }]
                                }


                            service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()
                            msg = ", you have been removed from " + RAIDS[num-1] + " :thumbsup:"
                        else:
                            msg = ", it doesn't look like you were signed up for that raid. Your name is not on the list. :thinking:"

                except Exception as e:
                     print(str(e))
                
        else:
            msg = "Try entering a number between 1 and " + str(len(RAIDS))
    except Exception as e:
        msg = "  (leave - Exception) " + str(e) + " \nHang on, we'll get this taken care of.\n\n <@361223731986825218>  HAAAALLLLPPPP!!!"
    await client.say(context.message.author.mention + msg)






@client.command(pass_context=True,
                description='Creates a new Ex Raid spreadsheet.', 
                brief='Creates a new Ex Raid spreadsheet.')
async def createNewExRaid(context, gym_name):
    resetRaids()
    try: 
        msg = "Would you like to create a new raid called " + gym_name + "?"

# need to add code to actually CREATE the NEW EX RAID SHEET
# 
# 
# 
# 
#           to do
# 
# 
# 
# 
# 
# need to add code to actually CREATE the NEW EX RAID SHEET

        msg = ", you have created a new raid called " + gym_name + " :thumbsup:   :clap: :clap: :clap:"
    except Exception as e:
        msg = "  (createNewExRaid - Exception) " + str(e) + " \nHang on, we'll get this taken care of.\n\n <@361223731986825218>  HAAAALLLLPPPP!!!"
    await client.say(context.message.author.mention + msg)






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
 







@client.command()
async def signUp():    
    await client.say('Click this link to sign up for an upcoming EX Raid \n\n https://goo.gl/forms/BkIdUUvn8Hra9Z692')






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
                SHEET_ID = "1ST_WxLsxyocBmhLn58PqsFvN98cTn36l1pJIm1IQoqs"

                r = requests.get(_url, stream = True)
                
                text = pytesseract.image_to_string(Image.open(r.raw))
                # text = image_to_string(Image.open(r.raw))

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

                await client.send_message(message.channel, message.author.mention + " Your pass for \n**" + raidLocation + "**\n**" + raidTime + "** was uploaded. " + random.choice(emoji) + "\n Type **$set [desired start time] [team name]** to finish signing up. \nFor example: \n    **$set hatch mystic**\n    **$set noon valor**\n    **$set 1:30 instinct**")
                
                def setInfo(msg):
                    return msg.content.startswith('$set')

                msg = await client.wait_for_message(author=message.author, check=setInfo)
                await client.add_reaction(msg, '\U0001F44D') 
                info = msg.content[len('$set'):].strip()
               
                info = info.split(" ")
                startTime = info[0]
                team = info[1]


                try: 
                    sheetName = ''
                    writeRange = ''
                    values = ''
                    resource = ''


                    values = [
                        [
                            message.author.name,
                            # trainerName,
                            startTime,
                            team
                        ]
                    ]
                    resource = {
                        "majorDimension": "ROWS",
                        "values": values
                        }

                    sheetName = (output[1] + " " + output[0])
                    
                    writeRange = (sheetName + "!A1:D")
                    

                    try:

                        writeRange = ("'" + sheetName + "'!A:D")
                        # body = {
                        #         'values': values
                        #     }
                        
                        ####
                        result = service.spreadsheets().values().get(spreadsheetId=SHEET_ID, range=writeRange).execute()
                        retrievedValues = result.get('values', [])
                        print('retrievedValues -> ')
                        print(retrievedValues)
                        print('printing elements .... ')
                        newValues = []
                        for element in retrievedValues:
                            print(element)
                            newValues.append(element)
                        
                        newValues.append([
                            message.author.name,
                            startTime,
                            team
                        ])
                        print('newValues -> ')
                        print(newValues)


                        ####
                        body = {
                                'values': newValues
                            }
                        result = service.spreadsheets().values().update(
                            spreadsheetId=SHEET_ID, range=writeRange,
                            valueInputOption="USER_ENTERED", body=body).execute()



                        msg = " you were added successfully!"

                    except Exception as e:
                        print("PROBLEM")
                        print('Attempt to create sheet')

            
                        writeRange = ("'" + str(sheetName) + "'!A1:D10")
                        body = {
                            "requests": [
                                {
                                "addSheet": {
                                    "properties": {
                                    "title": sheetName
                                        }
                                    }
                                },
                                # {
                                # "append": {
                                #     "properties": {
                                #     "title": sheetName
                                #         }
                                #     }
                                # },

                            ]
                        }

                        service.spreadsheets().batchUpdate(spreadsheetId=SHEET_ID, body=body).execute()  
                        print('sheet created')
                        print('adding first user')
                     

                        try:
                            writeRange = ("'" + sheetName + "'!A1:D")
                            body = {
                                    'values': values
                                }
                            result = service.spreadsheets().values().update(
                                spreadsheetId=SHEET_ID, range=writeRange,
                                valueInputOption="USER_ENTERED", body=body).execute()

                            msg = " you were added successfully!"
                        except Exception as e:
                            print('something isnt working right .........' + str(e))

                
                except Exception as e:
                    msg = "  (join - Exception) " + str(e) + " \nHang on, we'll get this taken care of.\n\n <@361223731986825218>  HAAAALLLLPPPP!!!"
                await client.send_message(message.channel, message.author.mention + msg)



                # await client.add_reaction(message, '\U0001F44D') 
       
        await processImage(url)
        # testing text extraction from image




    
    if client.user in message.mentions:
        if 'fuck you' in message.content.lower() or 'fuck off' in message.content.lower():
            await client.send_message(message.channel, ("yo, chill tf out\n\n\n**Blacklist user:** " + message.author.mention))
        elif 'you suck' in message.content.lower():
            await client.send_message(message.channel, ("okay, then don't ask me to do anything for you\n\n\n**Blacklist user:** " + message.author.mention + "\nbye, felicia   :nail_care:"))
        elif 'thanks' in message.content.lower() or 'thank you' in message.content.lower():
            await client.send_message(message.channel, "Anything for you kid.")
        else:
            await client.send_message(message.channel, (random.choice(mentionResponses)))

    if 'bad bot' in message.content.lower():
        await client.send_message(message.channel, "I will try to behave.")
    elif 'good bot' in message.content.lower():
        await client.send_message(message.channel, ":heart_eyes::heart_eyes::heart_eyes:")
    

    await client.process_commands(message)
        





@client.command(pass_context=True)
async def showEmojis(context):    
    
    for x in client.get_all_emojis():
        print(x.id)
    await client.say("<:emoji_name:456205777389092895><:emoji_name:456205778022563851><:emoji_name:456205778395725834>")

   

@client.command(pass_context=True)
async def discordVersion(context):
    await client.say(discord.__version__)


@client.command(pass_context=True)
async def rank(context, action, role):
    print('action: ' + action)
    print('role: ' + role)
    user = context.message.author
    role = discord.utils.get(user.server.roles, name="testRole")

    if action.lower() == 'join':    
        await client.add_roles(user, role)
        await client.send_message(context.message.channel, "you've been added to " + str(role) + " :thumbsup:" + user.mention)
        await client.send_message(user, 'To add a phone number for text notifications for your role, type: **!set [cell-phone-number]**  \njust like this -> **!set 555-123-1234** ')
        def setInfo(msg):
            return msg.content.startswith('!set')
        msg = await client.wait_for_message(author=user, check=setInfo)
        info = msg.content[len('$set'):].strip()       
        info = info.split(" ")
        phoneNumber = info[0]
        print('phone: ' + str(phoneNumber))

        
        # for bucket in s3.buckets.all():
        #     print(bucket.name)
        
        # obj = s3.Bucket('user-profile-bucket-ex-raid-bot').Object('roleProfiles.txt')


        bucket = 'user-profile-bucket-ex-raid-bot'
        fileName = 'roleProfiles.csv'
        
        s3Resource.Object(bucket, fileName).download_file(fileName)
        with open(fileName, 'a') as f:
            f.write(user.name + ',' + str(phoneNumber) + ',')
            s3Resource.Bucket(bucket).upload_file(fileName,fileName)
            print('upload complete')



     
        # s3Client.get_object(Body=df,Bucket='user-profile-bucket-ex-raid-bot', Key='roleProfiles.csv')
        








        # with open(obj, 'a+') as f:
        #     for line in f:
        #         print('read from file -> ' + str(line))
        #     f.write(str(user.name) + ',' + str(phoneNumber) + ',')
        #     s3.Bucket('user-profile-bucket-ex-raid-bot').put_object(Key='roleProfiles.txt', Body=f)

       
        await client.send_message(user, 'your phone number ' + str(phoneNumber) + ' will be set for notifications. remove your number at any time by private messaging @ExRaidBot "!removePhone"')

    elif action.lower() == 'leave':
        await client.remove_roles(user, role)
        await client.say(user.mention + "you've been removed from " + str(role) + " :thumbsup:")




@client.command(pass_context=True)
async def removePhone(context):
    print('implement !removePhone')
    await client.say('implement !removePhone')

# async def list_servers():
#     await client.wait_until_ready()
#     while not client.is_closed:
#         print("Current servers:")
#         for server in client.servers:
#             print(server.name)
#         await asyncio.sleep(6)


# client.loop.create_task(list_servers())

client.run(TOKEN)
