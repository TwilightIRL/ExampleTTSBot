#wow commenting up here? smh. Comments that have an ! at the start are stuff that anyone setting this up will need to view (there should only be 2). The rest are just explanations of how this works for the curious
#also if you're looking for something else, go check out extra.py for some other unrelated stuff that you might wanna setup
import discord
import asyncio
from discord.ext import commands, tasks
import gtts
from gtts import gTTS
client = discord.Client()
bot = commands.Bot(command_prefix="/") #leaving the command_prefix blank will make the bot respond to any command that matches the context for the command.
#in other words commands like the first one would change from /enter to just enter. I added the / as a precaution, but you can remove it if you want.
from collections import deque
from tempfile import TemporaryFile
from discord import FFmpegPCMAudio

#this command joins the bot to the authors voice channel; it will also remove the message that called it for the purpose of keeping the channel clean
#the else statement is just to let you know if you try using it while the bot can't a vc to join. Commands like this usually only work if they're called in the server the voice chat is in
@bot.command()
async def enter(ctx):
    if ctx.author.voice:
        await ctx.channel.purge(limit=1)
        await ctx.message.author.voice.channel.connect()
    else:
        await ctx.send("You're either not in a voice channel right now, or in one I can't see")

#mostly the same stuff as the above command going on in here, except this time we make the voice channel a variable, wow. This serves little purpose in this command as we could do something similar to the above command
#but doing it this way helps set us up for the next command and understanding how that one works. Learning is fun! (also as a side you can just edit the ctx.send parts of these to change what the bot prints when those parts of the command are called or add your own)
@bot.command()
async def disconnect(ctx):
    await ctx.channel.purge(limit=1)
    vc = ctx.voice_client
    if not vc:
        await ctx.send("Oi, I'm not in a voice channel")
        return
    await vc.disconnect()
    await ctx.send("Bye Bye!")

#so this is the meat of this. so I'll be commenting in line to make it more clear which line I'm talking about, even though I usually avoid that
@bot.command()
async def tts(ctx):
    message_queue = deque([]) #this allows for a queue of messages later in the command
    message = ctx.message.content[4:] #if you change the context to call the command add or subtract from this the number of letters you changed. So if you made it a one letter command take 2 off
    message = message #this line makes sure that the many if/elses coming up have the same message in question
    try:
        vc = ctx.message.guild.voice_client #so all thats happening in the below if statement is the command calling the google text to speech library (gtts), using it to write a mp3, and using FFmpeg to play it
        if not vc.is_playing():
            tts = gtts(message)
            f = TemporaryFile()
            tts.write_to_fp(f)
            f.seek(0)
            vc.play(discord.FFmpegPCMAudio(f,executable="C:/FFmpeg/ffmpeg.exe", pipe=True)) #!You'll need to change the file path for your ffmpeg.exe for this to run properly. Unless its here for some reason
        else:
            message_queue.append(message)
            while vc.is_playing(): #mostly the same stuff from above is here, except this line and the one above. These add a message to the current queue and wait for the bot to finish talking.
                await asyncio.sleep(0.1)
            tts = gTTS(message_queue.popleft())
            f = TemporaryFile()
            tts.write_to_fp(f)
            f.seek(0)
            vc.play(discord.FFmpegPCMAudio(f,executable="C:/FFmpeg/ffmpeg.exe", pipe=True)) #!You'll need to change the file path for your ffmpeg.exe for this to run properly. Unless its here for some reason
    except(TypeError, AttributeError):
        try:
            tts = gTTS(message) # this section is in case of an error, the bot will still try and put the message out, the below one should only be raised if you're not in a vc, but it could also happen if the bot can't find ffmpeg
            f = TemporaryFile()
            tts.write_to_fp(f)
            f.seek(0)
            vc.play(discord.FFmpegPCMAudio(f,executable="C:/FFmpeg/ffmpeg.exe", pipe=True)) #!You'll need to change the file path for your ffmpeg.exe for this to run properly. Unless its here for some reason
        except(AttributeError, TypeError):
            await ctx.send("Smh, not even in a voice channel")
            return
        f.close()

id = open("id.txt", 'r') #!make sure you add your key to this! the text file is in the project directory
id = id.read()
bot.run(id)

