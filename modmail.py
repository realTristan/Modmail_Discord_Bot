from discord.ext import commands
from discord import utils
import discord
import asyncio
import datetime
import os,sys,re


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = "!", intents = intents)

@bot.event
async def on_ready():
	print(f" [!] Launched {bot.user.name}")







@bot.event
async def on_message(message):
    if message.content.startswith('!close'):
        if message.author.guild_permissions.manage_channels:
            if message.channel.category.name == 'modmail':
                if message.content[8:] == '' or message.content[8:] == ' ':
                    close_reason = "None Given"
                else:
                    close_reason = message.content[7:]


                topic = message.channel.topic
                if topic:
                    member = message.guild.get_member(int(topic))
                    if member:
                        embed = discord.Embed(title='ModMail Ticket Closed',description = f'`Reason: {close_reason}`', color=16711758)
                        embed.set_footer(icon_url= f'{message.author.avatar_url}', text=f'{message.author.name}')
                        embed.timestamp = datetime.datetime.utcnow()
                        await member.send(embed = embed)
                        
                await message.channel.delete(reason=message.content[7:])


            else:
                await message.delete()
                embed1 = discord.Embed(title='Wrong Channel!', description = 'Please use this command in the ModMail Category!', color=16711758)
                embed1.set_footer(icon_url= f'{message.author.avatar_url}', text=f'{message.author.name}')
                embed1.timestamp = datetime.datetime.utcnow()
                await message.channel.send(embed=embed1, delete_after=3)
        else:
            await message.delete()
            embed2 = discord.Embed(title='Access Denied', description = '`Required Permissions: Manage_Channels`', color=16711758)
            embed2.set_footer(icon_url= f'{message.author.avatar_url}', text=f'{message.author.name}')
            embed2.timestamp = datetime.datetime.utcnow()
            await message.channel.send(embed=embed2, delete_after=2)

    else:
        pass

    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel):
        guild = bot.get_guild(YOUR GUILD ID) # <==== USE (guild id) not ("guild id")
        categ = utils.get(guild.categories, name = "modmail")
        if not categ:
            overwrites = {
                guild.default_role : discord.PermissionOverwrite(read_messages = False),
                guild.me : discord.PermissionOverwrite(read_messages = True)
            }
            categ = await guild.create_category(name = "modmail", overwrites = overwrites)

        channel = utils.get(categ.channels, topic = str(message.author.id))

        if not channel:
            channel = await categ.create_text_channel(name = f"{message.author.name}#{message.author.discriminator}", topic = str(message.author.id))
            await channel.send("@here **//** `Type a Hidden Message by using !(message)`")
            

        embed3 = discord.Embed(description = message.content, color=16711758)
        embed3.set_author(name = message.author, icon_url = message.author.avatar_url)
        embed3.timestamp = datetime.datetime.utcnow()
        await channel.send(embed = embed3)

    elif isinstance(message.channel, discord.TextChannel):
        if message.content.startswith(bot.command_prefix):
            pass
        else:
            topic = message.channel.topic
            if topic:
                member = message.guild.get_member(int(topic))
                if member:
                    embed4 = discord.Embed(description = message.content, color=16711758)
                    embed4.set_author(name = message.author, icon_url = message.author.avatar_url)
                    embed4.timestamp = datetime.datetime.utcnow()
                    await member.send(embed = embed4)
    








bot.run("YOUR BOT TOKEN")



