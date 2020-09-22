# Bot.py
import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

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
    if '!helpadmin' == message.content:
        await message.channel.send('Specific admin commands:'
                                   '- admin!users: Displays all users on server')
    if '!help' == message.content:
        await message.channel.send('List of commands:'
                                   '- !help: Displays help'
                                   '\n'
                                   'Memes:'
                                   '- !egal - Wendler'
                                   '- !mock - Mocks the last message'
                                   '\n'
                                   'Automatic functions:'
                                   '- Repeats \'f\', \'F\' and \':regional_indicator_f:\'')
    if 'admin!users' == message.content:
        channel = client.get_channel(755841743861317632)
        await channel.send(message.author.mention)
        members = '\n - '.join([member.name for member in guild.members])
        await channel.send('Guild Members:\n - ' + members)
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
    #if 'happy birthday' in message.content.lower():
    #    await message.channel.send('Happy Birthday! :partying_face:')
    # f-Bot
    if 'f' == message.content.lower() or '🇫' == message.content:
        await message.channel.send(message.content)

client.run(TOKEN)