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
        ab=0

        guild_dict = {

        }


        emoji_dict = {
            '0': '❌',
            '1': "1️⃣",
            '2': "2️⃣",
            '3': "3️⃣",
            '4': "4️⃣",
            '5': "5️⃣",
            '6': "6️⃣",
            '7': "7️⃣",
            '8': '8️⃣',
            '9': '9️⃣',
            '10': '🔟',
        }

        react_dict = {
            '❌': 0,
            "1️⃣": 1,
            "2️⃣": 2,
            "3️⃣": 3,
            "4️⃣": 4,
            "5️⃣": 5,
            "6️⃣": 6,
            "7️⃣": 7,
            '8️⃣': 8,
            '9️⃣': 9,
            '🔟': 10,
        }



        embed_select= discord.Embed(title='Select Server to Send Message', description=f'*React with the* ***X*** *to cancel the support request*\n‎‎‏‏‎ ‎',color=65535)


        for guild_check in bot.guilds:
            if guild_check.get_member(message.author.id) is not None:
                ab +=1
                guild_dict[f"{ab}"] = f"{guild_check.id}"
            
                emoji= emoji_dict.get(f"{ab}")
                embed_select.add_field(name=emoji + ' ' + guild_check.name, value=f'**ID:** {guild_check.id}')
            else:
                pass



        msg = await message.author.send(embed=embed_select)

        

        if ab > 2:
            reaction = await get_reacts(message.author, bot, msg, ['❌',"1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣",'8️⃣','9️⃣','🔟'])
        elif ab == 2:
            reaction = await get_reacts(message.author, bot, msg, ['❌',"1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣"])
        else:
            reaction = await get_reacts(message.author, bot, msg, ['❌',"1️⃣","2️⃣","3️⃣","4️⃣","5️⃣"])



        if reaction != '❌':
            await msg.delete()
            main_react = react_dict.get(f"{reaction}")
            guild = bot.get_guild(int(guild_dict.get(f"{main_react}")))


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
            

            log_chan = utils.get(categ.channels, name = "modmail_logs")
            if not log_chan:
                log_chan = await categ.create_text_channel(name = "modmail_logs")
            
                


            if message.attachments != empty_arr:
                files = message.attachments

                for file in files:
                    embed33 = discord.Embed(title='Message Recieved', description=message.content, color=65535)
                    embed33.set_thumbnail(url=file.url)
                    embed33.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
                    embed33.timestamp = datetime.datetime.utcnow()
                    await channel.send(embed=embed33)


                    embed332 = discord.Embed(title=f'Message Recieved: #{channel.name}', description=message.content, color=65535)
                    embed332.set_thumbnail(url=file.url)
                    embed332.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
                    embed332.timestamp = datetime.datetime.utcnow()
                    await log_chan.send(embed=embed332)


            else:
                embed3 = discord.Embed(title='Message Recieved',description = message.content, color=65535)
                embed3.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
                embed3.timestamp = datetime.datetime.utcnow()
                await channel.send(embed = embed3)



                embed333 = discord.Embed(title=f'Message Recieved: #{channel.name}',description = message.content, color=65535)
                embed333.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
                embed333.timestamp = datetime.datetime.utcnow()
                await log_chan.send(embed=embed333)
        
        else:
            await msg.delete()



    elif isinstance(message.channel, discord.TextChannel):
        if message.content.startswith(bot.command_prefix):
            pass
        else:
            guild = message.guild
            categ = utils.get(guild.categories, name = "modmail")
            log_chan = utils.get(categ.channels, name = "modmail_logs")
            topic = message.channel.topic
            if topic:
                member = message.guild.get_member(int(topic))
                if member:
                    if message.attachments != empty_arr:
                        files = message.attachments

                        for file in files:
                            embed44 = discord.Embed(title='Message Recieved', description=message.content, color=65535)
                            embed44.set_thumbnail(url=file.url)
                            embed44.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
                            embed44.timestamp = datetime.datetime.utcnow()
                            await member.send(embed=embed44)

                            embed442 = discord.Embed(title=f'Message Sent: #{message.channel.name}', description=message.content, color=65535)
                            embed442.set_thumbnail(url=file.url)
                            embed442.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
                            embed442.timestamp = datetime.datetime.utcnow()
                            await log_chan.send(embed=embed442)

                    else:
                        embed4 = discord.Embed(title='Message Recieved',description = message.content, color=65535)
                        embed4.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
                        embed4.timestamp = datetime.datetime.utcnow()
                        await member.send(embed = embed4)

                        embed444 = discord.Embed(title=f'Message Sent: #{message.channel.name}',description = message.content, color=65535)
                        embed444.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
                        embed444.timestamp = datetime.datetime.utcnow()
                        await log_chan.send(embed = embed444)
    



