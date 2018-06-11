from __future__ import print_function
import os
import random
import requests
import asyncio
import csv
from discord.ext.commands import Bot
from discord import Game
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
# this bot made for the bcs pogo community with love


TOKEN = 'NDM5OTQxODU5MTQyNDAyMDU4.Df2S-Q.m1JHaVAljyyosk6eF0Eoe2GM9IY'
BOT_PREFIX = ("$", "!")

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
        ':thumbsup:'
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
        'Don\'t call me that in public...',
        'Hey, cutie',
        'Gig em!',
        'I\'m still here',
        'At your beck and call.',
        'It\'s a great day to be a bot!',
        'Checkitoutcheckitoutcheckitoutcheckitout',
        'Can you hear me now?',
        'You\'re a wizard, Harry.',
        'Have you tried turning it off and on again?',
        '**POGO IS LIFE**',
        '*@ExRaidBot is typing...*',
        'I\'m not that innocent',
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
        'Error 404: response not found',
        'Talk to me.',
        'Okay, Let\'s start over. Hi, I\'m bot.' 
    ]



client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')
@client.command()
async def help():
    msg = ("To interact with the bot, type in the commands shown below in  **bold letters**\n    *Pro Tips!* :wink:\n" + \
        "        *Don't* type the square brackets.\n        *Do* type the exclamation point.\n\n" + \
        "**!raids**    To see a list of upcoming Ex Raids. Use the numbers from this list for the other commands, such as: \n      **!raiders 1** \n      **!join 2** \n      **!leave 3**\n\n" + \
        "**!raiders [number]**    To see a list of people signed up for the Ex Raid.\n\n" +  \
        "**!join [number]**    Sign up for an Ex Raid.\n\n" + \
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
            RANGE_NAME = RAIDS[num-1] + "!A3:B100"
            result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
            values = result.get('values', [])
            if not values:
                msg = 'No data found.'
                print('No data found.')
            else:
                msg = 'Trainers attending ' + RAIDS[num-1] + ": \n"
                for cell in values:
                    if cell[0] == '': 
                        msg += (cell[1] + "\n")
                    else:
                        msg += (cell[0]  + "\n")
        else:
            msg = "Try entering a number between 1 and " + str(len(RAIDS))
    except Exception as e:
        msg = "  (raiders - Exception) " + str(e) + " \nHang on, we'll get this taken care of.\n\n <@361223731986825218>  HAAAALLLLPPPP!!!"
    await client.say(msg)



@client.command(pass_context=True, 
                description='Adds your name to the spreadsheet for a Raid.', 
                brief='Adds your name to the spreadsheet for a Raid.')
async def join(context, number):
    resetRaids()
    try: 
        num = int(number)
        if (0 < num) and (num <= len(RAIDS)):
            values = [
                [
                    context.message.author.name
                ]
            ]
            resource = {
                "majorDimension": "ROWS",
                "values": values
                }
            range = RAIDS[num-1] + "!A1:B1"
            service.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=range,
                body=resource,
                valueInputOption="USER_ENTERED"
                ).execute()

            msg = ", you have been added to " + RAIDS[num-1] + " " + random.choice(emoji)
        else:
            msg = "Try entering a number between 1 and " + str(len(RAIDS))
    except Exception as e:
        msg = "  (join - Exception) " + str(e) + " \nHang on, we'll get this taken care of.\n\n <@361223731986825218>  HAAAALLLLPPPP!!!"
    await client.say(context.message.author.mention + msg)
   


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
    # RANGE_NAME = "All!A2:C250"
    # result = service.spreadsheets().values().get(spreadsheetId=PIN_SPREADSHEET_ID, range=RANGE_NAME).execute()
    # values = result.get('values', [])
    # if not values:
    #     msg = 'No data found.'
    #     print('No data found.')
    # else:
    #     for cell in values:
    #         msg += (cell[0] + ": \n" + cell[2])
    # await client.say(msg)




    # gym = (value for key, value in GYMS.items() if gym_name.lower in key.lower())

    for key, value in GYMS.items():
        if gym_name.lower() in key.lower():
            gym = value

    # gym = GYMS.get('Dixie Chicken')
    # print("\n\ngym " + gym)
    if gym is None:
        gym = "Sorry, try searching a different keyword."

    await client.say(gym)


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
    
    if client.user in message.mentions:
        if 'fuck you' in message.content.lower() or 'fuck off' in message.content.lower():
            await client.send_message(message.channel, ("yo, chill tf out\n\n\n**Blacklist user:** " + message.author.mention))
        elif 'you suck' in message.content.lower():
            await client.send_message(message.channel, ("okay, then don't ask me to do anything for you\n\n\n**Blacklist user:** " + message.author.mention + "\nbye, felicia   :nail_care:"))
        else:
            await client.send_message(message.channel, (random.choice(mentionResponses)))
    await client.process_commands(message)
        

# async def list_servers():
#     await client.wait_until_ready()
#     while not client.is_closed:
#         print("Current servers:")
#         for server in client.servers:
#             print(server.name)
#         await asyncio.sleep(6)


# client.loop.create_task(list_servers())

client.run(TOKEN)
