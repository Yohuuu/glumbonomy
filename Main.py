import nextcord as discord
from discord import SlashOption
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
from discord.ext import commands
from typing import Optional

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

backup = "C:/Users/2008a/OneDrive/Рабочий стол/python/Glumbonomy/backupdb.py"
stocks = "C:/Users/2008a/OneDrive/Рабочий стол/python/Glumbonomy/stocks.py"

# Run the files
subprocess.Popen(["python", backup])
subprocess.Popen(["python", stocks])

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Error!", description=f"This command is on cooldown, you can use it in {round(error.retry_after, 2)} seconds!.", color=discord.Color.red())
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

@bot.slash_command(name = "scrungler", description = "Scrungler")
async def scrungler(interaction: discord.Interaction):
    await interaction.response.send_message("<:scrungler:1082698194502287400>")

@bot.slash_command(name = "work", description = "Work for Glumbo!")
@commands.cooldown(1, 30, commands.BucketType.user)
async def work(interaction: discord.Interaction):
    glumboAmount = random.randrange(0, 601)
    userID = interaction.user.id
    
    # add money to the user's account in the database
    await insert_glumbo(userID, glumboAmount)
    job = await job_work(glumboAmount)
    embed = discord.Embed(
        title="Work", description=job, colour=discord.Color.yellow()
    )
    await interaction.response.send_message(embed=embed)

@bot.slash_command(name = "crime", description = "Commit a crime for some Glumbo! Or get caught and lose it.")
@commands.cooldown(1, 900, commands.BucketType.user)
async def crime(interaction: discord.Interaction):
    try:
        glumboAmount = random.randrange(0, 1001)
        status = random.choice([True, False])
    except Exception as e:
        await print(e)

    userID = interaction.user.id

    try:
        if status == True:
            # add money to the user's account in the database
            await insert_glumbo(userID, glumboAmount)
        else:
            await remove_glumbo(userID, glumboAmount)
    except Exception as e:
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
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await print(e)


@bot.slash_command(name = "slut", description = "erm what the scallop")
@commands.cooldown(1, 900, commands.BucketType.user)
async def slut(interaction: discord.Interaction):
    try:
        glumboAmount = random.randrange(0, 1001)
        status = random.choice([True, False])
    except Exception as e:
        await print(e)

    userID = interaction.user.id

    try:
        if status == True:
            # add money to the user's account in the database
            await insert_glumbo(userID, glumboAmount)
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
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await print(e)

@bot.slash_command(description="Adds money to the user")
async def addmoney(interaction: discord.Interaction, usertogivemoneyto: Optional[discord.Member] = SlashOption(required=True), amountofmoneytogive: Optional[int] = SlashOption(required=True)):
    try:
        if not any(role.name == 'Admin' for role in interaction.user.roles):
            embed = discord.Embed(
            title="Add Money", description=f"You don't have the permission to run this command!", colour=discord.Color.yellow()
        )
            await interaction.response.send_message(embed=embed)
            return
        usertogivemoneyto = usertogivemoneyto.id
        conn = await create_connection("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")
        await insert_glumbo(usertogivemoneyto, amountofmoneytogive)
        await conn.close()
    except Exception as e:
        print(e)

    embed = discord.Embed(
        title="Add Money", description=f"Added <:glumbo:1003615679200645130>{amountofmoneytogive} to the user <@{usertogivemoneyto}>", colour=discord.Color.yellow()
    )
    await interaction.response.send_message(embed=embed) 

@bot.slash_command(description="Mod abuse mod abuse! Removes money from the user")
@commands.cooldown(1, 15, commands.BucketType.user)
async def removemoney(interaction: discord.Interaction, usertoremovemoneyfrom: Optional[discord.Member] = SlashOption(required=True), amountofmoneytoremove: Optional[int] = SlashOption(required=True)):
    try:
        if not any(role.name == 'Admin' for role in interaction.user.roles):
            embed = discord.Embed(
            title="Add Money", description=f"You don't have the permission to run this command!", colour=discord.Color.yellow()
        )
            await interaction.response.send_message(embed=embed)
            return
        data = await remove_glumbo(usertoremovemoneyfrom.id, amountofmoneytoremove)
    except Exception as e:
        print(e)

    if data == "This user doesn't have any money to remove!":
        embed = discord.Embed(
            title="Remove Money", description=f"{data}", colour=discord.Color.yellow()
        ) 

    if data == "This user doesn't exist in the database!":
        embed = discord.Embed(
            title="Remove Money", description=f"{data}", colour=discord.Color.yellow()
        ) 
        
    else:
        embed = discord.Embed(
            title="Remove Money", description=f"Removed <:glumbo:1003615679200645130>{amountofmoneytoremove} from the user {usertoremovemoneyfrom.mention}", colour=discord.Color.yellow()
        )
    await interaction.response.send_message(embed=embed)
    

