import discord
from discord import member
from discord.ext import commands
from discord import DMChannel
import asyncio
import random
import requests
import json
from pprint import pprint

hypixelAPIkey = 'd2b434cf-f481-450a-9efa-e666b09bad4f'

def getInfo(call):
    r = requests.get(call)
    return r.json



bot = commands.Bot(command_prefix='=')


@bot.event
async def on_ready():
    print('MathBot ({0.user}) is active.'.format(bot))
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name='over the Mathematics Guild Discord'))
        await asyncio.sleep(10)
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name='=help'))
        await asyncio.sleep(10)

@bot.command()
async def verify(ctx, minecraftUsername, user : discord.User = None):
    if ctx.channel.id == 926487494600581183:
        if user == None:
            obvMath = await bot.fetch_user('873911255184834571')
            embed = discord.Embed(description = "Automatic verification is not finished yet, so it has to be done manually for now. Don't worry though, you don't have to do anything else. obvMath, the guild master, has been notified that you are trying to verify and will verify you ASAP. Thank you for your cooperation!", color=0xFFD700)
            embed.add_field(name='‏', value=f'The Minecraft username you are trying to verify with is **{minecraftUsername}**. If this is not correct, re-run `=verify <Minecraft Username>` with the correct username. You can also use this command after you are verified if you have changed your Minecraft username.')
            obvMathEmbed = discord.Embed(description = f'**{ctx.author.name}#{ctx.author.discriminator}** is trying to verify with the Minecraft username **{minecraftUsername}.**', color=0xFFD700)
            obvMathEmbed.add_field(name='‏', value=f'[{minecraftUsername} on 25karma](https://25karma.xyz/player/{minecraftUsername}) - [{minecraftUsername} on Plancke](https://plancke.io/hypixel/player/stats/{minecraftUsername})')
            await ctx.reply(embed=embed)
            await DMChannel.send(obvMath, embed=obvMathEmbed)
        else:
            if ctx.author.id == 873911255184834571:
                obvMath = await bot.fetch_user('873911255184834571')
                embed = discord.Embed(description = "Automatic verification is not finished yet, so it has to be done manually for now. Don't worry though, you don't have to do anything else. obvMath, the guild master, has been notified that you are trying to verify and will verify you ASAP. Thank you for your cooperation!", color=0xFFD700)
                embed.add_field(name='‏', value=f'The Minecraft username you are trying to verify with is **{minecraftUsername}**. If this is not correct, re-run `=verify <Minecraft Username>` with the correct username. You can also use this command after you are verified if you have changed your Minecraft username.')
                obvMathEmbed = discord.Embed(description = f'**{user}** is trying to verify with the Minecraft username **{minecraftUsername}.**', color=0xFFD700)
                obvMathEmbed.add_field(name='‏', value=f'[{minecraftUsername} on 25karma](https://25karma.xyz/player/{minecraftUsername}) - [{minecraftUsername} on Plancke](https://plancke.io/hypixel/player/stats/{minecraftUsername})')
                await ctx.reply(embed=embed)
                await DMChannel.send(obvMath, embed=obvMathEmbed)
            else:
                pass
    else:
        embed = discord.Embed(description = 'You cannot use the verify command in this channel!', color = 0xFF0000)
        await ctx.reply(embed=embed)

@bot.command()
async def approve(ctx, user : discord.User, minecraftUsername, guildRole):
    unverifiedRole = discord.utils.get(user.guild.roles, name='Unverified')
    memberRole = discord.utils.get(user.guild.roles, name='Member')
    trustedRole = discord.utils.get(user.guild.roles, name='Trusted')
    staffRole = discord.utils.get(user.guild.roles, name='Staff')
    verifyChannel = bot.get_channel(926487494600581183)
    logChannel = bot.get_channel(925493868760272947)
    if ctx.author.id == 873911255184834571:
        if guildRole == 'Member' or guildRole == 'member':
            await ctx.message.delete()
            await user.edit(nick=minecraftUsername)
            await user.remove_roles(unverifiedRole)
            await user.add_roles(memberRole)
        elif guildRole == 'Trusted' or guildRole == 'trusted':
            await ctx.message.delete()
            await user.edit(nick=f'[Trusted] {minecraftUsername}')
            await user.remove_roles(unverifiedRole)
            await user.add_roles(memberRole)
            await user.add_roles(trustedRole)
        elif guildRole == 'Staff' or guildRole == 'staff':
            await ctx.message.delete()
            await user.edit(nick=f'[Staff] {minecraftUsername}')
            await user.remove_roles(unverifiedRole)
            await user.add_roles(memberRole)
            await user.add_roles(trustedRole)
            await user.add_roles(staffRole)
        embed = discord.Embed(description = f'**{user.display_name}#{user.discriminator}** has been verified with the Minecraft account **{minecraftUsername}** and the guild rank of **{guildRole}**!', color = 0x12EDFF)
        dmEmbed = discord.Embed(description = f'You have been verified with the Minecraft account **{minecraftUsername}** and the guild rank of {guildRole} in the Mathematics Guild Discord server.', color = 0x12EDFF)
        await verifyChannel.send(embed=embed)
        await logChannel.send(embed=embed)
        await user.send(embed=dmEmbed)
    else:
        embed = discord.Embed(description = f'{ctx.author.mention}, you do not have permission to do that.', color = 0xFF0000)
        await ctx.send(embed=embed)

