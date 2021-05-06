# Bot.py
import asyncio
import time
import os
import random
import re
from difflib import SequenceMatcher

import discord
from dotenv import load_dotenv

from github import Github
from pathlib import Path
import gspread

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
GH_TAGS_SHEET_ID = "125LetUS9LFb9gMc71yBZqX0heq1RzAQN2fGkad8TbmE"
CHILLOUT_TAGS_SHEET_ID = "1YlIv84-yh8SyX4AlFKcJY1KMPhDHZUoZVlxSC5Hr3vY"
TAG_RANGE_DEFAULT = 'Tags!A:D'
TAG_RANGE_NAMES = 'Tags!B:B'

gc = gspread.oauth(scopes=gspread.auth.DEFAULT_SCOPES)

pavilions = []
client = discord.Client()
adminChannelID = 755841743861317632  # default for chillout lounge

runeBotShort = 'rb'
tag_list_name = "tags.txt"
if not Path("./" + tag_list_name).exists():
    with open(tag_list_name, "w"):
        pass
numberLines = 0
text_file = open("HighSchoolDxD.txt", encoding="utf8")
# filtered_file = open("HighSchoolDxDFiltered.txt", encoding="utf8")
# filtered_file.write(text_file.read())
lines = text_file.read().split('\n')
# for i in range(len(lines) - 1):
#    if "Hiryuu Fansubs" in lines[i]:
#        while ""
text_file.close()


def setRepo(text):
    open("RepoInfo.txt", "w").close()
    if len(text) == 0:
        return
    if text.startswith('https://'):
        split = text.split('/')
        text = split[len(split) - 2] + '/' + split[len(split) - 1]
    file = open("RepoInfo.txt", "w")
    file.write("REPOINFO=" + text)
    file.close()


def getRepo():
    assertFile("RepoInfo.txt")
    file = open("RepoInfo.txt", "r")
    string = file.read()[9:]
    file.close()
    return string


def assertFile(text):
    if not os.path.isfile(text):
        setRepo(" ")


runeBotLoginMail = 'realrunebot@gmail.de'
runeBotLoginName = 'RealRuneBot'
runeBotLoginPass = 'runebot4eva!'

git = Github(runeBotLoginName, runeBotLoginPass)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def seconds():
    return 'second(s)'


def minutes():
    return 'minute(s)'


def hours():
    return 'hour(s)'


def days():
    return 'day(s)'


def durDict(str):
    options = {'s': seconds,
               'm': minutes,
               'h': hours,
               'd': days}
    return options[str]()


def checkIfRowsHaveName(rows, name) -> bool:
    for row in rows:
        if row[1] == name:
            return True
    return False


def nameExists(str) -> bool:
    f = open(tag_list_name, "r")
    tags = f.readlines()
    f.close()
    for line in tags:
        if str == line.split(';')[0]:
            return True
    return False


async def rping(message):
    users = set()
    for reaction in message.reactions:
        async for user in reaction.users():
            users.add(user)
    new_pings = '{}'.format(message.author.mention)
    for user in users:
        if user != client.user:
            new_pings += ' {}'.format(user.mention)
    await message.channel.send(new_pings)


async def timer(msg, duration, text):
    second_int = time.time()
    target_int = duration + second_int
    while True:
        if time.time() >= target_int:
            break
        await asyncio.sleep(1)
    await rping(msg)
    await msg.channel.send(f"Your countdown has ended: " + " ".join(text))


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    # fetch current pavilions


