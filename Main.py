import discord
import random
import aiosqlite
import database
from database import insert_glumbo
from database import create_connection
from database import get_glumbo_data
from database import remove_glumbo
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
@commands.cooldown(1, 15, commands.BucketType.user)
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
        
    jobs = [f"You became a ShackCord admin and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"You worked at McDonald's as a janitor and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"You sold your soul to ShackCord and earned <:glumbo:1003615679200645130>{glumboAmount}!", f"You sold lemonade on the road and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"You started your own discord server and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"You started a successful corporation and earned<:glumbo:1003615679200645130>{glumboAmount}!", f"You bought a book from the local library and found<:glumbo:1003615679200645130>{glumboAmount} in it!", f"You found <:glumbo:1003615679200645130>{glumboAmount} in an old jacket you thought you lost!"]
    embed = discord.Embed(
        title="Work", description=random.choice(jobs), colour=discord.Color.yellow()
    )
    await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
@has_permissions(manage_roles=True, ban_members=True)
async def addmoney(ctx, userToGiveMoneyTo: discord.Member, amountOfMoneyToGive):
    try:
        username = ctx.author.name
        conn = await create_connection("C:/Users/User/Desktop/python/glumbo.db")
        data = await insert_glumbo(conn, userToGiveMoneyTo, amountOfMoneyToGive)
    except Exception as e:
        await ctx.send(e)
    embed = discord.Embed(
        title="Add Money", description=f"Added <:glumbo:1003615679200645130>{amountOfMoneyToGive} to the user {userToGiveMoneyTo.mention}", colour=discord.Color.yellow()
    )
    await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
@has_permissions(manage_roles=True, ban_members=True)
async def removemoney(ctx, userToRemoveMoneyFrom: discord.Member, amountOfMoneyToRemove):
    try:
        username = ctx.author.name
        conn = await create_connection("C:/Users/User/Desktop/python/glumbo.db")
        data = await remove_glumbo(conn, userToRemoveMoneyFrom, amountOfMoneyToRemove)
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
@commands.cooldown(1, 15, commands.BucketType.user)
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

bot.run('MTE3NDk5MzEzNTY2ODAzOTc2MA.GcewJh.fqSTNCMJR1rYvhyodlrK8rlc_pxKjl7ptexPU4')