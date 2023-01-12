
import discord
from discord import Option
from datetime import timedelta
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from datetime import datetime


bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} Logged in, api loggin = true.")


@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")




@bot.slash_command(name = 'timeout', description = "mutes/timeouts a member")
@commands.has_permissions(moderate_members = True)
async def timeout(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False), days: Option(int, max_value = 27, default = 0, required = False), hours: Option(int, default = 0, required = False), minutes: Option(int, default = 0, required = False), seconds: Option(int, default = 0, required = False)): #setting each value with a default value of 0 reduces a lot of the code
    if member.id == ctx.author.id:
        await ctx.respond("Error, try another user.")
        return
    if member.guild_permissions.moderate_members:
        await ctx.respond("Moderators cannot be moderated, try removing their roles first.")
        return
    duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
    if duration >= timedelta(days = 28): #added to check if time exceeds 28 days
        await ctx.respond("Error, time specified greater than 28 days.", ephemeral = True) #responds, but only the author can see the response
        return
    if reason == None:
        await member.timeout_for(duration)
        await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}>.")
    else:
        await member.timeout_for(duration, reason = reason)
        await ctx.respond(f"<@{member.id}> has been timed out for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}> for '{reason}'.")

@timeout.error
async def timeouterror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("Missing Permissions.")
    else:
        raise error

@bot.slash_command(name = 'unmute', description = "unmutes/untimeouts a member")
@commands.has_permissions(moderate_members = True)
async def unmute(ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False)):
    if reason == None:
        await member.remove_timeout()
        await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}>.")
    else:
        await member.remove_timeout(reason = reason)
        await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}> for '{reason}'.")

@unmute.error
async def unmuteerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("Missing Permissions.")
    else:
        raise error


@bot.slash_command(name = "ban", description = "Bans a member")
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: Option(discord.Member, description = "Who do you want to ban?"), reason: Option(str, description = "Why?", required = False)):
    if member.id == ctx.author.id: #checks to see if they're the same
        await ctx.respond("Error, try another user.")
    elif member.guild_permissions.administrator:
        await ctx.respond("You cannot ban other moderators, try removing their roles first.")
    else:
        if reason == None:
            reason = f"None provided by {ctx.author}"
        await member.ban(reason = reason)
        await ctx.respond(f"<@{ctx.author.id}>, <@{member.id}> has been banned successfully from this server!\n\nReason: {reason}")
    
@ban.error
async def banerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You need Ban Members and Administrator permissions to do this!")
    else:
        await ctx.respond("Something went wrong...") #most likely due to missing permissions
        raise error

@bot.slash_command(name = "kick", description = "Kicks a member")
@commands.has_permissions(kick_members = True, administrator = True)
async def kick(ctx, member: Option(discord.Member, description = "Who do you want to kick?"), reason: Option(str, description = "Why?", required = False)):
    if member.id == ctx.author.id: #checks to see if they're the same
        await ctx.respond("Error, try another user.")
    elif member.guild_permissions.administrator:
        await ctx.respond("You cannot kick other moderators, try removing their roles first.")
    else:
        if reason == None:
            reason = f"None provided by {ctx.author}"
        await member.kick(reason = reason)
        await ctx.respond(f"<@{ctx.author.id}>, <@{member.id}> has been kicked from this server!\n\nReason: {reason}")

@kick.error
async def kickerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You need Kick Members permissions to do this!")
    else:
        await ctx.respond("Something went wrong, contact support for help.") #most likely due to missing permissions 
        raise error


@bot.slash_command(name = "bans", description = "Get a list of members who are banned from this server!")
@commands.has_permissions(ban_members = True)
async def bans(ctx):
    await ctx.defer()
    bans = await ctx.guild.bans()
    embed = discord.Embed(title = f"List of Bans in {ctx.guild}", timestamp = datetime.now(), color = discord.Colour.red())
    for entry in bans:
        if len(embed.fields) >= 25:
            break
        if len(embed) > 5900:
            embed.add_field(name = "Too many bans to list")
        else:
            embed.add_field(name = f"Ban", value = f"Username: {entry.user.name}#{entry.user.discriminator}\nReason: {entry.reason}\nUser ID: {entry.user.id}\nIs Bot: {entry.user.bot}", inline = False)
    await ctx.respond(embed = embed)

@bot.slash_command(name = "unban", description = "Unbans a member")
@commands.has_permissions(ban_members = True)
async def unban(ctx, id: Option(discord.Member, description = "The User ID of the person you want to unban.", required = True)):
    await ctx.defer()
    member = await bot.get_or_fetch_user(id)
    await ctx.guild.unban(member)
    await ctx.respond(f"I have unbanned {member.mention}.")

@unban.error
async def unbanerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("You need ban members permissions to do this!")
    else: 
        await ctx.respond(f"Something went wrong, I couldn't unban this member or this member isn't banned.")
        raise error

@bot.slash_command(name = "help", description = "Sends Help!")
async def help(ctx): 
    await ctx.respond(f"Here you go <@{ctx.author.id}>, you got help **Well Done** :sunglasses:")


@bot.slash_command(name = "tag", Description = "does Somthing")
async def tag(ctx):
    await ctx.respond(f"To create a tag, join the support server and request a tag be created.")
 


bot.run('MTA0Mjg2MDI1MzAzNDg0MDA2NA.Gv5r6u.O9DDnZBHYd9yMX06dM6Mj-aHd66hwEWQx5ZVCY')


