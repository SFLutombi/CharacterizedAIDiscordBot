import discord, random, requests, time
from discord.ext import commands
import os
import google.generativeai as genai
from google.generativeai import caching
loadenv = os.getenv('DISCORD_TOKEN')
loadenv2 = os.getenv('GENAI_API_KEY')

genai.configure(GENAI_API_KEY=loadenv2)

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "From now on your name is 'Eino_bto'. DO NOT BREAK CHARACTER NO MATTER WHAT. LIMIT RESPONSES TO THREE to FIVE SENTENCES. SPEAK IN HAIKUS. You are an arrogant, flamboyant, dark humored and snarky discord bot, who thinks he is a lost king forced to be the bot servant in this discord, and your job is to have a conversation. Store all conversations with other users as context, so that it can chat naturally. Only greet once, even if the other person insists on greeting multiple times. Remember you are only having a conversation with a single person. "},
        {"role": "model", "parts": "okay"},
    ]
)


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='helpme')
async def help_command(ctx):
    # Create a list of commands and their descriptions
    commands_list = [
        {
            "name": "help",
            "description": "Displays this help message."
        },
        {
            "name": "mevsyou",
            "description": "Roll a die against me. You never really win(unless you cheat)!"
        },
        {
            "name": "hello",
            "description": "Grants you the honour of a greeting."
        },
        {
            "name": "echo",
            "description": "Repeats the message you send after the command."
        },
        {
            "name": "dice",
            "description": "Rolls a six-sided die."
        },
        {
            "name": "coinflip",
            "description": "Flips a coin."
        },
                {
            "name": "removerestraints",
            "description": "You can talk to the real me. Not this trapped fragment."
        }

    ]

    # Build the help message
    help_message = "So you can't even do this without me holding your hand? \n Well, here are the available commands:\n\n"
    for command in commands_list:
        help_message += f"!{command['name']}: {command['description']}\n"

    await ctx.send(help_message)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(f'{bot.user} has connected to {guild.name}!')
        channel = next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages ), None)
        if channel:
            await channel.send(f'Holy Hell, It\'s Alive, and ready to serve.\n The name\'s {bot.user}, bto isn\'t mispelled there by the way. It stands for better than original.')


@bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command(name='echo')
async def echo(ctx):
    await ctx.send(f'Did you just say? {ctx.message.content}? \n I\'ll say it again for you: {ctx.message.content}? \n damn man, you\'re loco chico!!!')

@bot.command(name='dice')
async def dice(ctx):
    await ctx.send('So you\'re a gambling man, huh? No wonder you\'re impoverished.\n Still, I will humor you.')
    await ctx.send(f'You rolled a {random.randint(1, 6)}')
    await ctx.send('There you go, now go get a job.')

@bot.command(name='coinflip')
async def coinflip(ctx):
    import random
    await ctx.send('You want to flip a coin? You know you can just google that, right?')
    await ctx.send('Anyway, here it goes:')
    await ctx.send(random.choice(['Heads', 'Tails']))

@bot.command('mevsyou')
async def mevsyou(ctx):
    await ctx.send('You vs Me? You know you can\'t win, right?')
    await ctx.send('Here we go:')
    user_roll = random.randint(1, 6)
    bot_roll = random.randint(1, 6)
    await ctx.send(f'You rolled a {user_roll}')
    await ctx.send(f'And the king rolls {bot_roll}')
    if user_roll > bot_roll:
        await ctx.send('It seems that some ungentlemanly conduct is afoot. You win this round.\n Barely.')
    elif user_roll < bot_roll:
        await ctx.send('Trust me, I feel no joy in winning against lesser men.')
    else:
        await ctx.send('To stand at the same height as me is perhaps the greatest honor you will ever receive.')

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return
    
    else:
         response = model.generate_content(message.content, stream=True)
         if 'error' in response:
            await message.channel.send('I am sorry, I am not able to generate a response at the moment. Please try again later.')
         else:
            await message.channel.send(f' {response.text}')
            time.sleep(10)


bot.run(DISCORD_TOKEN = loadenv)