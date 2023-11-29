import discord
import random
import aiosqlite
import asyncio
import subprocess
from database import insert_glumbo
from database import create_connection
from database import get_cash_data
from database import get_bank_data
from database import remove_glumbo
from database import dep
from database import withd
from database import create_business
from database import buy_stocks
from database import sell_stocks
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

backup = "C:/Users/User/Desktop/python/Glumbonomy/backupdb.py"
stocks = "C:/Users/User/Desktop/python/Glumbonomy/stocks.py"

# Run the files
subprocess.Popen(["python", backup])
subprocess.Popen(["python", stocks])

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
        title="Cooldown!", description=f'This command is on cooldown, you can use it in {round(error.retry_after, 2)} seconds!', colour=discord.Color.yellow()
    )
        await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Error!", description="You have not provided enough arguments. Please check the command usage.", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Error!", description="This command is not found!", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.tree.command(name = "glumbo", description="Says Glumbo! Just a test command to see if the bot works, nothing more", guild=discord.Object(id=998886208916688907))
@commands.cooldown(1, 15, commands.BucketType.user)
async def glumbo(ctx):
    await ctx.send("Glumbo!")

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def scrungler(ctx):
    await ctx.send("<:scrungler:1082698194502287400>")

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
            await remove_glumbo(userID, glumboAmount)
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
    except Exception as e:
        await print(e)
    finally:
        await conn.close()


@bot.command()
@commands.cooldown(1, 900, commands.BucketType.user)
async def slut(ctx):
    try:
        glumboAmount = random.randrange(0, 1001)
        status = random.choice([True, False])
    except Exception as e:
        await print(e)

    userID = ctx.author.id

    # create a database connection
    conn = await create_connection("C:/Users/User/Desktop/python/glumbo.db")

    try:
        if status == True:
            # add money to the user's account in the database
            await insert_glumbo(conn, userID, glumboAmount)
        else:
            await remove_glumbo(userID, glumboAmount)
    except Exception as e:
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
        data = await remove_glumbo(userToRemoveMoneyFrom.id, amountOfMoneyToRemove)
    except Exception as e:
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
    

@bot.command()
@commands.cooldown(1, 5400, commands.BucketType.user)
async def rob(ctx, userToRemoveMoneyFrom: discord.Member):
    status = random.random() < 0.5
    try:
        conn = await create_connection("C:/Users/User/Desktop/python/glumbo.db")
    except Exception as e:
        await print(e)
    
    try:
        amountOfMoneyStolen = await get_cash_data(conn, userToRemoveMoneyFrom.id) * 0.5
        if status < 0.5:
            if amountOfMoneyStolen <= 0.0:
                embed = discord.Embed(
                    title="Rob", description=f"{userToRemoveMoneyFrom.mention} does not have any glumbo to rob! Epic fail!", colour=discord.Color.yellow()
                )
            else:
                amountOfMoney = await get_cash_data(conn, userToRemoveMoneyFrom.id)
                amountOfMoneyStolen = round(amountOfMoney * 0.5)
                amountOfMoneyStolen = await remove_glumbo(userToRemoveMoneyFrom.id, amountOfMoneyStolen)
                embed = discord.Embed(
                title="Rob", description=f"Stole <:glumbo:1003615679200645130>{amountOfMoneyStolen} from the user {userToRemoveMoneyFrom.mention}", colour=discord.Color.yellow()
            )
            await ctx.send(embed=embed)
        else:
            fine = random.randrange(0, 2001)
            amountOfMoneyStolen = await remove_glumbo(ctx.author.id, fine)
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
        await conn.close()
        await print(e)
    finally:
        await conn.close()

