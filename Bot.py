# Bot.py
import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

pavilions = []
client = discord.Client()
adminChannelID = 755841743861317632 #default for chillout lounge

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

    # Commands
    ## help
    if 'admin!help' == message.content:
        if not [x for x in message.author.roles if x.name == 'Admin']:
            return
        await adminChannel.send('Specific admin commands:'
                                '\n- admin!users: Displays all users on server'
                                '\n- admin!channel <set>: Shows a message in current admin channel. Sets current '
                                'channel as new admin channel with \'set\' argument'
                                '\n- admin!tempban <userID> <duration> <unit>: WIP')
    if '!help' == message.content:
        await message.channel.send('List of commands:'
                                   '\n- !help: Displays help'
                                   '\n'
                                   '\nMemes:'
                                   '\n- !egal - Wendler'
                                   '\n- !mock - Mocks the last message'
                                   '\n- !bonk - bonk'
                                   '\n- !intelligent - no signs'
                                   '\n'
                                   '\nAutomatic functions:'
                                   '\n- Repeats \'f\', \'F\' and \':regional_indicator_f:\'')

    ## admin commands
    if 'admin!users' == message.content:
        if not [x for x in message.author.roles if x.name == 'Admin']:
            return
        await adminChannel.send(message.author.mention)
        members = 'ID/Account Name/Nickname'
        for member in guild.members:
            if isinstance(member.nick, str):
                members += '\n- ' + str(member.id) + '\t' + member.name + '\t' + member.nick
            else:
                members += '\n- ' + str(member.id) + '\t' + member.name + '\t' + member.name
        await adminChannel.send('Guild Members:\n' + members)

    if message.content.lower().startswith('admin!channel'):
        if not [x for x in message.author.roles if x.name == 'Admin']:
            return
        args = message.content.lower().split()
        if len(args) == 1:
            await adminChannel.send("This is the current admin channel. ID: " + str(adminChannelID))
        elif args[1] == 'set':
            adminChannelID = message.channel.id

    if message.content.lower().startswith('admin!tempban'):
        if not [x for x in message.author.roles if x.name == 'Admin']:
            return
        args = message.content.lower().split()
        if len(args) == 4:
            userID = int(args[1])
            if not isinstance(guild.get_member(userID), discord.Member):
                await adminChannel.send('User with ID ' + str(userID) + ' not found')
                return
            await adminChannel.send('User with ID: ' + str(userID) + ' has been banned for ' + str(args[2]) + ' ' + durDict(args[3]))

    ## normal commands
    if '!intelligent' == message.content:
        await message.channel.send('https://tenor.com/view/buzz-lightyear-no-sign-of-intelligent-life-dumb-toy-story-gif-11489315')
    if '!bonk' == message.content:
        await message.channel.send('https://media1.tenor.com/images/ae34b2d6cbac150bfddf05133a0d8337/tenor.gif?itemid=14889944')
    if '!egal' == message.content:
        await message.channel.send('https://giphy.com/gifs/vol2cat-oliver-egal-wendler-ZG5KTqutRAfZ6i5OVR')
    if '!mock' == message.content:
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

    # Pavillion management
    if message.content.lower().startswith('!pavillion'):
        if message.author == client.user:
            return
        args = message.content.split()
        if len(args) == 1:
            await message.channel.send('Usage: !pavilion <help|erect|burn>')
            return
        if args[1] == 'help':
            await message.channel.send('Usage: !pavilion <help|erect|burn> | Every user is allowed one pavilion for voice and text respectively.')
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
