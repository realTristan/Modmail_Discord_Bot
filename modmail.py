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





empty_arr = []


@bot.event
async def get_reacts(user, client, message, emojis, timeout=None):
    for emoji in emojis:
        await message.add_reaction(emoji)
    try:
        def check(reaction, reactor):
            return reactor.id == user.id and reaction.emoji in emojis
        reaction, user = await client.wait_for("reaction_add", check=check, timeout=timeout)
        return reaction.emoji
    except:
        pass




@bot.event
async def on_message(message):
    await bot.process_commands(message)
            
    if message.author.bot:
        return



    if isinstance(message.channel, discord.DMChannel):
        guild_list = []
        ab=0

        guild_dict = {
                
        }


        emoji_dict = {
            
        }

        react_dict = {

        }

        emoji_dict[f"1"] = "1️⃣"
        emoji_dict[f"2"] = "2️⃣"
        emoji_dict[f"3"] = "3️⃣"
        emoji_dict[f"4"] = "4️⃣"
        emoji_dict[f"5"] = "5️⃣"

        react_dict[f"1️⃣"] = 1
        react_dict[f"2️⃣"] = 2
        react_dict[f"3️⃣"] = 3
        react_dict[f"4️⃣"] = 4
        react_dict[f"5️⃣"] = 5





        embed_select= discord.Embed(title='Select Server to send message to')


        for guild_check in bot.guilds:
            ab +=1
            guild_dict[f"{ab}"] = f"{guild_check.id}"
            
            emoji= emoji_dict[f"{ab}"]

            embed_select.add_field(name=f'React with {emoji}', value=guild_check.name)



        msg = await message.author.send(embed=embed_select)
        reaction = await get_reacts(message.author, bot, msg, ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣"])
        main_react = react_dict[f"{reaction}"]
        guild = bot.get_guild(int(guild_dict[f"{main_react}"]))
       

        categ = utils.get(guild.categories, name = "modmail")
        if not categ:
            overwrites = {
                guild.default_role : discord.PermissionOverwrite(read_messages = False),
                guild.me : discord.PermissionOverwrite(read_messages = True)
            }
            categ = await guild.create_category(name = "modmail", overwrites = overwrites)

        channel = utils.get(categ.channels, topic = str(message.author.id))

        if not channel:
            channel = await categ.create_text_channel(name = f"{message.author}", topic = str(message.author.id))
            await channel.send("@here **//** `Type a Hidden Message by using !(message)`")
            
        if message.attachments != empty_arr:
            files = message.attachments

            for file in files:
                embed33 = discord.Embed(title='Message Recieved', description=message.content, color=16711758)
                embed33.set_thumbnail(url=file.url)
                embed33.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
                embed33.timestamp = datetime.datetime.utcnow()
                await channel.send(embed=embed33)
        else:
            embed3 = discord.Embed(title='Message Recieved',description = message.content, color=16711758)
            embed3.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
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
                    if message.attachments != empty_arr:
                        files = message.attachments

                        for file in files:
                            embed44 = discord.Embed(title='Message Recieved', description=message.content, color=16711758)
                            embed44.set_thumbnail(url=file.url)
                            embed44.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
                            embed44.timestamp = datetime.datetime.utcnow()
                            await member.send(embed=embed44)
                    else:
                        embed4 = discord.Embed(title='Message Recieved',description = message.content, color=16711758)
                        embed4.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
                        embed4.timestamp = datetime.datetime.utcnow()
                        await member.send(embed = embed4)
    



# adds an user to the tickets channel
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



#close the ticket channel / delete the ticket channel
@bot.command()
@commands.has_permissions(manage_channels=True)
async def close(ctx, *args):
    if ctx.author.guild_permissions.manage_channels:
        if ctx.channel.category.name == 'modmail':
            

            format_args1 = list(args)

            format_args2 = ' '.join(format_args1)
            
            if str(args) != '()':
                close_reason = str(format_args2)
            else:
                close_reason = "None Given"


            topic = ctx.channel.topic
            if topic:
                member = ctx.guild.get_member(int(topic))
                if member:
                    embed = discord.Embed(title='ModMail Ticket Closed',description = f'`Reason: {close_reason}`', color=16711758)
                    embed.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author}')
                    embed.timestamp = datetime.datetime.utcnow()
                    await member.send(embed = embed)
                    
            await ctx.channel.delete(reason=close_reason)


        else:
            await ctx.message.delete()
            embed1 = discord.Embed(title='Wrong Channel!', description = '`Please use this Command in the ModMail Category!`', color=16711758)
            embed1.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author.name}')
            embed1.timestamp = datetime.datetime.utcnow()
            await ctx.channel.send(embed=embed1, delete_after=3)
    else:
        await ctx.message.cdelete()
        embed2 = discord.Embed(title='Access Denied', description = '`Required Permissions: Manage_Channels`', color=16711758)
        embed2.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author.name}')
        embed2.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed2, delete_after=2)





bot.run('YOUR BOT TOKEN')

