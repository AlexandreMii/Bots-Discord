import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is online! Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong.')

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked.')

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has been banned.')

@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)  # +1 pour supprimer le message de commande
    await ctx.send(f'{amount} messages have been deleted.', delete_after=5)

@bot.command()
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f'Role {role.name} has been added to {member.mention}.')

@bot.command()
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f'Role {role.name} has been removed from {member.mention}.')

@bot.command()
async def listroles(ctx):
    roles = ctx.author.roles
    role_names = [role.name for role in roles]
    await ctx.send(f'Roles of {ctx.author.mention}: {", ".join(role_names)}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    bad_words = ['badword1', 'badword2']  # Remplacez par vos mots interdits
    for word in bad_words:
        if word in message.content.lower():
            await message.delete()
            await message.channel.send(f'{message.author.mention}, please do not use inappropriate language.', delete_after=5)
            break

bot.run('MTM1MDIxMTM1NzY4NTA1NTU0OQ.G3NCMK.dl8qxNVxRPrcOvtTBPKzlkWPVsq0_XnLLWesBI')

@bot.command()
async def createchannel(ctx, channel_name: str):
    guild = ctx.guild
    await guild.create_text_channel(channel_name)
    await ctx.send(f'Channel {channel_name} has been created.')

@bot.command()
async def deletechannel(ctx, channel: discord.TextChannel):
    await channel.delete()
    await ctx.send(f'Channel {channel.name} has been deleted.')

    import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ID du canal de logs
LOG_CHANNEL_ID = 8  # Remplacez par l'ID de votre canal de logs

@bot.event
async def on_ready():
    print(f'Bot is online! Logged in as {bot.user}')
    global log_channel
    log_channel = bot.get_channel(LOG_CHANNEL_ID)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong.')

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked.')
    if log_channel:
        await log_channel.send(f'User {member} has been kicked by {ctx.author.mention}. Reason: {reason}')

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has been banned.')
    if log_channel:
        await log_channel.send(f'User {member} has been banned by {ctx.author.mention}. Reason: {reason}')

@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)  # +1 pour supprimer le message de commande
    await ctx.send(f'{amount} messages have been deleted.', delete_after=5)

@bot.command()
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f'Role {role.name} has been added to {member.mention}.')
    if log_channel:
        await log_channel.send(f'Role {role.name} has been added to {member.mention} by {ctx.author.mention}.')

@bot.command()
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f'Role {role.name} has been removed from {member.mention}.')
    if log_channel:
        await log_channel.send(f'Role {role.name} has been removed from {member.mention} by {ctx.author.mention}.')

@bot.command()
async def listroles(ctx):
    roles = ctx.author.roles
    role_names = [role.name for role in roles]
    await ctx.send(f'Roles of {ctx.author.mention}: {", ".join(role_names)}')

@bot.command()
async def createchannel(ctx, channel_name: str):
    guild = ctx.guild
    await guild.create_text_channel(channel_name)
    await ctx.send(f'Channel {channel_name} has been created.')
    if log_channel:
        await log_channel.send(f'Channel {channel_name} has been created by {ctx.author.mention}.')

@bot.command()
async def deletechannel(ctx, channel: discord.TextChannel):
    await channel.delete()
    await ctx.send(f'Channel {channel.name} has been deleted.')
    if log_channel:
        await log_channel.send(f'Channel {channel.name} has been deleted by {ctx.author.mention}.')

@bot.command()
async def setnickname(ctx, member: discord.Member, nickname: str):
    await member.edit(nick=nickname)
    await ctx.send(f'Nickname of {member.mention} has been set to {nickname}.')
    if log_channel:
        await log_channel.send(f'Nickname of {member.mention} has been set to {nickname} by {ctx.author.mention}.')

@bot.command()
async def mute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)
    await member.add_roles(muted_role)
    await ctx.send(f'{member.mention} has been muted.')
    if log_channel:
        await log_channel.send(f'{member.mention} has been muted by {ctx.author.mention}.')

@bot.command()
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if muted_role:
        await member.remove_roles(muted_role)
        await ctx.send(f'{member.mention} has been unmuted.')
        if log_channel:
            await log_channel.send(f'{member.mention} has been unmuted by {ctx.author.mention}.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    bad_words = ['badword1', 'badword2']  # Remplacez par vos mots interdits
    for word in bad_words:
        if word in message.content.lower():
            await message.delete()
            await message.channel.send(f'{message.author.mention}, please do not use inappropriate language.', delete_after=5)
            if log_channel:
                await log_channel.send(f'{message.author.mention} used inappropriate language: {message.content}')
            break

bot.run('MTM1MDIxMTM1NzY4NTA1NTU0OQ.G3NCMK.dl8qxNVxRPrcOvtTBPKzlkWPVsq0_XnLLWesBI')

@bot.command()
async def ping(ctx):
    print("Ping command received")
    await ctx.send('Pong.')

    31896527441527
    