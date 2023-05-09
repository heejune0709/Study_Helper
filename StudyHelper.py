#MTA4MTA3OTYzMDYzMjU4NzMwNA.GXY-RO.1TE3a_pqwexb3qjK0VwIh-GDp98dLMW8fMXNL8
import discord, asyncio, os 
from discord.ext.commands import Bot
from discord.ext import commands
import datetime
from datetime import datetime, timedelta
import random
import re
import emoji
import re
from collections import OrderedDict
import time
import random
import requests
import youtube_dl
import math
TOKEN = 'MTA4MTA3OTYzMDYzMjU4NzMwNA.GXY-RO.1TE3a_pqwexb3qjK0VwIh-GDp98dLMW8fMXNL8'

intents = discord.Intents.all()
game = discord.Game("Let's help")

bot = commands.Bot(command_prefix='?', status=discord.Status.online, activity=game, intents=intents)

#examreminder
#input: examsave cal3/2023-04-14 15:03/cbtf
#output: You have cal3 exam on cbtf at 2023-04-14 15:03
#output: Less than one hour left before your cal3 exam on cbtf!
#////////////////////////////////////////////////////////////////////////////////////////////
exam_list = {}
@bot.listen('on_message')
async def examsave(ctx):
    if ctx.content.startswith("exam"):
        parts = ctx.content.split('/', maxsplit=2)
        #print(parts[0].split(' ', maxsplit=1)[1])
        exam = parts[0].split(' ', maxsplit=1)[1]
        due = parts[1].strip() if len(parts) > 1 else ""
        place = parts[2].strip() if len(parts) > 2 else ""
        print(exam)
        print(due)
        print(place)
        if not re.match(r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}", due):
            await ctx.channel.send('Wrong format. Type in !exam Exam/`YYYY-MM-DD HH:MM`/place.')
            return
        exam_list[exam] = {'due_date': datetime.strptime(due, '%Y-%m-%d %H:%M'), 'place': place}
        await ctx.channel.send(f"You have {exam} exam on {place} at {due}")
        now=datetime.now()
        then=datetime.strptime(due, '%Y-%m-%d %H:%M')
        oneh_before=int(then.hour-(timedelta(hours=1, minutes=0, seconds=0)/timedelta(hours=1)))
        newthen=then.replace(hour=oneh_before)
        wait_time=(newthen-now).total_seconds()
        print(newthen)
        print(now)
        print(oneh_before)
        print(wait_time)
        await asyncio.sleep(wait_time)
        
        await ctx.channel.send(f'Less than one hour left before your {exam} exam on {place}!')
        
#print the exam list
@bot.command()
async def myexams(ctx):
    await ctx.send(exam_list)
#list become empty again when the bot become offline
#start again when the bot is online

#testing if this logic works
@bot.command()
async def schedule_message(ctx):
    now=datetime.datetime.now()
    then=now.replace(hour=22, minute=53)
    wait_time=(then-now).total_seconds()
    await asyncio.sleep(wait_time)

    await ctx.send("Good morning!!")
#////////////////////////////////////////////////////////////////////////////////////////////
#examreminder


#studyTimer
#input: studytimer 0:10 #minute:second
#output: Your timer is set to 0minutes 10seconds from now!
#output: Time is over!!!

#////////////////////////////////////////////////////////////////////////////////////////////
@bot.listen('on_message')
async def studytimer(message):
    #channel = ctx.channel
    if message.content.startswith("studytimer"):
        #await message.channel.send('Please write how many minutes you want to set the timer. (In minutes!!)')
        #mins = message.content
        parts = message.content.split(':', maxsplit=1)
        mins = parts[0].split(' ', maxsplit=1)[1]
        secs = parts[1].strip() if len(parts) > 1 else ""

        await message.channel.send(f"Your timer is set to {mins}minutes {secs}seconds from now!")
        mins=int(mins)
        secs=int(secs)
        
        mins=mins*60
        await asyncio.sleep(mins+secs)

        await message.channel.send("Time is over!!!")
#////////////////////////////////////////////////////////////////////////////////////////////
#studyTimer


#toDoList
#input: todo hwname/YYYY-MM-DD HH:MM
#output: You have math421hw9 due to 2023-03-30 23:59.

#input: ?mylist
#output: Your list:
#math421hw9 2023-03-30 23:59
#cs233lab9 2023-03-30 23:59

#input: check math421hw9
#output: Your list:
#👍 math421hw9 2023-03-30 23:59
#cs233lab9 2023-03-30 23:59

