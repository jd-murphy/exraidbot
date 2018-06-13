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

INSTINCT_EMOJI = "<:emoji_name:456205777389092895>" # <:emoji_name:456205777389092895> # instinct
MYSTIC_EMOJI = "<:emoji_name:456205778022563851>" # <:emoji_name:456205778022563851> # mystic
VALOR_EMOJI = "<:emoji_name:456205778395725834>" # <:emoji_name:456205778395725834> # valor

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
                            msg += (cell[0] + "     ")
                        except:
                            pass
                    else:
                        try:
                            msg += (cell[1] + "     ")
                        except:
                            pass

                    try:
                        msg += (cell[2] + "     ")
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
                
                    msg += "\n\n"

                    

                    raidersString = msg
                    embed=discord.Embed(title="GPS pin for the gym", url="https://www.google.com/maps?q=30.608839,-96.3372580", color=0x2af8f6)
                    embed.set_author(name="Staking the Claim 6/12/2018")
                    embed.add_field(name='Trainers signed up for this raid: ', value=raidersString, inline=True)
                    # embed.add_field(name='Start Time', value='second', inline=False)
                    # embed.add_field(name='Team', value='third', inline=False)



        else:
            msg = "Try entering a number between 1 and " + str(len(RAIDS))
    except Exception as e:
        msg = "  (raiders - Exception) " + str(e) + " \nHang on, we'll get this taken care of.\n\n <@361223731986825218>  HAAAALLLLPPPP!!!"
    # await client.say(msg)
    await client.say(embed=embed)





# @client.command(pass_context=True)
# async def embedRaiders(context, raiders):
#     raidersString = ''
#     embed=discord.Embed(title="GPS pin for the gym", url="https://www.google.com/maps?q=30.608839,-96.3372580", color=0x2af8f6)
#     embed.set_author(name="Staking the Claim 6/12/2018")
#     embed.add_field(name='Trainer Name', value=raidersString, inline=False)
#     # embed.add_field(name='Start Time', value='second', inline=False)
#     # embed.add_field(name='Team', value='third', inline=False)
#     await client.say(embed=embed)
    





@client.command(pass_context=True, 
                description='Adds your name to the spreadsheet for a Raid.', 
                brief='Adds your name to the spreadsheet for a Raid.')
async def join(context, number, trainerName, startTime, team):
    resetRaids()
    try: 
        num = int(number)
        if (0 < num) and (num <= len(RAIDS)):
            values = [
                [
                    context.message.author.name,
                    trainerName,
                    startTime,
                    team
                ]
            ]
            resource = {
                "majorDimension": "ROWS",
                "values": values
                }
            range = RAIDS[num-1] + "!A1:D1"
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

    for key, value in GYMS.items():
        if gym_name.lower() in key.lower():
            gym = value

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

    #     if x.id == "294956739688923136":
    # await client.add_reaction(message,str(x))




        





# async def list_servers():
#     await client.wait_until_ready()
#     while not client.is_closed:
#         print("Current servers:")
#         for server in client.servers:
#             print(server.name)
#         await asyncio.sleep(6)


# client.loop.create_task(list_servers())

client.run(TOKEN)
