import discord
import random
import aiosqlite
import asyncio
from database import insert_glumbo
from database import create_connection
from database import get_glumbo_data
from database import remove_glumbo
from database import create_table
from jobs import job_work
from jobs import job_crime
from jobs import job_slut
from config import token
from discord.ext import commands

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
    userID = ctx.author.id

    # create a database connection
    conn = await create_connection("C:/Users/User/Desktop/python/glumbo.db")

    try:
        # add money to the user's account in the database
        await insert_glumbo(conn, userID, glumboAmount)
    except Exception as e:
        await print(e)
    
    try:
        job = await job_work(glumboAmount)
        embed = discord.Embed(
            title="Work", description=job, colour=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        await conn.close()
    except Exception as e:
        await conn.close()
        await print(e)

@bot.command()
@commands.cooldown(1, 900, commands.BucketType.user)
async def crime(ctx):
    try:
        glumboAmount = random.randrange(0, 1001)
        status = random.choice([True, False])
    except Exception as e:
        await conn.close()
        await print(e)

    userID = ctx.author.id

    # create a database connection
    conn = await create_connection("C:/Users/User/Desktop/python/glumbo.db")

    try:
        if status == True:
            # add money to the user's account in the database
            await insert_glumbo(conn, userID, glumboAmount)
        else:
            await remove_glumbo(conn, userID, glumboAmount)
    except Exception as e:
        await conn.close()
        await print(e)
    
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
        await conn.close()
    except Exception as e:
        await conn.close()
        await print(e)


@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def slut(ctx):
    try:
        glumboAmount = random.randrange(0, 1001)
        status = random.choice([True, False])
    except Exception as e:
        await conn.close()
        await print(e)

    userID = ctx.author.id

    # create a database connection
    conn = await create_connection("C:/Users/User/Desktop/python/glumbo.db")

    try:
        if status == True:
            # add money to the user's account in the database
            await insert_glumbo(conn, userID, glumboAmount)
        else:
            await remove_glumbo(conn, userID, glumboAmount)
    except Exception as e:
        await conn.close()
        await print(e)
    
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
        await conn.close()
    except Exception as e:
        await conn.close()
        await print(e)


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

        userID = ctx.author.id
        conn = await create_connection("C:/Users/User/Desktop/python/glumbo.db")
        data = await insert_glumbo(conn, userToGiveMoneyTo.id, amountOfMoneyToGive)
    except Exception as e:
        await conn.close()
        await print(e)

    embed = discord.Embed(
        title="Add Money", description=f"Added <:glumbo:1003615679200645130>{amountOfMoneyToGive} to the user {userToGiveMoneyTo.mention}", colour=discord.Color.yellow()
    )
    await ctx.send(embed=embed)
    await conn.close()

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
        data = await remove_glumbo(conn, userToRemoveMoneyFrom.id, amountOfMoneyToRemove)
    except Exception as e:
        await conn.close()
        await print(e)

    if data == "This user doesn't have any money to remove!":
        embed = discord.Embed(
            title="Add Money", description=f"{data}", colour=discord.Color.yellow()
        )
    else:
        embed = discord.Embed(
            title="Add Money", description=f"Removed <:glumbo:1003615679200645130>{amountOfMoneyToRemove} from the user {userToRemoveMoneyFrom.mention}", colour=discord.Color.yellow()
        )
    await ctx.send(embed=embed)
    await conn.close()

@bot.command()
@commands.cooldown(1, 1, commands.BucketType.user)
async def rob(ctx, userToRemoveMoneyFrom: discord.Member):
    status = random.random()
    try:
        conn = await create_connection("C:/Users/User/Desktop/python/glumbo.db")
    except Exception as e:
        await print(e)
    
    try:
        amountOfMoneyStolen = await get_glumbo_data(conn, userToRemoveMoneyFrom.id) * 0.05
        if status < 0.05:
            if amountOfMoneyStolen == "This user doesn't have any money to rob!":
                embed = discord.Embed(
                    title="Rob", description=f"{amountOfMoneyStolen}", colour=discord.Color.yellow()
                )
            else:
                amountOfMoney = await get_glumbo_data(conn, userToRemoveMoneyFrom.id)
                amountOfMoneyStolen = round(amountOfMoney * 0.05)
                amountOfMoneyStolen = await remove_glumbo(conn, userToRemoveMoneyFrom.id, amountOfMoneyStolen)
                embed = discord.Embed(
                title="Rob", description=f"Stole <:glumbo:1003615679200645130>{amountOfMoneyStolen} from the user {userToRemoveMoneyFrom.mention}", colour=discord.Color.yellow()
            )
            await ctx.send(embed=embed)
        else:
            fine = random.randrange(0, 1001)
            amountOfMoneyStolen = await remove_glumbo(conn, ctx.author.id, fine)
            embed = discord.Embed(
                title="Rob", description=f"You tried to rob {userToRemoveMoneyFrom.mention}, but you were caught and paid a <:glumbo:1003615679200645130>{fine} fine!", colour=discord.Color.red()
            )
            await ctx.send(embed=embed)

        if amountOfMoneyStolen == "This user doesn't have any money to rob!":
            embed = discord.Embed(
                title="Rob", description=f"{amountOfMoneyStolen}", colour=discord.Color.yellow()
            )
            await ctx.send(embed=embed)
            await conn.close()
    except Exception as e:
        await conn.close()
        await print(e)

@bot.command(aliases=['bal'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def balance(ctx):
    try:
        conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
        userID = ctx.author.id
        data = await get_glumbo_data(conn, userID)
    except Exception as e:
        await conn.close()
        await print(e)

    if data == "You don't have any glumbo!":
        embed = discord.Embed(
        title=f"{userID}'s balance", description=f"{data}", colour=discord.Color.yellow()
    )
    else:
        embed = discord.Embed(
        title=f"{ctx.author.name}'s balance", description=f"You have <:glumbo:1003615679200645130>{data}!", colour=discord.Color.yellow()
    )

    await ctx.send(embed=embed)
    await conn.close()

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def additem(ctx, itemName: str, itemDescription: str, price: int, message: str = None, roleID: int = None):
    try:           
        # Connect to the database
        conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
        c = await conn.cursor()

        # Insert the new item into the shop table
        await c.execute("""
        INSERT INTO shop (itemName, itemDescription, price, message, roleID) 
        VALUES (?, ?, ?, ?, ?)
        """, (itemName, itemDescription, price, message, roleID))
        await conn.commit()

        embed = discord.Embed(
            title="Shop", description=f"Item {itemName} has been successfully added to the shop with the price of <:glumbo:1003615679200645130>{price}!", color=discord.colour.Color.yellow()
        )
        await ctx.send(embed=embed)

        # Close the connection
        await conn.close()
    except Exception as e:
        await conn.close()
        await print(e)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def removeitem(ctx, itemName: str):
    try:           
        # Connect to the database
        conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
        c = await conn.cursor()

        # Insert the new item into the shop table
        await c.execute("""
        DELETE FROM userItems WHERE itemID=?
        """, (itemName))

        await c.execute("""
        DELETE FROM shop WHERE itemID=?
        """, (itemName))

        await conn.commit()

        embed = discord.Embed(
            title="Shop", description=f"Item {itemName} has been successfully removed from the shop!", color=discord.colour.Color.yellow()
        )
        await ctx.send(embed=embed)

        # Close the connection
        await conn.close()
    except Exception as e:
        await conn.close()
        await print(e)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def use(ctx, itemName):
    try:
        conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
        c = await conn.cursor()
        sql = "SELECT roleID, message, itemID FROM shop WHERE itemName = ?"
        await c.execute(sql, (itemName,))
        row = await c.fetchone()
        
        if row is not None:
            role_id, message, itemID = row
            if role_id:
                role = ctx.guild.get_role(role_id)
                if role:
                    if role in ctx.author.roles:
                        embed = discord.Embed(
                            title="Shop", description="You already have that role!", color=discord.colour.Color.red()
                        )
                        await conn.close()
                    else:
                        await ctx.author.add_roles(role)
                        c = await conn.cursor()
                        sql = "DELETE FROM userItems WHERE userID = ? AND itemID = ?"
                        await c.execute(sql, (ctx.author.id, itemID))
                        await conn.commit()
                        await conn.close()

                        embed = discord.Embed(
                            title="Shop", description=f"You have been given the {role.name} role.", color=discord.colour.Color.yellow()
                        )
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                            title="Shop", description="Role not found!", color=discord.colour.Color.red()
                        )
                    await conn.close()
                    await ctx.send(embed=embed)
            elif message:
                c = await conn.cursor()
                sql = "DELETE FROM userItems WHERE userID = ? AND itemID = ?"
                await c.execute(sql, (ctx.author.id, itemID))
                await conn.commit()
                await conn.close()
                await ctx.send(message)
            else:
                embed = discord.Embed(
                    title="Shop", description="This item does not give any roles or messages!", color=discord.colour.Color.red()
                )
                await conn.close()
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Shop", description="Item not found in the shop.", color=discord.colour.Color.red()
            )
            await conn.close()
            await ctx.send(embed=embed)

    except Exception as e:
        await conn.close()
        print(e)


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def shop(ctx):
    try:
        # Connect to the database
        conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
        c = await conn.cursor()

        # Query the shop table for all items
        await c.execute("SELECT itemID, itemName, price, itemDescription FROM shop")
        items = await c.fetchall()

        # Close the connection
        await conn.close()

        # Create an embed
        embed = discord.Embed(title="Shop", description="Here are the items available in the shop:", color=discord.Color.yellow())

        # Add each item to the embed
        for item in items:
            embed.add_field(name=f"{item[1]} (ID: {item[0]})", value=f"Price: <:glumbo:1003615679200645130>{item[2]}, Description: {item[3]}", inline=False)

        # Send the embed
        await ctx.send(embed=embed)
    except Exception as e:
        await conn.close()
        await print(e)

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def buy(ctx, itemName: str):
    userID = ctx.author.id

    # Connect to the database
    conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
    c = await conn.cursor()

    # Check if the item exists in the shop
    await c.execute("SELECT * FROM shop WHERE itemName = ?", (itemName,))
    item = await c.fetchone()

    if item is None:
        await ctx.send("This item does not exist in the shop.")
    else:
        # If the item exists, insert a new record into the userItems table
        await c.execute("INSERT INTO userItems (userID, itemID) VALUES (?, ?)", (userID, item[0]))
        await conn.commit()
        await ctx.send(f"You have successfully bought {itemName}!")

    # Close the connection
    await conn.close()

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def inventory(ctx):
    userID = ctx.author.id

    # Connect to the database
    conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
    c = await conn.cursor()

    # Query the userItems table for items owned by the user
    await c.execute("""
    SELECT itemName 
    FROM shop 
    INNER JOIN userItems ON shop.itemID = userItems.itemID 
    WHERE userID = ?
    """, (userID,))
    items = await c.fetchall()

    if items:
        # If the user owns any items, send a message with the list of items
        item_list = ', '.join(item[0] for item in items)

        embed = discord.Embed(
            title="Inventory", description=f"You own the following items: {item_list}", color=discord.colour.Color.yellow()
        )

        await ctx.send(embed=embed)
    else:
        # If the user does not own any items, send a message to inform them
        await ctx.send("You do not own any items.")

    # Close the connection
    await conn.close()

async def reconnect_loop():
    while True:
        await asyncio.sleep(1)
        if bot.is_closed():
            print('Bot is disconnected, attempting to reconnect...')
            try:
                await bot.start(token)
                print('Reconnect successful.')
                break
            except Exception as e:
                print(f'Reconnect failed, {e}, retrying in 5 seconds...')
                await asyncio.sleep(5)

async def main():
    try:
        await bot.start(token)    
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Fatal exception {e}, running reconnect loop.")
        await reconnect_loop()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