@client.event
async def on_message(message):
    global adminChannelID
    adminChannel = client.get_channel(adminChannelID)
    guild = discord.utils.get(client.guilds, name=GUILD)
    if message.author == client.user:
        return

    # repo crawler

    # DxD
    global lines
    secondList = []
    for i in range(len(lines)):
        if similar(message.content.lower(), lines[i].lower()) > 0.75 and len(lines[i]) > 3:
            if i + 1 <= len(lines):
                secondList.append(lines[i + 1])
    if len(secondList) > 0:
        await message.channel.send(secondList[random.randint(0, len(secondList) - 1)])

    # DIE TECHNIK THADDÄUS
    if 'technik' in message.content.lower():
        await message.channel.send('DIE TECHNIK, THADDÄUS!')

    # Dieser bot hat den style und das geld
    if 'style' in message.content.lower():
        await message.channel.send('und das Geld.')

    # Commands
    ## help
    if '!help' == message.content:
        await message.channel.send('Bot usages:'
                                   '\n- ' + runeBotShort + '!<command> - issue commands to RuneBot')
    if runeBotShort + '!adminhelp' == message.content:
        if not [x for x in message.author.roles if x.name == 'Admin']:
            return
        await adminChannel.send('Specific admin commands [start with ' + runeBotShort + '!admin]:'
                                                                                        '\n- users: Displays all users on server'
                                                                                        '\n- channel <set>: Shows a message in current admin channel. Sets current '
                                                                                        'channel as new admin channel with \'set\' argument'
                                                                                        '\n- tempban <userID> <duration> <unit>: WIP')
    if runeBotShort + '!help' == message.content:
        await message.channel.send('List of commands [start with ' + runeBotShort + '!]:'
                                                                                    '\n- help: Displays help'
                                                                                    '\n- Using > or ; has similar functions as in Grand Haven (Kingfisher/Sharkie)'
                                                                                    '\n'
                                                                                    '\nMemes:'
                                                                                    '\n- egal - Wendler'
                                                                                    '\n- mock - Mocks the last message'
                                                                                    '\n- bonk - bonk'
                                                                                    '\n- intelligent - no signs'
                                                                                    '\n- impostor - ejects all impostors'
                                                                                    '\n'
                                                                                    '\nAutomatic functions:'
                                                                                    '\n- Repeats \'f\', \'F\' and \':regional_indicator_f:\''
                                                                                    '\n- Knows the complete script of Highschool DxD Season 1'
                                                                                    '\n- DIE TECHNIK, THADDÄUS!')

    ## admin commands
    if runeBotShort + '!adminusers' == message.content:
        if not [x for x in message.author.roles if x.name == 'Admin']:
            return
        await adminChannel.send(message.author.mention)
        members = '[ID]/[Account Name]/[Nickname]'
        await adminChannel.send('Guild Members:\n' + members)
        retain = ''
        for member in guild.members:
            if isinstance(member.nick, str):
                temp = '\n- ' + str(member.id) + '\t' + member.name + '\t' + member.nick
            else:
                temp = '\n- ' + str(member.id) + '\t' + member.name + '\t' + member.name
            if len(temp) + len(retain) > 2000:
                await adminChannel.send(retain)
                retain = ''
            retain += temp
        await adminChannel.send(retain)

    if message.content.lower().startswith(runeBotShort + '!adminchannel'):
        if not [x for x in message.author.roles if x.name == 'Admin']:
            return
        args = message.content.lower().split()
        if len(args) == 1:
            await adminChannel.send("This is the current admin channel. ID: " + str(adminChannelID))
        elif args[1] == 'set':
            adminChannelID = message.channel.id

    if message.content.lower().startswith(runeBotShort + '!admintempban'):
        if not [x for x in message.author.roles if x.name == 'Admin']:
            return
        args = message.content.lower().split()
        if len(args) == 4:
            userID = int(args[1])
            if not isinstance(guild.get_member(userID), discord.Member):
                await adminChannel.send('User with ID ' + str(userID) + ' not found')
                return
            await adminChannel.send(
                'User with ID: ' + str(userID) + ' has been banned for ' + str(args[2]) + ' ' + durDict(args[3]))

    ## GH Command System
    if message.content.startswith('>') or message.content.startswith(';'):
        current_string = message.content[1:].split(' ')
        if current_string[0] == 't' or current_string[0] == 'tag' or current_string[0] == 'tags':
            sheet = gc.open("Chillout Tags").sheet1
            if current_string[1] == 'create':
                substring = current_string[2].split('\n')
                if len(substring) > 1:
                    temp_str = list()
                    temp_str.append(current_string[0])
                    temp_str.append(current_string[1])
                    i = 0
                    for val in substring:
                        temp_str.append(substring[i])
                        i += 1
                    i = 0
                    for val in current_string[3:]:
                        temp_str.append(current_string[3 + i])
                        temp_str.append('\n')
                    temp_str.pop()
                    current_string = temp_str
                try:
                    sheet.find(current_string[2], in_column=2)
                    await message.channel.send("Tag already exists.")
                except gspread.exceptions.CellNotFound:
                    sheet.append_row([current_string[2], ''.join(current_string[3:]), message.author.id])
                    await message.channel.send("Tag created.")
            elif current_string[1] == 'update':
                substring = current_string[2].split('\n')
                if len(substring) > 1:
                    temp_str = list()
                    temp_str.append(current_string[0])
                    temp_str.append(current_string[1])
                    i = 0
                    for val in substring:
                        temp_str.append(substring[i])
                        i += 1
                    i = 0
                    for val in current_string[3:]:
                        temp_str.append(current_string[3 + i])
                    current_string = temp_str
                try:
                    found_cell = sheet.find(current_string[2], in_column=2)
                    if int(message.author.id) != int(
                            sheet.cell(found_cell.row, 4, value_render_option='FORMULA').value) and not [x for x in
                                                                                                         message.author.roles
                                                                                                         if
                                                                                                         x.name == 'Admin']:
                        raise gspread.exceptions.CellNotFound
                    sheet.cell(found_cell.row, 3, value_render_option='FORMULA').value = ''.join(current_string[3:])
                    await message.channel.send("Tag updated.")
                except gspread.exceptions.CellNotFound:
                    await message.channel.send("Either you are not the owner of the tag, "
                                               "not an admin or the tag doesn't exist.")
            elif current_string[1] == 'delete':
                try:
                    if sheet.row_count <= 1:
                        sheet.append_row(['', '', ''])
                    found_cell = sheet.find(current_string[2], in_column=2)
                    if int(message.author.id) != int(
                            sheet.cell(found_cell.row, 4, value_render_option='FORMULA').value) and not [x for x in
                                                                                                         message.author.roles
                                                                                                         if
                                                                                                         x.name == 'Admin']:
                        raise gspread.exceptions.CellNotFound
                    sheet.delete_row(found_cell.row)
                    await message.channel.send("Tag deleted.")
                except gspread.exceptions.CellNotFound:
                    await message.channel.send("Either you are not the owner of the tag, "
                                               "not an admin or the tag doesn't exist.")
            elif current_string[1] == 'help':
                await message.channel.send("Possible parameters: help, create, update, delete, tag name")
            else:
                try:
                    found_cell = sheet.find(current_string[1], in_column=2)
                    await message.channel.send(sheet.cell(found_cell.row, 3, value_render_option='FORMULA').value)
                except gspread.exceptions.CellNotFound:
                    await message.channel.send("Tag doesn't exist.")
        if current_string[0] == 'ght' or current_string[0] == 'ghtag' or current_string[0] == 'ghtags':
            sheet = gc.open("GH Tags backup").sheet1
            try:
                found_cell = sheet.find(current_string[1], in_column=2)
                await message.channel.send(sheet.cell(found_cell.row, 3, value_render_option='FORMULA').value)
            except gspread.exceptions.CellNotFound:
                await message.channel.send("Tag doesn't exist.")
        if current_string[0] == 'rping':
            link = current_string[1].split('/')
            server_id = int(link[4])
            channel_id = int(link[5])
            msg_id = int(link[6])

            server = client.get_guild(server_id)
            channel = server.get_channel(channel_id)
            msg = await channel.fetch_message(msg_id)

            if msg.author == message.author or [x for x in message.author.roles if x.name == 'Admin']:
                await rping(msg)
        if current_string[0] == 'rem':
            if current_string[1] == 'help':
                await message.channel.send("Usage: >rem <time amount> <message>\nThe amount")
            else:
                time_amount = re.findall(r'\d+[smhd]', current_string[1])
                actual_hours = 0
                actual_minutes = 0
                actual_seconds = 0
                for point in time_amount:
                    if point[len(point) - 1] == 's':
                        actual_seconds += int(point[0:len(point) - 1])
                    if point[len(point) - 1] == 'm':
                        actual_minutes += int(point[0:len(point) - 1])
                    if point[len(point) - 1] == 'h':
                        actual_hours += int(point[0:len(point) - 1])
                total_seconds = int(actual_seconds) + int(actual_minutes) * 60 + int(actual_hours) * 60 * 60
                if not total_seconds <= 0:
                    await message.channel.send(
                        "Set timer for " + str(actual_hours) + 'h' + str(actual_minutes) + 'm' + str(
                            actual_seconds) + 's' + ".")
                    await message.add_reaction("⏰")
                    if len(current_string) >= 3:
                        await timer(message,
                                    int(actual_seconds) + int(actual_minutes) * 60 + int(actual_hours) * 60 * 60,
                                    current_string[2:])
                    else:
                        await timer(message,
                                    int(actual_seconds) + int(actual_minutes) * 60 + int(actual_hours) * 60 * 60,
                                    "No message given.")
                else:
                    await message.channel.send("Invalid time.")

    ## normal commands
    if runeBotShort + '!impostor' == message.content:
        for member in guild.members:
            for role in member.roles:
                if str(role).find('Impostor') != -1:
                    await message.channel.send(member.name + ' was An Impostor!')
    if runeBotShort + '!intelligent' == message.content:
        await message.channel.send('https://tenor.com/view/buzz-lightyear-no-sign-of-intelligent-life-dumb-toy-story'
                                   '-gif-11489315')
    if runeBotShort + '!bonk' == message.content:
        await message.channel.send('https://media1.tenor.com/images/ae34b2d6cbac150bfddf05133a0d8337/tenor.gif?itemid'
                                   '=14889944')
    if runeBotShort + '!egal' == message.content:
        await message.channel.send('https://giphy.com/gifs/vol2cat-oliver-egal-wendler-ZG5KTqutRAfZ6i5OVR')
    if runeBotShort + '!mock' == message.content:
        content = ""
        messages = await message.channel.history(limit=2).flatten()
        await messages[0].delete()

        whitelist = set('abcdefghijklmnopqrstuvwxyzöüä ABCDEFGHIJKLMNOPQRSTUVWXYZÖÜÄß0123456789')
        content = ''.join(filter(whitelist.__contains__, messages[1].content.lower()))

        newContent = ""
        toggle = bool(random.random().__round__())
        for c in content:
            if toggle:
                newContent += c.upper()
            else:
                newContent += c
            toggle = not toggle

        if newContent != "":
            await message.channel.send(newContent)

    # repo management
    if message.content.lower().startswith(runeBotShort + '!repo'):
        args = message.content.split()
        if len(args) == 1:
            await message.channel.send('Usage:'
                                       '\n...!repo set <insert repo link> - sets new repo'
                                       '\n...!repo issue <insert issue number of current repo> - shows issue with given number of current repo')
        elif args[1] == 'set':
            if len(args) > 2:
                setRepo(args[2])
                await message.channel.send('Repo set successfully as ' + getRepo())
        elif args[1] == 'issue':
            if not len(re.findall("\w+/\w+", getRepo())) == 1:
                await message.channel.send('Invalid repository format, use \'<user>/<repo name>\'.\nCurrent: '
                                           + getRepo())
                return
            if len(args) > 2:
                await message.channel.send('Getting Issue #' + args[2] + ' from ' + getRepo() +
                                           '\n Link: ' + 'https://github.com/' + getRepo() + '/issues/' + args[2])
                comment = git.get_repo(getRepo()).get_issue(int(args[2]))
                await message.channel.send('First Comment:\nBy User: '
                                           + str(comment.user.login)
                                           + '\nID: '
                                           + str(comment.id)
                                           + '\nCreated at: '
                                           + str(comment.created_at)
                                           + '\nMessage: '
                                           + str(comment.body)
                                           )

    # Pavillion management
    if message.content.lower().startswith(runeBotShort + '!pavillion'):
        if message.author == client.user:
            return
        args = message.content.split()
        if len(args) == 1:
            await message.channel.send(
                'Usage: !pavilion <help|erect|burn> [erect/burn: custom name] [erect: text/voice]')
            return
        if args[1] == 'help':
            await message.channel.send('Usage: !pavilion <help|erect|burn> | Every user is allowed one pavilion for '
                                       'voice and text respectively.')
        if args[1] == 'erect':
            await message.channel.send('Not implemented yet')
        if args[1] == 'burn':
            await message.channel.send('Not implemented yet')

    # Happy Birthday Function - Disabled, since not useful :/
    # if 'happy birthday' in message.content.lower():
    #    await message.channel.send('Happy Birthday! :partying_face:')

    # f-Bot
    if 'f' == message.content.lower() or '🇫' == message.content:
        await message.channel.send(message.content)


client.run(TOKEN)
