import discord
import random
import aiosqlite
import database
from database import insert_glumbo
from database import create_connection
from database import get_glumbo_data
from database import remove_glumbo
from jobs import job_work
from jobs import job_crime
from jobs import job_slut
from cryptography.fernet import Fernet
from config import token
from aiosqlite import Error
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
        title="Cooldown!", description=f'This command is on cooldown, you can use it in {round(error.retry_after, 2)} seconds!', colour=discord.Color.yellow()
    )
        await ctx.send(embed=embed)

@bot.tree.command(name = "glumbo", description="Says Glumbo! Just a test command to see if the bot works, nothing more", guild=discord.Object(id=998886208916688907))
@commands.cooldown(1, 15, commands.BucketType.user)
async def glumbo(ctx):
    await ctx.send("Glumbo!")

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def work(ctx):
    glumboAmount = random.randrange(0, 601)
    username = ctx.author.name

    # create a database connection
    conn = await create_connection("C:/Users/User/Desktop/python/glumbo.db")

    try:
        # add money to the user's account in the database
        await insert_glumbo(conn, username, glumboAmount)
    except Exception as e:
        await ctx.send(e)
    
    try:
        job = await job_work(glumboAmount)
        embed = discord.Embed(
            title="Work", description=job, colour=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(e)

@bot.command()
@commands.cooldown(1, 900, commands.BucketType.user)
async def crime(ctx):
    try:
        glumboAmount = random.randrange(0, 1001)
        status = random.choice([True, False])
    except Exception as e:
        await ctx.send(e)

    username = ctx.author.name

    # create a database connection
    conn = await create_connection("C:/Users/User/Desktop/python/glumbo.db")

    try:
        if status == True:
            # add money to the user's account in the database
            await insert_glumbo(conn, username, glumboAmount)
        else:
            await remove_glumbo(conn, username, glumboAmount)
    except Exception as e:
        await ctx.send(e)
    
    try:
        job = await job_crime(glumboAmount, status)
        if status == True:
            status_color = discord.colour.Color.yellow()
        else:
            status_color = discord.colour.Color.red()
        embed = discord.Embed(
            title="Crime", description=job, colour=status_color
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(e)


@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def slut(ctx):
    try:
        glumboAmount = random.randrange(0, 1001)
        status = random.choice([True, False])
    except Exception as e:
        await ctx.send(e)

    username = ctx.author.name

    # create a database connection
    conn = await create_connection("C:/Users/User/Desktop/python/glumbo.db")

    try:
        if status == True:
            # add money to the user's account in the database
            await insert_glumbo(conn, username, glumboAmount)
        else:
            await remove_glumbo(conn, username, glumboAmount)
    except Exception as e:
        await ctx.send(e)
    
    try:
        job = await job_slut(glumboAmount, status)
        if status == True:
            status_color = discord.colour.Color.yellow()
        else:
            status_color = discord.colour.Color.red()
        embed = discord.Embed(
            title="Slut", description=job, colour=status_color
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(e)


@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def addmoney(ctx, userToGiveMoneyTo: discord.Member, amountOfMoneyToGive):
    try:
        if not any(role.name == 'Admin' for role in ctx.author.roles):
            embed = discord.Embed(
            title="Add Money", description=f"You don't have the permission to run this command!", colour=discord.Color.yellow()
        )
            await ctx.send(embed=embed)
            return

        username = ctx.author.name
        conn = await create_connection("C:/Users/User/Desktop/python/glumbo.db")
        data = await insert_glumbo(conn, userToGiveMoneyTo.name, amountOfMoneyToGive)
    except Exception as e:
        await ctx.send(e)

    embed = discord.Embed(
        title="Add Money", description=f"Added <:glumbo:1003615679200645130>{amountOfMoneyToGive} to the user {userToGiveMoneyTo.mention}", colour=discord.Color.yellow()
    )
    await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def removemoney(ctx, userToRemoveMoneyFrom: discord.Member, amountOfMoneyToRemove):
    try:
        if not any(role.name == 'Admin' for role in ctx.author.roles):
            embed = discord.Embed(
            title="Add Money", description=f"You don't have the permission to run this command!", colour=discord.Color.yellow()
        )
            await ctx.send(embed=embed)
            return
        conn = await create_connection("C:/Users/User/Desktop/python/glumbo.db")
        data = await remove_glumbo(conn, userToRemoveMoneyFrom.name, amountOfMoneyToRemove)
    except Exception as e:
        await ctx.send(e)

    if data == "This user doesn't have any money to remove!":
        embed = discord.Embed(
            title="Add Money", description=f"{data}", colour=discord.Color.yellow()
        )
    else:
        embed = discord.Embed(
            title="Add Money", description=f"Removed <:glumbo:1003615679200645130>{amountOfMoneyToRemove} from the user {userToRemoveMoneyFrom.mention}", colour=discord.Color.yellow()
        )
    await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 7200, commands.BucketType.user)
async def rob(ctx, userToRemoveMoneyFrom: discord.Member):
    status = random.random() < 0.2
    try:
        conn = await create_connection("C:/Users/User/Desktop/python/glumbo.db")
    except Exception as e:
        await ctx.send(e)
    
    try:
        amountOfMoneyStolen = await get_glumbo_data(userToRemoveMoneyFrom.name) * 0.05
        if status < 0.2:
            if amountOfMoneyStolen == "This user doesn't have any money to rob!":
                embed = discord.Embed(
                    title="Rob", description=f"{amountOfMoneyStolen}", colour=discord.Color.yellow()
                )
            else:
                amountOfMoney = await get_glumbo_data(userToRemoveMoneyFrom.name)
                amountOfMoneyStolen = round(amountOfMoney * 0.05)
                amountOfMoneyStolen = await remove_glumbo(conn, userToRemoveMoneyFrom.name, amountOfMoneyStolen)
                embed = discord.Embed(
                title="Rob", description=f"Stole <:glumbo:1003615679200645130>{amountOfMoneyStolen} from the user {userToRemoveMoneyFrom.mention}", colour=discord.Color.yellow()
            )
            await ctx.send(embed=embed)
        else:
            fine = random.randrange(0, 1001)
            amountOfMoneyStolen = await remove_glumbo(conn, ctx.author.name, fine)
            embed = discord.Embed(
                title="Rob", description=f"You tried to rob {userToRemoveMoneyFrom.mention}, but you were caught and paid a <:glumbo:1003615679200645130>{fine} fine!", colour=discord.Color.red()
            )
            await ctx.send(embed=embed)

        if amountOfMoneyStolen == "This user doesn't have any money to rob!":
            embed = discord.Embed(
                title="Rob", description=f"{amountOfMoneyStolen}", colour=discord.Color.yellow()
            )
            await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(e)

@bot.command(aliases=['bal'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def balance(ctx):
    try:
        username = ctx.author.name
        conn = await create_connection("C:/Users/User/Desktop/python/glumbo.db")
        data = await get_glumbo_data(username)
    except Exception as e:
        await ctx.send(e)

    if data == "You don't have any glumbo!":
        embed = discord.Embed(
        title=f"{username}'s balance", description=f"{data}", colour=discord.Color.yellow()
    )
    else:
        embed = discord.Embed(
        title=f"{username}'s balance", description=f"You have <:glumbo:1003615679200645130>{data}!", colour=discord.Color.yellow()
    )

    await ctx.send(embed=embed)

bot.run(token)