# adds an user to the tickets channel
@bot.command()
@commands.has_permissions(manage_channels=True)
async def add(ctx, *args):
    await ctx.message.delete()
    guild = ctx.message.guild
    categ = utils.get(guild.categories, name = "modmail")
    log_chan = utils.get(categ.channels, name = "modmail_logs")


    format_args = list(args)

    user1 = format_args[0].strip('>').strip('<').strip('@').replace('!','')
    user2 = ctx.guild.get_member(int(user1))

    await ctx.channel.set_permissions(user2, view_channel=True, send_messages=True)
    await ctx.send(f'{ctx.author.mention} added {user2.mention} to the ticket!')
    topic = ctx.channel.topic
    if topic:
        member = ctx.guild.get_member(int(topic))
        if member:
            embed = discord.Embed(title='Added User to Ticket',description = f'{ctx.author.mention} added {user2.mention} to the ticket!', color=65535)
            embed.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author}')
            embed.timestamp = datetime.datetime.utcnow()
            await member.send(embed = embed)


            embed22 = discord.Embed(title=f'Added User to Ticket: #{ctx.channel.name}',description = f'{ctx.author.mention} added {user2.mention} to the ticket!', color=65535)
            embed22.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author}')
            embed22.timestamp = datetime.datetime.utcnow()
            await log_chan.send(embed = embed22)



#close the ticket channel / delete the ticket channel
@bot.command()
@commands.has_permissions(manage_channels=True)
async def close(ctx, *args):
    if ctx.author.guild_permissions.manage_channels:
        if ctx.channel.category.name == 'modmail':

            guild = ctx.message.guild
            categ = utils.get(guild.categories, name = "modmail")
            log_chan = utils.get(categ.channels, name = "modmail_logs")
 
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
                    embed = discord.Embed(title='ModMail Ticket Closed',description = f'`Reason: {close_reason}`', color=65535)
                    embed.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author}')
                    embed.timestamp = datetime.datetime.utcnow()
                    await member.send(embed = embed)



                    embed23 = discord.Embed(title=f'ModMail Ticket Closed: #{ctx.channel.name}',description = f'`Reason: {close_reason}`', color=65535)
                    embed23.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author}')
                    embed23.timestamp = datetime.datetime.utcnow()
                    await log_chan.send(embed = embed23)
                    
                    
            await ctx.channel.delete(reason=close_reason)


        else:
            await ctx.message.delete()
            embed1 = discord.Embed(title='Wrong Channel!', description = '`Please use this Command in the ModMail Category!`', color=65535)
            embed1.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author.name}')
            embed1.timestamp = datetime.datetime.utcnow()
            await ctx.channel.send(embed=embed1, delete_after=3)
    else:
        await ctx.message.cdelete()
        embed2 = discord.Embed(title='Access Denied', description = '`Required Permissions: Manage_Channels`', color=65535)
        embed2.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author.name}')
        embed2.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed2, delete_after=2)

bot.run('BOT TOKEN')

