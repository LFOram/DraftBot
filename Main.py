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
    if str(message.channel) == "official-picks": #If in the pick channel
        #parse message
        string = message.content #Get message
        list = string.split("-") #Split at -

        #Create dictionary for pick
        pick = {"Pick Number":list[0],"Team":list[1],"User":list[2],"Position":list[3],"Player":list[4]}

        #Append pick dictionary to CSV file
        with open("picks.csv", 'a') as file:
            newWriter = csv.DictWriter(file, pick.keys())
            newWriter.writerow(pick)

        # output pick to terminal
        print(list)







client.run(TOKEN)