@bot.command(aliases=['bal'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def balance(ctx):
    try:
        conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
        userID = ctx.author.id
        cash = await get_cash_data(conn, userID)
        bank = await get_bank_data(conn, userID)
    except Exception as e:
        await conn.close()
        await print(e)

    if cash and bank == "You don't have any glumbo!":
        embed = discord.Embed(
        title=f"{ctx.author.name}'s balance", description=f"You don't have any glumbo!", colour=discord.Color.yellow()
    )
    else:
        embed = discord.Embed(
        title=f"{ctx.author.name}'s balance", description=f"Cash: <:glumbo:1003615679200645130>{cash}; Bank: <:glumbo:1003615679200645130>{bank}", colour=discord.Color.yellow()
    )

    await ctx.send(embed=embed)
    await conn.close()

@bot.command(aliases=['dep'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def deposit(ctx, glumboToDeposit = None):
    try:
        conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
        userID = ctx.author.id
        glumboToDeposit = await dep(conn, userID, glumboToDeposit)

        embed = discord.Embed(title="Deposit", description=glumboToDeposit, color=discord.Color.yellow())
        await ctx.send(embed=embed)

    except Exception as e:
        print(e)

@bot.command(aliases=['with'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def withdraw(ctx, glumboToWithdraw = None):
    try:
        conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
        userID = ctx.author.id
        glumboToWithdraw = await withd(conn, userID, glumboToWithdraw)

        embed = discord.Embed(title="Withdraw", description=glumboToWithdraw, color=discord.Color.yellow())
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

            # Check if the user has the item
            sql = "SELECT * FROM userItems WHERE userID = ? AND itemID = ?"
            await c.execute(sql, (ctx.author.id, itemID))
            user_item = await c.fetchone()

            if user_item is not None:
                if role_id:
                    role = ctx.guild.get_role(role_id)
                    if role:
                        if role in ctx.author.roles:
                            embed = discord.Embed(
                                title="Shop", description="You already have that role!", color=discord.colour.Color.red()
                            )
                        else:
                            await ctx.author.add_roles(role)
                            sql = "DELETE FROM userItems WHERE userID = ? AND itemID = ?"
                            await c.execute(sql, (ctx.author.id, itemID))
                            await conn.commit()

                            embed = discord.Embed(
                                title="Shop", description=f"You have been given the {role.name} role.", color=discord.colour.Color.yellow()
                            )
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                                title="Shop", description="Role not found!", color=discord.colour.Color.red()
                            )
                        await ctx.send(embed=embed)
                elif message:
                    sql = "DELETE FROM userItems WHERE userID = ? AND itemID = ?"
                    await c.execute(sql, (ctx.author.id, itemID))
                    await conn.commit()
                    await ctx.send(message)
                else:
                    embed = discord.Embed(
                        title="Shop", description="This item does not give any roles or messages!", color=discord.colour.Color.red()
                    )
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Shop", description="You do not have this item.", color=discord.colour.Color.red()
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Shop", description="Item not found in the shop.", color=discord.colour.Color.red()
            )
            await ctx.send(embed=embed)

        await conn.close()
    except Exception as e:
        await conn.close()
        print(e)


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def buy(ctx, itemName: str):
    try:

        userID = ctx.author.id

        # Connect to the database
        conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
        c = await conn.cursor()

        # Check if the item exists in the shop
        await c.execute("SELECT * FROM shop WHERE itemName = ?", (itemName,))
        item = await c.fetchone()

        # Check if the user has enough money to buy the item

        await c.execute("SELECT cash FROM userData WHERE userID = ?", (userID,))
        cash = (await c.fetchone())[0]
        
        # Get item price

        await c.execute("SELECT price FROM shop WHERE itemName = ?", (itemName,))
        price = (await c.fetchone())[0]

        if cash < price:
            embed = discord.Embed(title="Shop", description="You don't have enough cash to buy this item!", color=discord.Color.yellow())
            await ctx.send(embed=embed)
        else:
            if item is None:
                await ctx.send("This item does not exist in the shop.")
            else:
                # If the item exists, insert a new record into the userItems table
                await c.execute("INSERT INTO userItems (userID, itemID) VALUES (?, ?)", (userID, item[0]))
                await c.execute("UPDATE userData SET cash = cash - ? WHERE userID = ?", (price, userID,))
                await conn.commit()
                embed = discord.Embed(title="Shop", description=f"You have successfully bought {itemName}!", color=discord.Color.yellow())
                await ctx.send(embed=embed)
    except Exception as e:
        print(e)
    finally:
        # Close the connection
        await conn.close()

@bot.command(aliases=['inv'])
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
        embed = discord.Embed(title="Shop", description=f"You do not own any items!", color=discord.Color.red())
        await ctx.send(embed=embed)
    # Close the connection
    await conn.close()


@bot.command()
@commands.has_role(998911733081067570)
@commands.cooldown(1, 15, commands.BucketType.user)
async def createbusiness(ctx, businessName, stockName, stockPrice):
    try:
        if len(stockName) == 4:
            userID = ctx.author.id
            conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
            cash = await get_cash_data(conn, userID)

            if int(stockPrice) > 10001:
                embed = discord.Embed(title="Business", description=f"Your stock price can't be bigger than 10000 glumbo!", color=discord.Color.yellow())
                await ctx.send(embed=embed)
                return

            if int(cash) >= 100000:
                data = await create_business(conn, userID, businessName, stockName, stockPrice)

                if data == "User already has a business.":
                    embed = discord.Embed(title="Business", description=f"{data}", color=discord.Color.yellow())
                    await ctx.send(embed=embed)
                    return
                elif stockPrice > 0:                   
                    await remove_glumbo(userID, 100000)
                    embed = discord.Embed(title="Business", description=f"{data}", color=discord.Color.yellow())
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="Business", description=f"Your stock price can't be 0 or less!", color=discord.Color.red())
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Business", description=f"You can't don't have enough glumbo to create a business!", color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Business", description=f"Your stock name can't be less or greater than 4 characters!", color=discord.Color.red())
            await ctx.send(embed=embed)
    except Exception as e:
        print(e)
    finally:
        await conn.close()
        
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def stocks(ctx):
    try:
        # Connect to the database
        conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
        c = await conn.cursor()

        # Query the business table for all items
        await c.execute("SELECT businessName, userID, stockName, stockPrice, stocksBought, stocksSold FROM business")
        items = await c.fetchall()

        # Close the connection
        await conn.close()

        # Create an embed
        embed = discord.Embed(title="Stocks", description="Here are the items available in the stock market:", color=discord.Color.yellow())

        # Add each item to the embed
        for item in items:
            user = await bot.fetch_user(item[1])
            embed.add_field(name=f"{item[2]} (Company: {item[0]})", value=f"Price: <:glumbo:1003615679200645130>{item[3]}, Company owner: {user.mention}, Stocks bought: {item[4]}, Stocks sold: {item[5]}", inline=False)

        # Send the embed
        await ctx.send(embed=embed)
    except Exception as e:
        await conn.close()
        await print(e)


@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def buystock(ctx, stockName, stockAmount):
    try:      
       conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")       
       userID = ctx.author.id
       data = await buy_stocks(conn, userID, stockName, int(stockAmount))
       embed = discord.Embed(title="Stocks", description=data, color=discord.Color.yellow())
       await ctx.send(embed=embed)

    except Exception as e:
        print(e)
    finally:
        # Close the connection
        await conn.close()

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def sellstock(ctx, stockName, stockAmount):
    try:
        conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
        userID = ctx.author.id

        if stockAmount.lower() == 'all':
            # Perform the sell operation for all stocks
            data = await sell_stocks(conn, userID, stockName, stockAmount)
        elif stockAmount.isdigit() and int(stockAmount) > 0:
            # Perform the sell operation for the specified quantity
            data = await sell_stocks(conn, userID, stockName, int(stockAmount))
        else:
            await ctx.send("Please provide a valid quantity of stocks to sell.")
            return

        embed = discord.Embed(title="Stocks", description=data, color=discord.Color.yellow())
        await ctx.send(embed=embed)

    except Exception as e:
        print(e)
        await ctx.send("An error occurred while processing your request.")

    finally:
        # Close the connection
        if conn and not conn.closed:
            await conn.close()



@bot.command(aliases=['stockinv'])
@commands.cooldown(1, 10, commands.BucketType.user)
async def stockinventory(ctx):
    userID = ctx.author.id

    # Connect to the database
    conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
    c = await conn.cursor()

    # Query the userItems table for items owned by the user
    await c.execute("""
    SELECT stockName 
    FROM userStocks  
    WHERE userID = ?
    """, (userID,))
    stocks = await c.fetchall()

    if stocks:
        # If the user owns any items, send a message with the list of items
        stock_list = ', '.join(item[0] for item in stocks)

        embed = discord.Embed(
            title="Inventory", description=f"You own the following stocks: {stock_list}", color=discord.colour.Color.yellow()
        )

        await ctx.send(embed=embed)
    else:
        # If the user does not own any items, send a message to inform them
        embed = discord.Embed(title="Shop", description=f"You do not own any stocks!", color=discord.Color.red())
        await ctx.send(embed=embed)
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
