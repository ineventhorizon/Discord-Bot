import discord
import youtube_dl
import os
from discord.utils import get
from discord.ext import commands

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():

    await client.change_presence(status=discord.Status.online,activity=discord.Game('local ımyeh'))
    print('We have logged in as  {0.user}'.format(client))

@client.command(aliases=['ping','latency'])
async def sasa(ctx):
    await ctx.send(f'asas {round(client.latency*1000)}ms')

@client.command()
async def join(ctx):
    if not discord.opus.is_loaded():
        # the 'opus' library here is opus.dll on windows
        # or libopus.so on linux in the current directory
        # you should replace this with the location the
        # opus library is located in and with the proper filename.
        # note that on windows this DLL is automatically provided for you
        discord.opus.load_opus('opus')
    author = ctx.message.author
    channel = author.voice.channel
    vc = get(client.voice_clients, guild=ctx.guild)

    if vc and vc.is_connected():
        await vc.move_to(channel)
        print(f'moved to {channel}')
    else:
        vc = await channel.connect()
        print(f'connected to {channel}')




@client.command()
async def test(ctx):
    vc = get(client.voice_clients)
    ch1 = get(client.get_all_channels(),name='youtube')

    print(vc)

    await ch1.send('test')




@client.command()
async def leave(ctx):

    if not discord.opus.is_loaded():
        # the 'opus' library here is opus.dll on windows
        # or libopus.so on linux in the current directory
        # you should replace this with the location the
        # opus library is located in and with the proper filename.
        # note that on windows this DLL is automatically provided for you
        discord.opus.load_opus('opus')

    author = ctx.message.author
    channel = author.voice.channel
    vc = get(client.voice_clients, guild=ctx.guild)

    if not vc:
        print('bot is not in a channel')
        await ctx.send('Not in a channel!')
    else:
        await vc.disconnect()
        print(f'disconnected from {channel}')

@client.command()
async def play(ctx, url):
    if not discord.opus.is_loaded():
        # the 'opus' library here is opus.dll on windows
        # or libopus.so on linux in the current directory
        # you should replace this with the location the
        # opus library is located in and with the proper filename.
        # note that on windows this DLL is automatically provided for you
        discord.opus.load_opus('opus')

    responseCh = get(client.get_all_channels(), name='youtube', guild=ctx.guild)
    author = ctx.message.author
    channel = author.voice.channel
    svName = ctx.guild


    vc = get(client.voice_clients, guild=ctx.guild)

    if vc and vc.is_connected():
        await vc.move_to(channel)
        print(f'moved to {channel}')
        if vc.is_playing():
            print('already playing another audio')
    else:
        vc = await channel.connect()
        print(f'connected to {channel}')
        is_song_there = os.path.isfile(f'{svName}.mp3')
        try:
            if is_song_there:
                os.remove(f'{svName}.mp3')
                print("Removed the old song file")
        except PermissionError:
            print('Currently it is being played, can not remove!')
            await responseCh.send('Another song is playing.')
            return

        print('Getting ready!')
        await responseCh.send(f'Getting ready to play: {url}')

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
            'outtmpl':'%(id)s.%(ext)s'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        y_id = ydl.extract_info(url).get('id')
        print(id)

        for file in os.listdir('./'):
            if file.endswith('.mp3') and file.startswith(f'{y_id}'):
                print(f'Renaming {file}')
                os.rename(file, f'{svName}.mp3')

        print(f'Now playing: {url} ')
        await responseCh.send(f'Now playing: {url}')

        vc.play(discord.FFmpegPCMAudio(f'{svName}.mp3'), after=lambda e:print('done', e))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 0.07






client.run('')