@bot.command()
async def notlinked(ctx, user : discord.User):
    verifyChannel = bot.get_channel(926487494600581183)
    if ctx.author.id == 873911255184834571:
        embed = discord.Embed(description = 'Please link your Discord account to Hypixel. See the attatched video for instructions.', color=0xFF0000)
        await ctx.message.delete()
        await verifyChannel.send(embed=embed)
        await verifyChannel.send('https://imgur.com/a/mL8qLlh')
        await verifyChannel.send(f'( {user.mention} )')

@bot.command()
async def setrank(ctx, user : discord.User, minecraftUsername, rank):
    memberRole = discord.utils.get(user.guild.roles, name='Member')
    trustedRole = discord.utils.get(user.guild.roles, name='Trusted')
    staffRole = discord.utils.get(user.guild.roles, name='Staff')
    if ctx.author.id == 873911255184834571:
        if rank == 'Member' or rank == 'member':
            if memberRole in user.roles and not trustedRole in user.roles and not staffRole in user.roles:
                embed = discord.Embed(description = f'{minecraftUsername} is already is a member.', color=0xFF0000)
                await ctx.send(embed=embed)
            elif memberRole in user.roles and trustedRole in user.roles and not staffRole in user.roles:
                embed = discord.Embed(description = f"{minecraftUsername}'s rank has been changed from **trusted** to **member**.", color=0x00FF00)
                await user.edit(nick=minecraftUsername)
                await user.remove_roles(trustedRole)
                await ctx.send(embed=embed)
            elif memberRole in user.roles and trustedRole in user.roles and staffRole in user.roles:
                embed = discord.Embed(description = f"{minecraftUsername}'s rank has been changed from **staff** to **member**.", color=0x00FF00)
                await user.edit(nick=minecraftUsername)
                await user.remove_roles(staffRole)
                await user.remove_roles(trustedRole)
                await ctx.send(embed=embed)
        if rank == 'Trusted' or rank == 'trusted':
            if memberRole in user.roles and not trustedRole in user.roles and not staffRole in user.roles:
                embed = discord.Embed(description = f"{minecraftUsername}'s rank has been changed from **member** to **trusted**.", color=0x00FF00)
                await user.edit(nick=f'[Trusted] {minecraftUsername}')
                await user.add_roles(trustedRole)
                await ctx.send(embed=embed)
            elif memberRole in user.roles and trustedRole in user.roles and not staffRole in user.roles:
                embed = discord.Embed(description = f'{minecraftUsername} is already a trusted member.', color=0xFF0000)
                await ctx.send(embed=embed)
            elif memberRole in user.roles and trustedRole in user.roles and staffRole in user.roles:
                embed = discord.Embed(description = f"{minecraftUsername}'s rank has been changed from **staff** to **trusted**.", color=0x00FF00)
                await user.edit(nick=f'[Trusted] {minecraftUsername}')
                await user.remove_roles(staffRole)
                await ctx.send(embed=embed)
        if rank == 'Staff' or rank == 'staff':
            if memberRole in user.roles and not trustedRole in user.roles and not staffRole in user.roles:
                embed = discord.Embed(description = f"{minecraftUsername}'s rank has been changed from **member** to **staff**.", color=0x00FF00)
                await user.edit(nick=f'[Staff] {minecraftUsername}')
                await user.add_roles(trustedRole)
                await user.add_roles(staffRole)
                await ctx.send(embed=embed)
            elif memberRole in user.roles and trustedRole in user.roles and not staffRole in user.roles:
                embed = discord.Embed(description = f"{minecraftUsername}'s rank has been changed from **trusted** to **staff**.", color=0x00FF00)
                await user.edit(nick=f'[Staff] {minecraftUsername}')
                await user.add_roles(staffRole)
                await ctx.send(embed=embed)
            elif memberRole in user.roles and trustedRole in user.roles and staffRole in user.roles:
                embed = discord.Embed(description = f'{minecraftUsername} is already a staff member.', color=0xFF0000)
                await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description = f'{ctx.author.mention}, you do not have permission to do that.', color = 0xFF0000)
        await ctx.send(embed=embed)

