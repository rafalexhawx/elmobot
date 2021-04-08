import discord, asyncio
from random import choice
import subprocess as sbp

client = discord.Client()
elmo = '745767772465922119'
token = "NzQ1NzY3NzcyNDY1OTIyMTE5.Xz2kXA.Xk1VrvJOQ2t8eE0OkAxucLxObmE"

global server

courses = {
    
}

courses = sorted(courses)

commands = {
    '!help': 'Shows all available commands',
    '!rename': 'Changes your nickname. Usage !rename {nickname you want}',
    '!rps': 'Play a game of rock paper scissors with Elmo. Usage !rps {rock, paper or scissors}'
}

def get_ip():
    a = sbp.run("hostname -I".split(' '), capture_output=True).stdout
    return a

def rps(user_choice, user_id):
    rps_choices = ['rock', 'paper', 'scissors']
    elmo_choice = choice(rps_choices)
    user_choice = user_choice[0].strip()
    user_designator = f"<@!{user_id}> "
    if elmo_choice == user_choice:
        return elmo_choice.upper() + " " + user_designator +  "There was a tie, you will live a day longer"
    else:
        if user_choice == 'rock':
            if elmo_choice == 'paper':
                return  elmo_choice.upper() + " " + user_designator + "I win, kiss your ass goodbye"
            else:
                return elmo_choice.upper() + " " + user_designator + "You win, Elmo is now your bitch"
        
        elif user_choice == 'paper':
            if elmo_choice == 'scissors':
                return elmo_choice.upper() + " " + user_designator + "I win, kiss your ass goodbye"
            else:
                return elmo_choice.upper() + " " + user_designator + "You win, Elmo is now your bitch"
        
        elif user_choice == 'scissors':
            if elmo_choice == 'rock':
                return elmo_choice.upper() + " " + user_designator + "I win, kiss your ass goodbye"
            else:
                return elmo_choice.upper() + " " + user_designator + "You win, Elmo is now your bitch"
        
        else:
            return user_designator + "It's rock paper scissors. The options are in the title. You're unworthy of Elmo"


    


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.get_channel(746146302546673706).send(f"Elmo's server is running on IP {get_ip()}")
    server = client.get_guild(745657520470753350)
    cat = discord.utils.get(server.categories, name='Course related issues')
    for i in courses:
        await client.get_channel(746056960125829292).send(i)
        perms = discord.Permissions(send_messages=True, read_messages=True, add_reactions=True, read_message_history=True, embed_links=True, attach_files=True)
        await server.create_role(name=i, permissions=perms)
        r = discord.utils.get(server.roles, name=i)
        await server.create_text_channel(name=i, category=cat, overwrites={
            server.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False),
            r: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
        })
        
        

    

    
        
    

greetings = ["You're in elmo's world now", "You'll never leave this place", "You belong to me now", "Part of the ship, part of the crew", "Great, another bitch", "Abandon all hope yee who enter here", "Welcome to the land below the living", "This, this right here is what hell looks like",  "It doesn't get lower than this",
"Yay, an actual decent hum... Nevermind"]

elmo_messages = open("phrases.txt", "r").readlines()

@client.event
async def on_member_join(member):
    await client.get_channel(745657520470753353).send(f"Welcome <@!{member.id}>. " + choice(greetings))

@client.event
async def on_raw_reaction_add(payload):
    print(payload)
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    server = client.get_guild(745657520470753350)
    user = payload.member
    print(channel.name, message.content, payload.emoji.name)
    if payload.emoji.name == 'pistol_pete' and channel.name == 'class-signup':
        for chnl in client.get_all_channels():
            if chnl.name == message.content:
                role = discord.utils.get(server.roles, name=message.content)
                await user.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    print(payload)
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    server = client.get_guild(745657520470753350)
    user = payload.member
    print(channel.name, message.content, payload.emoji.name)
    if payload.emoji.name == 'pistol_pete' and channel.name == 'class-signup':
        for chnl in client.get_all_channels():
            if chnl.name == message.content:
                role = discord.utils.get(server.roles, name=message.content)
                await user.remove_roles(role)

@client.event
async def on_message(message):
    contents = str(message.content)
    print(contents, message)
    command_intro = contents.split(' ')[0]
    command_contents = contents.split(' ')[1:]
    if message.author == client.user:
        return
    else:
        if elmo in contents or "Elmo#8786" in contents or "<@!Elmo>" in contents:
            text = f"<@!{message.author.id}> Leave Elmo alone. I'm your secretary, not your mom so go make your own god damn sandwich!"
            print(f"Sent message ({text}) to user {message.author.name}")
            await message.channel.send(text)
        
        elif 'elmo' in contents.lower() and message.author.name != 'Elmo':
            await message.channel.send(f"{choice(elmo_messages)}", tts=False)

        elif command_intro == '!rename':
            member = message.author
            nickname = ' '.join(command_contents)
            await member.edit(nick=nickname)
            await message.channel.send(f"<@!{member.id}> Your new nickname is {nickname}")
        
        elif command_intro == '!help':
            for command in commands.keys():
                await message.channel.send(f"{command} -> {commands[command]}")
            
        elif command_intro == "!rps":
            await message.channel.send(rps(command_contents, message.author.id))
        
        elif command_intro == "!sandwich":
            
            if message.author.nick != None:
                await message.author.edit(nick=f"🍞{message.author.nick}🍞")
                await message.channel.send(f"{message.author.nick} Elmo made you a sandwich")
            else:
                await message.author.edit(nick=f"🍞{message.author.name}🍞")
                await message.channel.send(f"{message.author.name} Elmo made you a sandwich")
            server = client.get_guild(745657520470753350)
            role = discord.utils.get(server.roles, name='Sandwich')
            await message.author.add_roles(role)
            
            

        
        

            
    print("Done with management of input")


client.run(token)