@bot.slash_command(description="Rob a user! If you fail, you lose your glumbo.")
@commands.cooldown(1, 5400, commands.BucketType.user)
async def rob(interaction: discord.Interaction, usertoremovemoneyfrom: Optional[discord.Member] = SlashOption(required=True)):
    # 40% of robbery success
    status = random.random() < 0.4
    try:
        conn = await create_connection("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")
    except Exception as e:
        await print(e)
 
    try:
        if interaction.user.id == usertoremovemoneyfrom.id:
            embed = discord.Embed(
            title="Rob", description=f"Why would you need to rob yourself?", colour=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        amountOfMoneyStolen = await get_cash_data(conn, usertoremovemoneyfrom.id) * 0.4

        # If the robber got the 40% chance to rob a user
        if status < 0.4:
            # If the user has no money to steal(cash, not bank)
            if amountOfMoneyStolen <= 0.0:
                embed = discord.Embed(
                    title="Rob", description=f"{usertoremovemoneyfrom.mention} does not have any glumbo to rob! Epic fail!", colour=discord.Color.red()
                )
            # Steals the money
            else:
                amountOfMoney = await get_cash_data(conn, usertoremovemoneyfrom.id)
                amountOfMoneyStolen = round(amountOfMoney * 0.4)
                amountOfMoneyStolen = await remove_glumbo(usertoremovemoneyfrom.id, amountOfMoneyStolen)
                embed = discord.Embed(
                title="Rob", description=f"Stole <:glumbo:1003615679200645130>{amountOfMoneyStolen} from the user {usertoremovemoneyfrom.mention}", colour=discord.Color.yellow()
            )
            await interaction.response.send_message(embed=embed)
        # Rip bozo
        else:
            fine = random.randrange(0, 1901)
            amountOfMoneyStolen = await remove_glumbo(interaction.user.id, fine)
            embed = discord.Embed(
                title="Rob", description=f"You tried to rob {usertoremovemoneyfrom.mention}, but you were caught and paid a <:glumbo:1003615679200645130>{fine} fine!", colour=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)

        if amountOfMoneyStolen == "This user doesn't have any money to rob!":
            embed = discord.Embed(
                title="Rob", description=f"{amountOfMoneyStolen}", colour=discord.Color.yellow()
            )
            await interaction.response.send_message(embed=embed)
    except Exception as e:
        await conn.close()
        await print(e)
    finally:
        await conn.close()

@bot.slash_command(name="balance", description="Shows your balance")
@commands.cooldown(1, 10, commands.BucketType.user)
async def balance(interaction: discord.Interaction):
    try:
        conn = await aiosqlite.connect("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")
        userID = interaction.user.id

        # Gets the amount of cash and bank cash the user has
        cash = await get_cash_data(conn, userID)
        bank = await get_bank_data(conn, userID)
    except Exception as e:
        await conn.close()
        await print(e)

    if cash and bank == "You don't have any glumbo!":
        embed = discord.Embed(
        title=f"{interaction.user.name}'s balance", description=f"You don't have any glumbo!", colour=discord.Color.yellow()
    )
    else:
        embed = discord.Embed(
        title=f"{interaction.user.name}'s balance", description=f"Cash: <:glumbo:1003615679200645130>{cash}; Bank: <:glumbo:1003615679200645130>{bank}", colour=discord.Color.yellow()
    )

    await interaction.response.send_message(embed=embed)
    await conn.close()

@bot.slash_command(name="deposit", description="Deposits your money into the bank account")
@commands.cooldown(1, 10, commands.BucketType.user)
async def deposit(interaction: discord.Interaction, glumbotodeposit: Optional[int]):
    try:
        conn = await aiosqlite.connect("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")
        userID = interaction.user.id
        glumbotodeposit = await dep(conn, userID, glumbotodeposit)

        embed = discord.Embed(title="Deposit", description=glumbotodeposit, color=discord.Color.yellow())
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        print(e)


# TODO: make a check if its an integer or "all"
@bot.slash_command(description="Withdraws your money!")
@commands.cooldown(1, 10, commands.BucketType.user)
async def withdraw(interaction: discord.Interaction, glumbotowithdraw: Optional[int] = SlashOption(default=None)):
    try:
        conn = await aiosqlite.connect("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")
        userID = interaction.user.id
        glumbotowithdraw = await withd(conn, userID, glumbotowithdraw)

        embed = discord.Embed(title="Withdraw", description=glumbotowithdraw, color=discord.Color.yellow())
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        await conn.close()
        print(e)

@bot.slash_command(name="shop", description="Opens the shop")
@commands.cooldown(1, 10, commands.BucketType.user)
async def shop(interaction: discord.Interaction):
    try:
        # Connect to the database
        conn = await aiosqlite.connect("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")
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
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await conn.close()
        await print(e)
    

@bot.slash_command(name="additem", description="Adds an item to the shop")
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def additem(interaction: discord.Interaction, itemname: Optional[str] = SlashOption(required=True), price: Optional[int] = SlashOption(required=True), itemdescription: Optional[str] = SlashOption(required=False), message: Optional[str] = SlashOption(required=False, default=None), roleid: Optional[int] = SlashOption(required=False, default=None)):
    try:           
        # Connect to the database
        conn = await aiosqlite.connect("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")
        c = await conn.cursor()

        # Insert the new item into the shop table
        await c.execute("""
        INSERT INTO shop (itemName, itemDescription, price, message, roleID) 
        VALUES (?, ?, ?, ?, ?)
        """, (itemname, itemdescription, price, message, roleid))
        await conn.commit()

        embed = discord.Embed(
            title="Shop", description=f"Item {itemname} has been successfully added to the shop with the price of <:glumbo:1003615679200645130>{price}!", color=discord.colour.Color.yellow()
        )
        await interaction.response.send_message(embed=embed)

        # Close the connection
        await conn.close()
    except Exception as e:
        await conn.close()
        print(e)

@bot.slash_command(name="removeitem", description="Removes an item from the shop")
@commands.cooldown(1, 10, commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def removeitem(interaction = discord.Interaction, itemid: Optional[int] = SlashOption(required=True)):       
    try:           
        # Connect to the database
        conn = await aiosqlite.connect("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")
        c = await conn.cursor()

        # Insert the new item into the shop table
        await c.execute("""
        DELETE FROM userItems WHERE itemID=?
        """, (itemid,))

        await c.execute("""
        DELETE FROM shop WHERE itemID=?
        """, (itemid,))

        await conn.commit()

        embed = discord.Embed(
            title="Shop", description=f"Item {itemid} has been successfully removed from the shop!", color=discord.colour.Color.yellow()
        )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(e)
    finally:
        await conn.close()


@bot.slash_command(description="Use the items you bought from shop!")
@commands.cooldown(1, 10, commands.BucketType.user)
async def use(interaction: discord.Interaction, itemname: Optional[str]):
    try:
        conn = await aiosqlite.connect("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")
        c = await conn.cursor()
        sql = "SELECT roleID, message, itemID FROM shop WHERE itemName = ?"
        await c.execute(sql, (itemname,))
        row = await c.fetchone()
        
        if row is not None:
            role_id, message, itemID = row

            # Check if the user has the item
            sql = "SELECT * FROM userItems WHERE userID = ? AND itemID = ?"
            await c.execute(sql, (interaction.user.id, itemID))
            user_item = await c.fetchone()

            # this looks so fucking complicated, but it works
            # If the user has an item
            if user_item is not None:
                # If the item has a role id to give
                if role_id:
                    role = interaction.guild.get_role(role_id)
                    # If role exists(i guess)
                    if role:
                        # If the user has that role
                        if role in interaction.user.roles:
                            embed = discord.Embed(
                                title="Shop", description="You already have that role!", color=discord.colour.Color.red()
                            )
                        # Adds the role and removes the item
                        else:
                            await interaction.user.add_roles(role)
                            sql = "DELETE FROM userItems WHERE userID = ? AND itemID = ?"
                            await c.execute(sql, (interaction.user.id, itemID))
                            await conn.commit()

                            embed = discord.Embed(
                                title="Shop", description=f"You have been given the {role.name} role.", color=discord.colour.Color.yellow()
                            )
                        await interaction.response.send_message(embed=embed)
                    else:
                        embed = discord.Embed(
                                title="Shop", description="Role not found!", color=discord.colour.Color.red()
                            )
                        await interaction.response.send_message(embed=embed)
                # Else if the item has a message to send when used
                elif message:
                    sql = "DELETE FROM userItems WHERE userID = ? AND itemID = ?"
                    await c.execute(sql, (interaction.user.id, itemID))
                    await conn.commit()
                    await interaction.response.send_message(message)
                # Embed fail
                else:
                    embed = discord.Embed(
                        title="Shop", description="This item does not give any roles or messages!", color=discord.colour.Color.red()
                    )
                    await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(
                    title="Shop", description="You do not have this item.", color=discord.colour.Color.red()
                )
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="Shop", description="Item not found in the shop.", color=discord.colour.Color.red()
            )
            await interaction.response.send_message(embed=embed)

        await conn.close()
    except Exception as e:
        await conn.close()
        print(e)


@bot.slash_command(description="Buy an item from the shop!")
@commands.cooldown(1, 10, commands.BucketType.user)
async def buy(interaction: discord.Interaction, itemname: Optional[str] = SlashOption(required=True)):
    try:

        userID = interaction.user.id

        # Connect to the database
        conn = await aiosqlite.connect("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")
        c = await conn.cursor()

        # Check if the item exists in the shop
        await c.execute("SELECT * FROM shop WHERE itemName = ?", (itemname,))
        item = await c.fetchone()

        # Check if the user has enough money to buy the item

        await c.execute("SELECT cash FROM userData WHERE userID = ?", (userID,))
        cash = (await c.fetchone())[0]
        
        # Get item price

        await c.execute("SELECT price FROM shop WHERE itemName = ?", (itemname,))
        price = (await c.fetchone())[0]

        if cash < price:
            embed = discord.Embed(title="Shop", description="You don't have enough cash to buy this item!", color=discord.Color.yellow())
            await interaction.response.send_message(embed=embed)
        else:
            if item is None:
                await interaction.response.send_message("This item does not exist in the shop.")
            else:
                # If the item exists, insert a new record into the userItems table
                await c.execute("INSERT INTO userItems (userID, itemID) VALUES (?, ?)", (userID, item[0]))
                await c.execute("UPDATE userData SET cash = cash - ? WHERE userID = ?", (price, userID,))
                await conn.commit()
                embed = discord.Embed(title="Shop", description=f"You have successfully bought {itemname}!", color=discord.Color.yellow())
                await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(e)
    finally:
        # Close the connection
        await conn.close()

@bot.slash_command(description="Check your item inventory!")
@commands.cooldown(1, 10, commands.BucketType.user)
async def inventory(interaction: discord.Interaction):
    userID = interaction.user.id

    # Connect to the database
    conn = await aiosqlite.connect("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")
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

        await interaction.response.send_message(embed=embed)
    else:
        # If the user does not own any items, send a message to inform them
        embed = discord.Embed(title="Shop", description=f"You do not own any items!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
    # Close the connection
    await conn.close()


@bot.slash_command(description="Creates a business. Requires 100,000 Glumbo and Amazing Shack role")
@commands.has_role(998911733081067570)
@commands.cooldown(1, 15, commands.BucketType.user)
async def createbusiness(interaction: discord.Interaction, businessname: Optional[str] = SlashOption(required=True), stockname: Optional[str] = SlashOption(required=True), stockprice: Optional[int] = SlashOption(required=False)):
    try:
        stockname = stockname.upper()
        stockprice = int(stockprice) 
        if len(stockname) == 4:
            userID = interaction.user.id
            conn = await aiosqlite.connect("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")
            cash = await get_cash_data(conn, userID) 

            if stockprice > 10001:
                embed = discord.Embed(title="Business", description=f"Your stock price can't be bigger than 10000 glumbo!", color=discord.Color.yellow())
                await interaction.response.send_message(embed=embed)
                return

            if int(cash) >= 100000:
                data = await create_business(conn, userID, businessname, stockname, stockprice)

                if data == "User already has a business.":
                    embed = discord.Embed(title="Business", description=f"{data}", color=discord.Color.yellow())
                    await interaction.response.send_message(embed=embed)
                    return
                elif stockprice > 0:                   
                    await remove_glumbo(userID, 100000)
                    embed = discord.Embed(title="Business", description=f"{data}", color=discord.Color.yellow())
                    await interaction.response.send_message(embed=embed)
                else:
                    embed = discord.Embed(title="Business", description=f"Your stock price can't be 0 or less!", color=discord.Color.red())
                    await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title="Business", description=f"You can't don't have enough glumbo to create a business!", color=discord.Color.red())
                await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="Business", description=f"Your stock name can't be less or greater than 4 characters!", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(e)
    finally:
        await conn.close()
        
@bot.slash_command(description="Shows what stocks are available on the stock market")
@commands.cooldown(1, 10, commands.BucketType.user)
async def stocks(interaction: discord.Interaction):
    try:
        # Connect to the database
        conn = await aiosqlite.connect("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")
        c = await conn.cursor()

        # Query the business table for all items
        await c.execute("SELECT businessName, userID, stockName, stockPrice, stockPercentage FROM business")
        items = await c.fetchall()

        # Create an embed
        embed = discord.Embed(title="Stocks", description="Here are the items available in the stock market:", color=discord.Color.yellow())

        # Add each item to the embed
        for item in items:
            user = await bot.fetch_user(item[1])
            stockChange = item[4]

            if stockChange > 0.0:
                stockChange = f"+{stockChange}"

            embed.add_field(name=f"{item[2]} Company: ({item[0]})", value=f"Price: <:glumbo:1003615679200645130>{item[3]}, Company owner: {user.mention}, Percentage change: {stockChange}%", inline=False)

        # Send the embed
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await print(e)
    finally:
        await conn.close()


@bot.slash_command(description="Buys a stock from the stock market")
@commands.cooldown(1, 15, commands.BucketType.user)
async def buystock(interaction: discord.Interaction, stockname: Optional[str] = SlashOption(required=True), stockamount: Optional[int] = SlashOption(required=True)):
    try:      
       conn = await aiosqlite.connect("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")       
       userID = interaction.user.id
       import cProfile
       data = await buy_stocks(conn, userID, stockname, int(stockamount))
       embed = discord.Embed(title="Stocks", description=data, color=discord.Color.yellow())
       await interaction.response.send_message(embed=embed)

    except Exception as e:
        print(e)

# TODO: IMPLEMENT A CHECK THAT CONVERTS STOCK AMOUNT TO INT, AND IF ITS A STRING AND SAYS ALL, SELL ALL
@bot.slash_command(description="Sells a stock")
@commands.cooldown(1, 15, commands.BucketType.user)
async def sellstock(interaction: discord.Interaction, stockname: Optional[str] = SlashOption(required=True), stockamount: Optional[int] = SlashOption(required=True)):
    try:
        conn = await aiosqlite.connect("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")
        userID = interaction.user.id

        if stockamount.lower() == 'all':
            # Perform the sell operation for all stocks
            data = await sell_stocks(conn, userID, stockname, stockamount)
        elif stockamount.isdigit() and int(stockamount) > 0:
            # Perform the sell operation for the specified quantity
            data = await sell_stocks(conn, userID, stockname, int(stockamount))
        else:
            await interaction.response.send_message("Please provide a valid quantity of stocks to sell.")
            return

        embed = discord.Embed(title="Stocks", description=data, color=discord.Color.yellow())
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        print(e)
        await interaction.response.send_message("An error occurred while processing your request.")

    finally:
        # Close the connection
        if conn and not conn.closed:
            await conn.close()


@bot.slash_command(description="Shows what stocks you have")
@commands.cooldown(1, 10, commands.BucketType.user)
async def stockinventory(interaction: discord.Interaction):
    userID = interaction.user.id

    # Connect to the database
    conn = await aiosqlite.connect("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")
    c = await conn.cursor()

    # Query the userItems table for items owned by the user
    await c.execute("""
    SELECT stockName, quantity
    FROM userStocks  
    WHERE userID = ?
    """, (userID,))
    stocks = await c.fetchall()

    if stocks:
        # If the user owns any items, send a message with the list of items
        stock_list = ', '.join(f"{item[0]} ({item[1]})" for item in stocks)

        embed = discord.Embed(
            title="Inventory", description=f"You own the following stocks: {stock_list}", color=discord.colour.Color.yellow()
        )

        await interaction.response.send_message(embed=embed)
    else:
        # If the user does not own any items, send a message to inform them
        embed = discord.Embed(title="Shop", description=f"You do not own any stocks!", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
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
