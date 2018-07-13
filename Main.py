import asyncio
import csv
from discord.ext.commands import Bot

BOT_PREFIX = ("?", "!")
client = Bot(command_prefix=BOT_PREFIX)
TOKEN = 'NDY0MTA5MTU4MjM3NjAxODIy.Dh6LAw.NtaEigUvvWBgkH7vms3khyFQfqQ'

#PICKS = []#Unused. Array of all picks if needed in future

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


        #Append pick dictionary to CSV file
        with open("picks.csv", 'a') as file:
            newWriter = csv.DictWriter(file, pick.keys())
            newWriter.writerow(pick)

        #Format output with key value pairs
        string = ""
        for key,value in pick.items():
            string += key + ": " + value + ", "

        #Output to discord
        await client.send_message(message.channel, "Pick recorded " + string[:-2])#cut off final comma







client.run(TOKEN)