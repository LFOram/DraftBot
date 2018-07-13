import asyncio
import csv
import time
from discord.ext.commands import Bot

BOT_PREFIX = ("?", "!")
client = Bot(command_prefix=BOT_PREFIX)
TOKEN = 'NDY0MTA5MTU4MjM3NjAxODIy.Dh6LAw.NtaEigUvvWBgkH7vms3khyFQfqQ'

PICKS = []# Array of all picks if needed in future

list = [""]*5 #initial list for pick dictionary
pick = {"Pick Number":list[0],"Team":list[1],"User":list[2],"Position":list[3],"Player":list[4]}
#Write headers for CSV file
with open("picks.csv", 'w') as file:
    newWriter = csv.DictWriter(file, pick.keys())
    newWriter.writeheader()

@client.event
async def on_message(message): #New message event
    if str(message.channel) == "official-picks" and message.author.bot == False:  #If in the pick channel
        #parse message
        print(message.author)
        string = message.content #Get message
        list = string.split("-") #Split at -

        #Create dictionary for pick
        pick = {"Pick Number":list[0],"Team":list[1],"User":list[2],"Position":list[3],"Player":list[4]}

        #Check Pick list for duplicate
        if not any(p['User'] == pick['User'] for p in PICKS):
            print("Not duplicate")

            # Format output with key value pairs
            string = ""
            for key, value in pick.items():
                string += key + ": " + value + ", "

            # Output to discord
            msg = await client.send_message(message.channel, "Pick recorded " + string[:-2])  # cut off final comma
            #Get confirmation for pick
            #add initial reactions
            await client.add_reaction(msg,"✅")
            await client.add_reaction(msg,"❎")
            # Wait for not bot reaction
            bot = True
            while bot == True:
                res = await client.wait_for_reaction(["✅","❎"],message=msg) #waits for reaction to be added, returns reaction, user
                bot = res.user.bot #Check if reaction was initial bot reaction
            #User reactions
            if res.reaction.emoji == "✅": #Confirm pick
                await client.send_message(message.channel, "Pick confirmed. Next team on the clock")
                PICKS.append(pick) #add to pick list
                with open("picks.csv", 'a') as file: #write pick to CSV file
                    newWriter = csv.DictWriter(file, pick.keys())
                    newWriter.writerow(pick)
            elif res.reaction.emoji == "❎": #Cancel pick
                await client.send_message(message.channel, "Pick canceled. Previous team remain on the clock")

        else:
            print("Duplicate Pick")
            await client.send_message(message.channel, "Fucking idiot they've already been picked!")  # cut off final comma


        #Team detection. Ya know. this is a really bad way to do this.. oh well to late to change now. Redo this later?
        TeamList = [["Buffalo Stampede","Buffalo","Stampede","BUF"],
                    ["Hamilton Steelhawks","Hamilton","Steelhawks","HAM","Hawks"],
                    ["Manhattan Rage","Manhattan","Rage","MAN"],
                    ["Minnesota Chiefs","Minnesota","Chiefs","MIN"],
                    ["New England Wolfpack","New England","Wolfpack","NEW"],
                    ["Toronto North Stars","Toronto","North Stars","TOR",],
                    ["West Kendall Platoon","West Kendall","Platoon","WKP",],
                    ["Calgary Dragons","Calgary","Dragons","CAL"],
                    ["Edmonton Blizzard","Edmonton","Blizzard","EDM",],
                    ["Los Angeles Panthers","Los Angeles","Panthers","LAP"],
                    ["San Francisco Pride","San Francisco","Pride","SFP"],
                    ["Seattle Riot","Seattle","Riot","SEA","LOL"],
                    ["Texas Renegades","Texas","Renegades","TEX"],
                    ["Winnipeg Jets","Winnipeg","Jets","WPG"]
                    ]

        #Send message to confirm
    elif str(message.channel) == "official-picks" and message.author.bot == True:
        last_bot_message = message.id


# async def on_reaction_add(reaction):
#     if reaction.message == last_bot_message:
#         if reaction.emoji == "✅":
#             print("Confirmed")
#         elif reaction.emoji == "❎":
#             pass








client.run(TOKEN)