#input: remove math421hw9
#output: Your list:
#cs233lab9 2023-03-30 23:59
#////////////////////////////////////////////////////////////////////////////////////////////
todo_list={}
#save the name of task and due date into todo_list
#type: ?todo task/YYYY-MM-DD HH:MM
@bot.listen('on_message')
async def todosave(ctx):
    if ctx.content.startswith("todo"):
        parts = ctx.content.split('/', maxsplit=1)
        task = parts[0].split(' ', maxsplit=1)[1]
        due = parts[1].strip() if len(parts) > 1 else ""
        print(task)
        print(due)
        if not re.match(r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}", due):
            await ctx.channel.send('Wrong format. Type in ?todo task/`YYYY-MM-DD HH:MM`')
            return
        todo_list[task] = due
        await ctx.channel.send(f"You have {task} due to {due}.")
             
#print the todo_list
# type: ?mylist
@bot.command()
async def mylist(ctx):
    list_print="Your list:\n"
    for key in todo_list:
        list_print+=key+" "
        list_print+=todo_list[key]+"\n"
    await ctx.send(list_print)

#add thumbs_up emoji in front of the task done
#type: check taskname
@bot.listen('on_message')
async def todoremove(ctx):
    if ctx.content.startswith("check"):
        parts = ctx.content.split('/', maxsplit=0)
        task = parts[0].split(' ', maxsplit=1)[1]
        list_print="Your list:\n"
        for key in todo_list:
            if key==task:
                list_print+=emoji.emojize(':thumbs_up:')+" "
            list_print+=key+" "
            list_print+=todo_list[key]+"\n"
        await ctx.channel.send(list_print)

#remove the task from the list
# type: remove taskname
@bot.listen('on_message')
async def todoremove(ctx):
    if ctx.content.startswith("remove"):
        parts = ctx.content.split('/', maxsplit=0)
        task = parts[0].split(' ', maxsplit=1)[1]
        todo_list.pop(task, -1)
        list_print="Your list:\n"
        for key in todo_list:
            list_print+=key+" "
            list_print+=todo_list[key]+"\n"
        await ctx.channel.send(list_print)
#////////////////////////////////////////////////////////////////////////////////////////////
#toDoList

api_key = 'aac486d22a195ee88dc4698525927457'
lat =   40.116
lon =  -88.243

saved_h = {}
saved_hw = {}

vocab = {}

#hwdue
#input: savehw hwname/YYYY-MM-DD HH:MM
#output: You have CS225 MP3 until 2023-03-18 23:59

#////////////////////////////////////////////////////////////////////////////////////////////
@bot.listen('on_message')
async def hw_save(message):
    if message.content.startswith("savehw"):
        parts = message.content.split('/', maxsplit=1)
        print(parts[0].split(' ', maxsplit=1)[1])
        hw = parts[0].split(' ', maxsplit=1)[1]
        due = parts[1].strip() if len(parts) > 1 else ""
        print(hw)
        if not re.match(r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}", due):
            await message.channel.send('Wrong format. Type in savehw Homework/`YYYY-MM-DD HH:MM`.')
            return
        saved_hw[hw] = datetime.strptime(due, '%Y-%m-%d %H:%M')
        saved_hw_sorted = OrderedDict(sorted(saved_hw.items(), key=lambda x: x[1]))
        saved_hw.clear()
        saved_hw.update(saved_hw_sorted)
        print(datetime.strptime(due, '%Y-%m-%d %H:%M'))
        print(saved_hw.keys())
        print(saved_hw.values())
        await message.channel.send(f"You have {hw} until {due}")
        
@bot.listen('on_message')
async def due_calc_1(message):
    if message.content.startswith("todayhw"):
        now = datetime.now()
        #check = now.replace(hour = 23, minute = 2)
        #then = now + datetime.timedelta(days=1)
        #wait = (check-now).total_seconds()
        #wait = (then - now).total_seconds()
        print("works")
        for hw1, due1 in saved_hw.items():
            if now.date() == due1.date():
                print("check!")
                await message.channel.send(f"You have {hw1} until {due1}")

@bot.listen('on_message')
async def due_calc_2(message):
    if message.content.startswith("weeklyhw"):
        now = datetime.now()
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
#////////////////////////////////////////////////////////////////////////////////////////////
#hwdue

#stopwatch
#input: stopwatch
#output: Stopwatch started. Type !stop to stop.

