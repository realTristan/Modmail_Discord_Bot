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
    await bot.change_presence(activity=discord.Game(name="DM for Support"))
    print(f" [!] Launched {bot.user}")







@bot.event
async def on_message(message):
    await bot.process_commands(message)

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
                        embed.set_footer(icon_url= f'{message.author.avatar_url}', text=f'{message.author}')
                        embed.timestamp = datetime.datetime.utcnow()
                        await member.send(embed = embed)
                        
                await message.channel.delete(reason=message.content[7:])


            else:
                await message.delete()
                embed1 = discord.Embed(title='Wrong Channel!', description = '`Please use this Command in the ModMail Category!`', color=16711758)
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
        guild = bot.get_guild(YOUR GUILD ID)
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
    



@bot.command()
@commands.has_permissions(manage_channels=True)
async def add(ctx, *args):
    await ctx.message.delete()
    format_args = list(args)

    user1 = format_args[0].strip('>').strip('<').strip('@').replace('!','')
    user2 = ctx.guild.get_member(int(user1))

    await ctx.channel.set_permissions(user2, view_channel=True, send_messages=True)
    await ctx.send(f'{ctx.author.mention} added {user2.mention} to the ticket!')
    topic = ctx.channel.topic
    if topic:
        member = ctx.guild.get_member(int(topic))
        if member:
            embed = discord.Embed(title='Added User to Ticket',description = f'{ctx.author.mention} added {user2.mention} to the ticket!', color=16711758)
            embed.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author}')
            embed.timestamp = datetime.datetime.utcnow()
            await member.send(embed = embed)




































bot.run("YOUR BOT TOKEN")



