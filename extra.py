#ok so a bunch of stuff will be missing from this file like the bot run stuff as I'm intending for this to a resource, not something you actually run. If you want these exact commands you'll need their libraries and such
@bot.command() #alright starting kinda basic here, this is just a command showing how to play an mp3. The files in question are not here to keep the release lightweight so sub in your own.
async def vb(ctx):
    source = FFmpegPCMAudio('vb.mp3', executable="C:/FFmpeg/ffmpeg.exe") #the way I call the mp3 here implies that its already in the projects folder, if its not give it a file path
    vc = ctx.message.guild.voice_client
    while vc.is_playing():
        await asyncio.sleep(0.1)
    vc.play(source)

@bot.command() #using ctx again but this time to make a random choice. You'll need to import random for this one.
#You could also add lines to prevent choices like the word "or" but I didn't include those for the sake of usability. If you want help setting that up dm on my discord (TwilightSparkle#0001 at the time of writing)
async def choose(ctx, *choices: str):
    await ctx.send(random.choice(choices))
    await ctx.send("Obviously")

@bot.command() #this just shows how to use the ability to mention an author. This was added very early in my bot as a test
async def ping(ctx):
        msg = "pong. {0.author.mention}".format(ctx.message)
        await ctx.send(msg)

@bot.event
async def on_ready():
    await bot.wait_until_ready() #you'll need this event for the below one to work
    changestatus.start()

@tasks.loop(seconds=1800) # this is one of my favorites. this will change what your bot displays as its status. change the range as you add more. The seconds also add to 30 minutes but you can make that whatever (just don't make it too low, discord gets angry if you do :( )
#also if you want the bot to change YOUR status, dm for that, it's a bit more complex and requires more libraries that are kinda outdated and funky to work with, but I am happy to explain! just not here because it's long
async def changestatus():
    global x

    status = iter(
        [
            "Cookies and Cream",
            "watching my little pony",
            "d&d",
        ]
    )
    for x in range(random.randint(1, 3)):
        x = next(status)
    await bot.change_presence(activity=discord.Game(name=x))

@bot.command() #so this ones a bit more complex in purpose. The point of it is to store a variable that the ctx counts in case this bot doesn't have full uptime. I have no idea what *you* would use this for.
#you could use to count how many times a user sends a message using if statements, or count up to something funny happening, whatever. it's in your hands now
async def counting(ctx): #also I don't use pickle here because I don't really like pickle, sorry. If you wanted a working version of this with pickle one exists, but I'm assuming if you know what I'm on about then you know how to use pickle
    counter = open("test.txt", "r")
    storedcount = int(counter.readline())
    storedcount += 1
    counter = open("test.txt", "w")
    counter.write(str(storedcount) + "\n")
    ctx.send(counter)
    counter.close()
#so to avoid commands that are pointless heres some stuff so you don't have to read the discord.py docs (they suck)
#ctx.author.id can be used to change how a command responds depending on the author. like " if ctx.author.id == 12345" could be used to make a command only work for that id
#in a similar vein as above ctx.channel.id can be used to check channel ids, ctx.message.guild checks the server (or if the ctx even is a server), ctx.message.content checks the actual message
#you can also weave changes in status very easily into other commands such as adding the line "await bot.change_presence(activity=discord.Game(name="heartbroken </3"))" to an existing command
#I assume this is enough to get you started if you wanted more than tts, but if its not then just lmk, I read the discord docs so you don't have to