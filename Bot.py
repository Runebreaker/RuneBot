# Bot.py
import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


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

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_message(message):
    guild = discord.utils.get(client.guilds, name=GUILD)
    if message.author == client.user:
        return

    # Commands
    ## help
    if '!helpadmin' == message.content:
        await message.channel.send('Specific admin commands:'
                                   '- admin!users: Displays all users on server')
    if '!help' == message.content:
        await message.channel.send('List of commands:'
                                   '\n- !help: Displays help'
                                   '\n'
                                   '\nMemes:'
                                   '\n- !egal - Wendler'
                                   '\n- !mock - Mocks the last message'
                                   '\n'
                                   '\nAutomatic functions:'
                                   '\n- Repeats \'f\', \'F\' and \':regional_indicator_f:\'')

    ## admin commands
    if 'admin!users' == message.content:
        adminChannel = client.get_channel(755841743861317632)
        await adminChannel.send(message.author.mention)
        members = '\n - '.join([member.name for member in guild.members])
        await adminChannel.send('Guild Members:\n - ' + members)
    if message.content.lower().startsWith('admin!tempban'):
        if 'Admin' not in message.author.roles:
            return
        args = message.content.lower().split()
        if len(args) != 4:
            memID = client.users.get("name", args[1]).id
            adminChannel = client.get_channel(755841743861317632)
            await adminChannel.send('User with ID: ' + memID + ' has been banned for ' + durDict(args[3]))

    ## normal commands
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

    # Happy Birthday Function - Disabled, since not useful :/
    # if 'happy birthday' in message.content.lower():
    #    await message.channel.send('Happy Birthday! :partying_face:')

    # f-Bot
    if 'f' == message.content.lower() or '🇫' == message.content:
        await message.channel.send(message.content)


client.run(TOKEN)
