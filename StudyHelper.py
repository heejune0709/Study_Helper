import discord, asyncio, os
from discord.ext import commands
import datetime
import re
from collections import OrderedDict
import time
import random
import youtube_dl
saved_h = {}
saved_hw = {}
game = discord.Game("Studying")
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!',status = discord.Status.online, activity = game, intents = intents)
vocab = {}
players={}
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume = 0.5):
        super().__init__(source,volume)
        self.data=data
        self.title=data.get('title')
        self.url=''
    @classmethod
    async def from_url(cls, url, *, loop = None, stream = False):
        loop=loop or asyncio.get_event_loop()
        data= await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download= not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['title'] if  stream else ytdl.prepare_filename(data)
        return filename
@client.command()
async def hi(ctx):
    await ctx.send("Hello, I am HWdue bot")
@client.command()
async def bye(ctx):
    await ctx.send("See you")
@client.command(pass_context=True)
async def join(ctx):
    channel=ctx.message.author.voice.channel
    await channel.connect()
@client.command(pass_context=True)
async def leave(ctx):
    voice_client=ctx.message.guild.voice_client
    await voice_client.disconnect()
@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.guild
    voice_channel = server.voice_client
    if voice_channel is None:
        voice_channel = await ctx.author.voice.channel.connect()
    try:
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=client.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="/usr/local/bin/ffmpeg", source=filename))
    except Exception as e:
        print(f"An error occurred: {e}")


@client.listen('on_message')
async def hw_save(message):
    if message.content.startswith("savehw"):
        parts = message.content.split('/', maxsplit=1)
        print(parts[0].split(' ', maxsplit=1)[1])
        hw = parts[0].split(' ', maxsplit=1)[1]
        due = parts[1].strip() if len(parts) > 1 else ""
        print(hw)
        if not re.match(r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}", due):
            await message.channel.send('Wrong format. Type in !hw Homework/`YYYY-MM-DD HH:MM`.')
            return
        saved_hw[hw] = datetime.datetime.strptime(due, '%Y-%m-%d %H:%M')
        saved_hw_sorted = OrderedDict(sorted(saved_hw.items(), key=lambda x: x[1]))
        saved_hw.clear()
        saved_hw.update(saved_hw_sorted)
        print(datetime.datetime.strptime(due, '%Y-%m-%d %H:%M'))
        print(saved_hw.keys())
        print(saved_hw.values())
        await message.channel.send(f"You have {hw} until {due}")
    if message.content.startswith("deletehw"):
        _, check = message.content.split()
        if check in saved_hw:
            del saved_hw[check]
            await message.channel.send(f"{check} has been deleted from the list.")
        else:
            await message.channel.send(f"{check} is not in the list.")

    if message.content.startswith("resethw"):
        saved_hw.clear()
        await message.channel.send("The list has been reset.")

@client.listen('on_message')
async def due_calc_1(message):
    if message.content.startswith("todayhw"):
        now = datetime.datetime.now()
        #check = now.replace(hour = 23, minute = 2)
        #then = now + datetime.timedelta(days=1)
        #wait = (check-now).total_seconds()
        #wait = (then - now).total_seconds()
        print("works")
        for hw1, due1 in saved_hw.items():
            if now.date() == due1.date():
                print("check!")
                await message.channel.send(f"You have {hw1} until {due1}")

@client.listen('on_message')
async def due_calc_2(message):
    if message.content.startswith("weeklyhw"):
        now = datetime.datetime.now()
        #check = now.replace(hour = 23, minute = 2)
        #then = now + datetime.timedelta(days=1)
        #wait = (check-now).total_seconds()
        #wait = (then - now).total_seconds()
        print("works")
        for hw1, due1 in saved_hw.items():
            delta = due1 - now
            if delta.days >= 0 and delta.days <= 7:
                print("check!")
                await message.channel.send(f"You have {hw1} due on {due1.strftime('%A, %B %d')}")

@client.listen('on_message')
async def on_message(message):
    if message.content.startswith('startstopwatch'):
        start_time = time.time() # Record the starting time of the stopwatch
        await message.channel.send("Stopwatch started. Type `!stop` to stop.") # Send a message indicating that the stopwatch has started

        # Keep the stopwatch running until the user types "!stop"
        while True:
            try:
                msg = await client.wait_for('message', timeout=1.0) # Wait for a message from the user
                if msg.content == 'stopstopwatch':
                    end_time = time.time() # Record the ending time of the stopwatch
                    elapsed_time = round(end_time - start_time, 2) # Calculate the elapsed time in seconds
                    await message.channel.send(f"Stopwatch stopped. Elapsed time: {elapsed_time} seconds.") # Send a message with the elapsed time
                    break # Exit the loop and stop the stopwatch
                else:
                    current_time = time.time() - start_time # Calculate the current elapsed time
                    current_time_formatted = time.strftime("%H:%M:%S", time.gmtime(current_time)) # Format the current time as hours, minutes, and seconds
                    await message.channel.send(f"Elapsed time: {current_time_formatted}") # Send a message with the current elapsed time
            except asyncio.TimeoutError: # If no message is received for 1 second, continue the loop
                continue

@client.listen('on_message')
async def quiz(message):
    if message.author == client.user:
        return
    if message.content.startswith("addword"):
        _, word, meaning = message.content.split()
        vocab[word] = meaning
        await message.channel.send(f"{word} added.")

    if message.content.startswith("deleteword"):
        _, word = message.content.split()
        if word in vocab:
            del vocab[word]
            await message.channel.send(f"{word} deleted.")
        else:
            await message.channel.send(f"{word} does not exist.")

    if message.content.startswith("resetword"):
        vocab.clear()
        await message.channel.send("Vocab Reseted.")
    if message.content.startswith("wordquiz"):
        if not vocab:
            await message.channel.send("Save your words to start quiz.")
            return
        words = list(vocab.keys())
        random.shuffle(words)
        for word in words:
            meaning = vocab[word]

            await message.channel.send(f"{meaning}?")

            def check(m):
                return m.author == message.author and m.channel == message.channel

            try:
                response = await client.wait_for("message", check=check, timeout=10.0)
            except asyncio.TimeoutError:
                await message.channel.send(f"Time up! Answer:{word}")
            else:
                if response.content.lower() == word.lower():
                    await message.channel.send("Bingo!")
                else:
                    await message.channel.send(f"Wrong! Answer:{word}")
#trying to play youtube link
#succeed to make bot join voice chat
#but not playing anything yet


@client.event
async def on_ready():
    print("You can now use your bot")
#testtesttest
client.run('MTA4MTA3OTYzMDYzMjU4NzMwNA.GXY-RO.1TE3a_pqwexb3qjK0VwIh-GDp98dLMW8fMXNL8')







