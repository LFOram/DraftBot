import csv
from discord.ext import commands
from pathlib import Path
import datetime

BOT_PREFIX = ("?", "!")
Bot = commands.Bot
client = Bot(command_prefix=BOT_PREFIX)
TOKEN = Path('Token.txt').read_text()

#Array of all picks if needed in future
PICKS = []
FILE = ""

SHLDraftStarted = False
SMJHLDraftStarted = False

list = [""]*5 #initial list for pick dictionary
pick = {"Pick Number":list[0],"Team":list[1],"User":list[2],"Position":list[3],"Player":list[4]}

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


@client.command(name = "RemovePick",
                pass_context = True)
async def RemovePick(context,args):
    try:
        pickNo = int(args)
        for i,p in enumerate(PICKS):
            if int(p['Pick Number']) == pickNo:
                PICKS.pop(i)
                await client.say("Pick removed")
    except ValueError:
        await client.send_message(context.message.channel, "Please select a pick number")

@client.command(pass_context=True)
async def StartSHLDraft(context):
    global SHLDraftStarted
    SHLDraftStarted = True
    now = datetime.datetime.now()
    FILE = now.strftime("%Y-%m-%d-%h-%m-") + "SHLDraft" + ".csv"
    print(FILE)
    with open(FILE, 'w') as file:
        newWriter = csv.DictWriter(file, pick.keys())
        newWriter.writeheader()
    await client.send_message(context.message.channel, "Draft starting, SHL Mode")

@client.command(pass_context=True)
async def StartSMJHLDraft(context):
    global SMJHLDraftStarted
    SMJHLDraftStarted = True
    now = datetime.datetime.now()
    FILE = now.strftime("%Y-%m-%d-%h-%m-") + "SMJHLDraft" + ".csv"
    print(FILE)
    with open(FILE, 'w') as file:
        newWriter = csv.DictWriter(file, pick.keys())
        newWriter.writeheader()
    await client.send_message(message.channel, "Draft starting, SMJHL Mode")

@client.command(pass_context=True)
async def EndDraft(context):
    global SHLDraftStarted
    global SMJHLDraftStarted
    SHLDraftStarted = False
    SMJHLDraftStarted = False
    await client.send_message(context.message.channel, "Draft Ending")

@client.command(pass_context=True)
async def ListPicks(context):
    # function to list all picks
    print("listing picks")
    output = listAllPicks(PICKS)
    await client.send_message(context.message.channel, output)


@client.command(pass_context=True)
async def Kill(context):
    raise SystemExit

@client.command(pass_context=True)
async def test(ctx,arg):
    await client.say(arg)



@client.event
async def on_message(message): #New message event
    global SHLDraftStarted
    global SMJHLDraftStarted
    global pick
    global FILE

    if str(message.channel) == "official-picks" and message.author.bot == False:
        print(message.content.startswith("!"))
        if (SHLDraftStarted == True or SMJHLDraftStarted == True) and message.content.startswith("!") == False:  #If in the pick channel
            #parse message
            print(message.author)
            string = message.content #Get message
            list = string.split("-") #Split at -
            # strip spaces from input
            for i, item in enumerate(list):
                list[i] = item.strip()

            print([x.lower() for x in list])
            if "pass" in [x.lower() for x in list]:
                print("Pick(s) Passed")
                await client.send_message(message.channel, "Pick(s) Passed")
            else:
                try:
                   #Create dictionary for pick
                    if SHLDraftStarted == True:
                        pick = {"Pick Number":list[0],"Team":list[1],"User":list[2],"Position":list[3],"Player":list[4]}
                    elif SMJHLDraftStarted == True:
                        pick = {"Pick Number":list[0],"Team":list[1],"Player":list[2],"Position":list[3],"User":list[4]}

                    #Check Pick list for duplicate
                    if not any(p['User'] == pick['User'] for p in PICKS):
                        print("Not duplicate")

                        # Format output with key value pairs
                        string = ""
                        for key, value in pick.items():
                            string += key + ": " + value + ", "

                        # Output to discord
                        msg = await client.send_message(message.channel, "Pick recorded ``` " + string[:-2] +"```")  # cut off final comma
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

                            #Replace team with full name
                            pick['Team'] = pick['Team'].strip()
                            for i,team in enumerate(TeamList): #traverse list to correct team
                                if pick['Team'] in TeamList[i]: #find team
                                    pick['Team'] = team[0] #replace team with full team name

                            PICKS.append(pick) #add to pick list
                            with open(FILE, 'a') as file: #write pick to CSV file
                                newWriter = csv.DictWriter(file, pick.keys())
                                newWriter.writerow(pick)
                        elif res.reaction.emoji == "❎": #Cancel pick
                            await client.send_message(message.channel, "Pick canceled. Previous team remain on the clock")

                    else:
                        print("Duplicate Pick")
                        await client.send_message(message.channel, "Fucking idiot they've already been picked!")  # cut off final comma
                        #find previous pick
                        for p in PICKS:
                            if pick['User'] == p['User']:
                                # Format output with key value pairs
                                string = ""
                                for key, value in p.items():
                                    string += key + ": " + value + ", "
                                # Output to discord
                                msg = await client.send_message(message.channel,"```" + string[:-2] + "```")  # cut off final comma

                except IndexError:
                    await client.send_message(message.channel, "Follow the format dumb dumb")

            #Send message to confirm
        elif str(message.channel) == "official-picks" and message.author.bot == True:
            last_bot_message = message.id

    await client.process_commands(message)


def listAllPicks(Picks):
    output ="```"
    print("List all functions")
    for pick in Picks:
        string = ""
        for key, value in pick.items():
            string += key + ": " + value + ", "
        output = output + ("\n" + string[:-2])
    return (output + " ```")



#If you are reading this I am sorry, this is such bad code

client.run(TOKEN)