#input: !stop
#output: Stopwatch stopped. Elapsed time: 4.07 seconds.
#////////////////////////////////////////////////////////////////////////////////////////////
@bot.listen('on_message')
async def on_message(message):
    if message.content.startswith('stopwatch'):
        start_time = time.time() # Record the starting time of the stopwatch
        await message.channel.send("Stopwatch started. Type `!stop` to stop.") # Send a message indicating that the stopwatch has started

        # Keep the stopwatch running until the user types "!stop"
        while True:
            try:
                msg = await bot.wait_for('message', timeout=1.0) # Wait for a message from the user
                if msg.content == '!stop':
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
#////////////////////////////////////////////////////////////////////////////////////////////
#stopwatch

#quiz
#input: addword apple 사과
#output: apple added.

#input: wordquiz
#output: 사과?
#input_case1: apple
#output_case1: Bingo!
#input_case2: mango
#output_case2: Wrong! Answer:apple

#input: deleteword apple
#output: apple deleted.
#////////////////////////////////////////////////////////////////////////////////////////////
@bot.listen('on_message')
async def quiz(message):
    if message.author == bot.user:
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
                response = await bot.wait_for("message", check=check, timeout=10.0)
            except asyncio.TimeoutError:
                await message.channel.send(f"Time up! Answer:{word}")
            else:
                if response.content.lower() == word.lower():
                    await message.channel.send("Bingo!")
                else:
                    await message.channel.send(f"Wrong! Answer:{word}")
#////////////////////////////////////////////////////////////////////////////////////////////
#quiz

#weather
#input: weather
#output: Today, it is 46.7 degrees fahrenheit, 26.5 in Celcius
#////////////////////////////////////////////////////////////////////////////////////////////
@bot.listen('on_message')
async def weather(message):
    if message.content.startswith('weather'):
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}')
        # print(response.json())
        temperature = response.json()['main']['temp']
        
        # weather_des = response.json()['weather']['description']
        # wind = response.json()['wind']['speed']
 
        await message.channel.send(f'Today, it is {round((temperature - 273.15) * 5/9 + 32, 1)} degrees fahrenheit, {round(temperature - 273.15, 1)} in Celcius')
        # await message.channel.send('Weather: ' + weather_des + '/ Wind speed: ' + wind + 'm/s')
#////////////////////////////////////////////////////////////////////////////////////////////
#weather



#calculator
#///////////////////////////////////////////////////////////////////////////////////////////

@bot.listen('on_message')
async def calculator(message):
    #channel = ctx.channel
    if message.content.startswith("math"):
        parts = message.content.split()
        print(parts)
        first = parts[1].strip() if len(parts) > 1 else ""
        operator = parts[2].strip() if len(parts) > 2 else ""
        second = parts[3].strip() if len(parts) > 3 else ""

        first=int(first)
        second=int(second)

        if operator=='+':
            await message.channel.send(first+second)
        elif operator=='-':
            await message.channel.send(first-second)
        elif operator=='*':
            await message.channel.send(first*second)
        elif operator=='/':
            await message.channel.send(first/second)
        elif operator=='^' or operator=='**':
            await message.channel.send(first**second)
        elif operator=='%':
            await message.channel.send(first%second)
        else:
            await message.channel.send("You can only use +,-,*,/,^,%. Please try again with format math 1 + 2")

    elif message.content.startswith("trig"):
        parts = message.content.split()
        print(parts)
        operator = parts[1].strip() if len(parts) > 1 else ""
        num = parts[2].strip() if len(parts) > 2 else ""
        num=float(num)
        if operator=='sin':
            await message.channel.send(math.sin(num))
        elif operator=='cos':
            await message.channel.send(math.cos(num))
        elif operator=='tan':
            await message.channel.send(math.tan(num))
        else:
            await message.channel.send("You can only use cos, sin, tan. Please try again with format trig cos 3.14")
#//////////////////////////////////////////////////////////////////////////////////////////
#calculator

#youtube
#/////////////////////////////////////////////////////////////////////////////////////////////////////
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

@bot.command(pass_context=True)
async def join(ctx):
    channel=ctx.message.author.voice.channel
    await channel.connect()
@bot.command(pass_context=True)
async def leave(ctx):
    voice_client=ctx.message.guild.voice_client
    await voice_client.disconnect()
@bot.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.guild
    voice_channel = server.voice_client
    if voice_channel is None:
        voice_channel = await ctx.author.voice.channel.connect()
    try:
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="/usr/local/bin/ffmpeg", source=filename))
    except Exception as e:
        print(f"An error occurred: {e}")
    

#////////////////////////////////////////////////////////////////////////////////////////
#youtube


@bot.event
async def on_ready():
    print("You can now use your bot")


bot.run(TOKEN)