@bot.command()
async def namechange(ctx, newMinecraftUsername):
    obvMath = await bot.fetch_user('873911255184834571')
    embed = discord.Embed(description = 'Please wait until a staff member approves your name change.', color = 0xFFF504)
    embed.add_field(name='‏', value=f'Your new Minecraft username is **{newMinecraftUsername}**, correct?')
    obvMathEmbed = discord.Embed(description=f'**{ctx.author}** (**{ctx.author.display_name}**) is trying to verify their name change to **{newMinecraftUsername}**.', color = 0xFFF504)
    await ctx.reply(embed=embed)
    await DMChannel.send(obvMath, embed=obvMathEmbed)

@bot.command(aliases=['staffping', 'helpstaff', 'pingstaff'])
@commands.cooldown(1, 1800, commands.BucketType.user)
async def staffhelp(ctx):
    await ctx.send('Pinging <@&925399563320320041>!')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def embed(ctx, *, message):
    rng = random.randint(1,2)
    if rng == 1:
        embed = discord.Embed(description = message, color = 0xFFF504)
        await ctx.message.delete()
        await ctx.send(embed=embed)
    if rng == 2:
        embed = discord.Embed(description = message, color = 0x12EDFF)
        await ctx.message.delete()
        await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def editembed(ctx, message, *, newMessage):
    rng = random.randint(1,2)
    if rng == 1:
        embed = discord.Embed(description = newMessage, color = 0xFFF504)
        await ctx.message.delete()
        await message.edit(embed=embed)
    if rng == 2:
        embed = discord.Embed(description = newMessage, color = 0x12EDFF)
        await ctx.message.delete()
        await message.edit(embed=embed)

@bot.command(aliases = ['purge', 'clean'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int = 999999999):
    logChannel = bot.get_channel(925493868760272947)
    if ctx.channel.id == 925493868760272947 or ctx.channel.id == 934563515623166032:
        embed = discord.Embed(description = f'{ctx.author.mention}, you cannot use that command here.', color = 0xFF0000)
        await ctx.send(embed=embed)
    else:
        await ctx.channel.purge(limit = amount + 1)
        await asyncio.sleep(0.2)
        if amount == 999999999:
            embed = discord.Embed(description = f'Cleared {ctx.message.channel.mention}.', color = 0x00FF00)
            logChannelEmbed = discord.Embed(description = f'{ctx.author.mention} cleared {ctx.message.channel.mention}.', color = 0x00FF00)
            await ctx.send(embed=embed, delete_after=5)
            await logChannel.send(embed=logChannelEmbed)
        else:
            embed = discord.Embed(description = f'Cleared **{amount}** messages in {ctx.message.channel.mention}.', color = 0x00FF00)
            logChannelEmbed = discord.Embed(description = f'{ctx.author.mention} cleared **{amount}** messages in {ctx.message.channel.mention}.', color = 0x00FF00)
            await ctx.send(embed=embed, delete_after=5)
            await logChannel.send(embed=logChannelEmbed)

@bot.command(aliases = ['spamthebot', 'spamthebotlol', 'spamthebotlul', 'botspam'])
@commands.cooldown(1, 60, commands.BucketType.user)
async def spam(ctx):
    await ctx.send('spam spam spam spam spam spam spam spam spam spam spam spam spam spam spam spam spam spam spam spam spam spam spam spam spam spam')
    await ctx.send(f'bot spammed by {ctx.author.mention}')

bot.remove_command('help')
@bot.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(description = '`=help` command is currently a work in progress and is not available yet.')
    await ctx.reply(embed=embed)

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send(f'You can use that again in **{round(error.retry_after, 2)}** seconds.')
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.send('You do not have permission to do that.')
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f'You are missing the argument **{error.param}**')
        

@bot.event
async def on_message(message):
    if message.channel.id == 926487494600581183 and message.content.startswith('verify') or message.channel.id == 926487494600581183 and message.content.startswith('-verify'):
        embed = discord.Embed(description = 'Did you mean `=verify`?', color = 0xFF0000)
        await message.reply(embed=embed)
    await bot.process_commands(message)

bot.run('TOKEN')
