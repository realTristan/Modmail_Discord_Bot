import discord, os, os.path, json, datetime as datetime, asyncio
from discord.ext import commands
from discord.utils import get, find
from discord.ext.commands import has_permissions



class Core(commands.Cog):
    def __init__(self, client):
        self.client = client

    def write(self, file, data):
        with open(os.path.dirname(__file__) + f'\\..\\json\\{file}.json','w') as f:
            json.dump(data, f, indent=4)


    def modRole(self, guild):
        with open(os.path.dirname(__file__) + f'\\..\\json\\data.json','r+') as f:
            data=json.load(f)
            return guild.get_role(int(data[str(guild.id)]["mod_role"]))


    def logChannel(self, message, content, name):
        if len(message.attachments) != 0:
            for file in message.attachments:
                log_embed = discord.Embed(title=f'New Message: {name}', description=content, color=65535, timestamp = datetime.datetime.utcnow())
                log_embed.set_thumbnail(url=file.url); log_embed.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
        else:
            log_embed = discord.Embed(title=f'New Message: {name}',description = content, color=65535, timestamp = datetime.datetime.utcnow())
            log_embed.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
        return log_embed



    @commands.command()
    @has_permissions(administrator=True)
    async def setup(self, ctx, role:discord.Role):
        with open(os.path.dirname(__file__) + f'\\..\\json\\data.json','r+') as f:
            data=json.load(f)
            data.update({ctx.guild.id: {"mod_role": role.id}})
            self.write("data", data)
            
            if not get(ctx.guild.categories, name = "modmail"):
                categ = await ctx.guild.create_category("modmail")
                await categ.set_permissions(ctx.guild.default_role, read_messages=False, view_channel=False)
                await categ.set_permissions(role, read_messages = True, view_channel = True)
                await categ.create_text_channel(name = "modmail_logs")
            
            await ctx.send(embed=discord.Embed(description=f'{ctx.author.mention} has successfully setup modmail', color=65535))



    @commands.command()
    async def shelp(self, ctx):
        embed = discord.Embed(title='Snow™ Jr. ModMail Commands', color=65535, timestamp = datetime.datetime.utcnow())
        embed.add_field(name='Quick Send', value='Quickly send a message to a server\n!send (server id) (message)')
        embed.add_field(name='Close Ticket', value='Close a ticket\n!close (reason)')
        embed.add_field(name='Add User', value='Adds an user to the ticket\n!add (@user)')
        embed.add_field(name='Remove User', value='Removes an user from the ticket\n!remove (@user)')
        embed.add_field(name='Hidden Message', value='Type a hidden message\n**!**(message)')
        embed.set_footer(icon_url= f'{ctx.author.avatar_url}', text=ctx.author)
        await ctx.send(embed=embed)



    @commands.Cog.listener()
    async def get_reacts(self, user, message, emojis, guild_count):
        count=-1
        for i in range(len(emojis)):
            count+=1
            if count <= guild_count:
                await message.add_reaction(emojis[i])
                def check(reaction, reactor):
                    return reactor.id == user.id and reaction.emoji in emojis

        reaction, user = await self.client.wait_for("reaction_add", check=check)
        return reaction.emoji



    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel):
            if not message.author.bot:
                guild_count=0
                guild_dict = {}
                react_dict = {'❌': 0, "1️⃣": 1, "2️⃣": 2, "3️⃣": 3, "4️⃣": 4, "5️⃣": 5, "6️⃣": 6, "7️⃣": 7, '8️⃣': 8, '9️⃣': 9, '🔟': 10,}
                emojis=['❌', '1️⃣', '2️⃣', "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", '8️⃣', '9️⃣', '🔟']

                embed_select= discord.Embed(title='Select Server to Send Message', description=f'*React with the* ***X*** *to cancel the support request*\n‎‎‏‏‎*You can use* **!send (server id) (message)** *to use quick send!*\n ‎',color=65535)
                for guild_check in self.client.guilds:
                    if guild_check.get_member(message.author.id) is not None:
                        guild_count +=1
                        guild_dict[f"{guild_count}"] = f"{guild_check.id}"

                        embed_select.add_field(name=emojis[guild_count] + ' ' + guild_check.name, value=f'**ID:** {guild_check.id}')
            
                msg = await message.author.send(embed=embed_select)
                reaction = await self.get_reacts(message.author, msg, emojis, guild_count)

                if reaction != '❌':
                    guild = self.client.get_guild(int(guild_dict.get(f"{react_dict.get(f'{reaction}')}")))
                    categ = get(guild.categories, name = "modmail")
                    logs = get(categ.channels, name = "modmail_logs")

                    channel = get(categ.channels, topic = str(message.author.id))
                    if not channel:
                        channel = await categ.create_text_channel(name = f"{message.author}", topic = str(message.author.id))
                        await channel.send(f"||@here||\n**//** `Type a Hidden Message by using !(message)`\n**//** `Add Users to the Ticket by using !add (@user)`\n**//** `Remove Users from the Ticket by using !remove (@user)`\n**//** `Close the Ticket by using !close (reason)`\n **//** `Give an User the @[Modmail] role to Gain Access to this Category`")
                    
                    if len(message.attachments) != 0:
                        for file in message.attachments:
                            embed1 = discord.Embed(title='New Message', description=message.content, color=65535, timestamp = datetime.datetime.utcnow())
                            embed1.set_thumbnail(url=file.url); embed1.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
                            await channel.send(embed=embed1)
                    else:
                        embed2 = discord.Embed(title='New Message',description = message.content, color=65535, timestamp = datetime.datetime.utcnow())
                        embed2.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
                        await channel.send(embed = embed2)
                        
                    await logs.send(embed=self.logChannel(message, message.content, message.author))
                    await msg.delete()
                else:
                    await msg.delete()
                    return


        elif isinstance(message.channel, discord.TextChannel):
            if message.content.startswith(self.client.command_prefix):
                pass
            else:
                if not message.author.bot:
                    categ = get(message.guild.categories, name = "modmail")
                    logs = get(categ.channels, name = "modmail_logs")
                    member = message.guild.get_member(int(message.channel.topic))
                    if member:
                        if len(message.attachments) != 0:
                            for file in message.attachments:
                                embed = discord.Embed(title='New Message', description=message.content, color=65535, timestamp = datetime.datetime.utcnow())
                                embed.set_thumbnail(url=file.url); embed.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
                                await member.send(embed=embed)
                        else:
                            embed2 = discord.Embed(title='New Message',description = message.content, color=65535, timestamp = datetime.datetime.utcnow())
                            embed2.set_footer(icon_url= f'{message.author.avatar_url}', text=message.author)
                            await member.send(embed = embed2)

                        await logs.send(embed=self.logChannel(message, message.content, f'#{message.channel.name}'))



    @commands.command   
    async def send(self, ctx, guild_id: int, *args):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            guild = self.client.get_guild(guild_id)
            categ = get(guild.categories, name = "modmail")
            logs = get(categ.channels, name = "modmail_logs")

            channel = get(categ.channels, topic = str(ctx.author.id))
            if not channel:
                channel = await categ.create_text_channel(name = f"{ctx.author}", topic = str(ctx.author.id))
                await channel.send(f"||@here||\n**//** `Type a Hidden Message by using !(message)`\n**//** `Add Users to the Ticket by using !add (@user)`\n**//** `Remove Users from the Ticket by using !remove (@user)`\n**//** `Close the Ticket by using !close (reason)`\n **//** `Give an User the @[Modmail] role to Gain Access to this Category`")


        if len(ctx.message.attachments) != 0:
            files = ctx.message.attachments

            for file in files:
                embed =discord.Embed(title='New Message', description=' '.join(list(args)[0]), color=65535, timestamp = datetime.datetime.utcnow())
                embed.set_thumbnail(url=file.url); embed.set_footer(icon_url= f'{ctx.author.avatar_url}', text=ctx.author)
                await channel.send(embed=embed)

                sent_embed = discord.Embed(title=f'Message Sent: [{guild}]', color=65535, timestamp = datetime.datetime.utcnow())
                await ctx.author.send(embed=sent_embed, delete_after=2)

                new_embed = discord.Embed(title='New Message',description = ' '.join(list(args)[0]), color=65535, timestamp = datetime.datetime.utcnow())
                new_embed.set_footer(icon_url= f'{ctx.author.avatar_url}', text=ctx.author)
                await logs.send(embed=new_embed)
        else:
            embed = discord.Embed(title='New Message',description = ' '.join(list(args)[0]), color=65535, timestamp = datetime.datetime.utcnow())
            embed.set_footer(icon_url= f'{ctx.author.avatar_url}', text=ctx.author)
            await channel.send(embed = embed)

            sent_embed = discord.Embed(title=f'Message Sent: [{guild}]', color=65535, timestamp = datetime.datetime.utcnow())
            await ctx.author.send(embed=sent_embed, delete_after=2)

            new_embed = discord.Embed(title='New Message',description =' '.join(list(args)[0]), color=65535, timestamp = datetime.datetime.utcnow())
            new_embed.set_footer(icon_url= f'{ctx.author.avatar_url}', text=ctx.author)
            await logs.send(embed=new_embed)



    # adds an user to the tickets channel
    @commands.command()
    @has_permissions(manage_messages=True)
    async def add(self, ctx, user: discord.Member):
        if ctx.channel.category.name == 'modmail':
            categ = get(ctx.guild.categories, name = "modmail")
            logs = get(categ.channels, name = "modmail_logs")

            await ctx.channel.set_permissions(user, view_channel=True, send_messages=True)
            await ctx.send(f'{ctx.author.mention} added {user.mention} to the ticket!')
            if ctx.channel.topic:
                member = ctx.guild.get_member(int(ctx.channel.topic))
                if member:
                    embed = discord.Embed(title='Added User to Ticket',description = f'{ctx.author.mention} added {user.mention} to the ticket!', color=65535, timestamp = datetime.datetime.utcnow())
                    embed.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author}')
                    await member.send(embed = embed)

                    embed2 = discord.Embed(title=f'Added User to Ticket: #{ctx.channel.name}',description = f'{ctx.author.mention} added {user.mention} to the ticket!', color=65535, timestamp = datetime.datetime.utcnow())
                    embed2.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author}')
                    await logs.send(embed = embed2)



    # remove people from the ticket
    @commands.command()
    @has_permissions(manage_messages=True)
    async def remove(self, ctx, user:discord.Member):
        if ctx.channel.category.name == 'modmail':
            categ = get(ctx.guild.categories, name = "modmail")
            logs = get(categ.channels, name = "modmail_logs")

            await ctx.channel.set_permissions(user, view_channel=False, send_messages=False)
            await ctx.send(f'{ctx.author.mention} removed {user.mention} from the ticket!')
            if ctx.channel.topic:
                member = ctx.guild.get_member(int(ctx.channel.topic))
                if member:
                    embed = discord.Embed(title='Removed User from Ticket',description = f'{ctx.author.mention} removed {user.mention} from the ticket!', color=65535,timestamp = datetime.datetime.utcnow())
                    embed.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author}')
                    await member.send(embed = embed)

                    embed2 = discord.Embed(title=f'Removed User from Ticket: #{ctx.channel.name}',description = f'{ctx.author.mention} removed {user.mention} from the ticket!', color=65535, timestamp = datetime.datetime.utcnow())
                    embed2.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author}')
                    await logs.send(embed = embed2)




    #close the ticket channel / delete the ticket channel
    @commands.command()
    @has_permissions(manage_messages=True)
    async def close(self, ctx, *args):
        if ctx.channel.category.name == 'modmail':
            categ = get(ctx.guild.categories, name = "modmail")
            logs = get(categ.channels, name = "modmail_logs")
            
            if str(args) != '()': close_reason = ' '.join(list(args))
            else: close_reason = "None Given"

            if ctx.channel.topic:
                member = ctx.guild.get_member(int(ctx.channel.topic))
                if member:
                    embed = discord.Embed(title='ModMail Ticket Closed',description = f'`Reason: {close_reason}`', color=65535, timestamp = datetime.datetime.utcnow())
                    embed.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author}')
                    await member.send(embed=embed)

                    embed2 = discord.Embed(title=f'ModMail Ticket Closed: #{ctx.channel.name}',description = f'`Reason: {close_reason}`', color=65535, timestamp = datetime.datetime.utcnow())
                    embed2.set_footer(icon_url= f'{ctx.author.avatar_url}', text=f'{ctx.author}')
                    await logs.send(embed=embed2)
                    
                await ctx.channel.delete(reason=close_reason)







def setup(client):
    client.add_cog(Core(client))
