import aiosqlite
from aiosqlite import Error

database = "C:/Users/2008a/OneDrive/Рабочий стол/python/Glumbonomy/glumbonomy/glumbo.db"

async def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = await aiosqlite.connect(db_file)
        return conn
    except Error as e:
        if conn:
            await conn.close()
        print(e)

async def create_table():
    try:
        conn = await aiosqlite.connect(database)
        c = await conn.cursor()
        await c.execute("""CREATE TABLE userStocks (
                            userID BIGINT NOT NULL,
                            stockName TEXT NOT NULL,
                            FOREIGN KEY (userID) REFERENCES userData(userID),
                            FOREIGN KEY (stockName) REFERENCES business(stockName)
                        );
                        """)
        await conn.commit()
        await conn.close()
    except Error as e:
        await conn.close()
        print(e)


async def insert_glumbo(username, glumboAmount):
    try:
        conn = await create_connection(database)

        cur = await conn.cursor()
        
        # Check if the username exists in the database
        await cur.execute(f"SELECT COUNT(*) FROM userData WHERE userID=?", (username,))
        user_exists = await cur.fetchone()
        
        if user_exists[0] > 0:
            # If the username exists, update the glumboAmount
            sql = 'UPDATE userData SET cash = cash + ? WHERE userID = ?'
            await cur.execute(sql, (glumboAmount, username))
        else:
            # If the username does not exist, insert a new user
            sql = 'INSERT INTO userData(userID, cash) VALUES(?, ?)'
            await cur.execute(sql, (username, glumboAmount))
        
        await conn.commit()
    except Exception as e:
        print(e)
    finally:
        await conn.close()

async def remove_glumbo(username, glumboAmount):
    """
    Insert a new user or update the glumboAmount for an existing user in the userData table
    :param conn:
    :param username:
    :param glumboAmount:
    :return: None
    """
    try:
        conn = await aiosqlite.connect(database)
        cur = await conn.cursor()
        
        # Check if the username exists in the database
        await cur.execute(f"SELECT COUNT(*) FROM userData WHERE userID='{username}'")
        user_exists = await cur.fetchone()
        
        if user_exists[0] > 0:
            # If the username exists, check if they have enough glumbo
            await cur.execute(f"SELECT cash FROM userData WHERE userID='{username}'")
            user_cash = await cur.fetchone()
            
            # If the user has enough glumbo, update the glumboAmount
            sql = "UPDATE userData SET cash = cash - ? WHERE userID = ?"
            await cur.execute(sql, (int(glumboAmount), username))
            await conn.commit()
        else:
            return "This user doesn't exist in the database!" 
    except Exception as e:
        print(e)
    finally:
        await conn.close()


async def get_cash_data(conn, userID):
    c = await conn.cursor()
    await c.execute(f"SELECT cash FROM userData WHERE userID = '{userID}'")
    glumbo = await c.fetchone()
    if glumbo == None:
        return 0
    else:
        return int(glumbo[0])

    
async def get_bank_data(conn, username):
    c = await conn.cursor()
    await c.execute(f"SELECT bank FROM userData WHERE userID = '{username}'")
    glumbo = await c.fetchone()
    if glumbo == None:
        return 0
    else:
        return int(glumbo[0])


async def dep(conn, userID, glumboToDeposit):
    try:
        c = await conn.cursor()

        # Convert glumboToDeposit to an integer if it's a digit string
        if isinstance(glumboToDeposit, str) and glumboToDeposit.isdigit():
            glumboToDeposit = int(glumboToDeposit)

        # If the user types "all", get all the glumbo in the cash
        if glumboToDeposit == None:
            glumboToDeposit = await get_cash_data(conn, userID)

        # Check if glumboToDeposit is an integer and greater than 0
        if isinstance(glumboToDeposit, int) and glumboToDeposit > 0:
            # Check if the user has enough glumbo in cash
            glumboInCash = await get_cash_data(conn, userID)
            if glumboInCash < glumboToDeposit:
                return "You don't have enough glumbo in your cash!"

            # Transfer the specified amount of glumbo from cash to bank
            sql = "UPDATE userData SET bank = bank + ?, cash = cash - ? WHERE userID = ?"
            await c.execute(sql, (glumboToDeposit, glumboToDeposit, userID))
            await conn.commit()

            return f"You have successfully deposited <:glumbo:1003615679200645130>{glumboToDeposit}!"
        else:
            return "You can't deposit 0 or less glumbo!"
    except Exception as e:
        print(e)  # Print is not an async function.
        raise e    # It's better to raise exception so that caller can handle it properly.
    finally:
        await conn.close()
        
async def withd(conn, userID, glumboToWithdraw):
    try:
        c = await conn.cursor()

        # If the user types "all", get all the glumbo in the bank
        if glumboToWithdraw == None:
            glumboToWithdraw = await get_bank_data(conn, userID)
        else:
            glumboToWithdraw = int(glumboToWithdraw)

        if isinstance(glumboToWithdraw, int) and glumboToWithdraw > 0:
            # Check if the user has enough Glumbos in their Bank account 
            currentBankBalance = await get_bank_data(conn ,userID) 
            if currentBankBalance < glumboToWithdraw:
                return 'You do not have enough Glumbos to withdraw'

            sql = 'UPDATE userData SET bank=bank-?, cash=cash+? WHERE userID=?'
            await c.execute(sql,(glumboToWithdraw,glumboToWithdraw,userID))
            await conn.commit()

            return f"Successfully withdrawn <:glumbol:1003615679200645130>{glumboToWithdraw}!"
        else:
            return "You can't withdraw 0 or less Glumbo"
    except Exception as e:
        print(e)  # Print is not an async function.
        raise e    # It's better to raise exception so that caller can handle it properly.
    finally:
        await conn.close()

async def create_business(conn, userID, businessName, stockName, stockPrice):
    try:
        c = await conn.cursor()
        checkIfUserHasOtherBusinesses = "SELECT businessID FROM business WHERE userID = ?"
        await c.execute(checkIfUserHasOtherBusinesses, (userID,))
        result = await c.fetchone()

        if result is not None:
            return "User already has a business."
        
        # Add your business creation code here
        createBusiness = "INSERT INTO business(businessName, stockName, stockPrice, userID) VALUES(?, ?, ?, ?)"
        await c.execute(createBusiness, (businessName, stockName, stockPrice, userID,))
        await conn.commit()
        return f"Business {businessName} was created!"
    except Exception as e:
        print(e)
    finally:
        await conn.close()

async def buy_stocks(conn, userID, stockName, stockAmount):
    try:
        if stockAmount is None:
            return "You must specify the amount of stock to buy!"
        c = await conn.cursor()

        # Check if the item exists in the shop
        await c.execute("SELECT * FROM business WHERE stockName = ?", (stockName,))
        item = await c.fetchone()

        if item is None:
                return "This stock does not exist."

        # Check if the user has enough money to buy the item
        await c.execute("SELECT cash FROM userData WHERE userID = ?", (userID,))
        cash = (await c.fetchone())[0]
        
        # Get item price
        await c.execute("SELECT stockPrice FROM business WHERE stockName = ?", (stockName,))
        price = (await c.fetchone())[0]

        total_price = price * stockAmount

        if cash < total_price:
            return "You don't have enough cash to buy this stock!"
        else:            
                # Check if the user already owns this stock
                await c.execute("SELECT * FROM userStocks WHERE userID = ? AND stockName = ?", (userID, stockName))
                user_stock = await c.fetchone()

                if user_stock is None:
                    # If the user doesn't own this stock, insert a new record into the userStocks table
                    await c.execute("INSERT INTO userStocks (userID, stockName, quantity) VALUES (?, ?, ?)", (userID, stockName, stockAmount))
                else:
                    # If the user already owns this stock, increment the quantity
                    await c.execute("UPDATE userStocks SET quantity = quantity + ? WHERE userID = ? AND stockName = ?", (stockAmount, userID, stockName))

                await c.execute("UPDATE business SET stocksBought = stocksBought + ? WHERE stockName = ?", (stockAmount, stockName,))
                
                stocksSold = "SELECT stocksSold FROM business WHERE stockName = ?"
                await c.execute(stocksSold, (stockName,))
                stocksSold = (await c.fetchone())[0]

                if stocksSold - stockAmount <=0:
                    stocksSold = 0
                else:
                    stocksSold = stocksSold - stockAmount

                await c.execute("UPDATE business SET stocksSold = ? WHERE stockName = ?", (stocksSold, stockName,))
                await c.execute("UPDATE userData SET cash = cash - ? WHERE userID = ?", (total_price, userID,))
                await conn.commit()
                return f"You have successfully bought {stockAmount} {stockName} stocks!"
    except Exception as e:
        print(e)
    finally:
        await conn.close()

async def sell_stocks(conn, userID, stockName, stockAmount):
    try:
        c = await conn.cursor()

        # Check if the item exists in the shop
        await c.execute("SELECT * FROM business WHERE stockName = ?", (stockName,))
        item = await c.fetchone()
        if item is None:
                return "This stock does not exist."

        # Check if the user owns the item
        sql = "SELECT * FROM userStocks WHERE userID = ? AND stockName = ?"
        await c.execute(sql, (userID, stockName))
        user_item = await c.fetchone()

        if user_item is None or 0:
            return "You don't own this stock!"

        if user_item is not None:
            await c.execute("SELECT stockPrice FROM business WHERE stockName = ?", (stockName,))
            price = (await c.fetchone())[0]

            # If the user wants to sell all their stocks
            if stockAmount == 'all':
                stockAmount = user_item[2]  # Convert to int here
            else:
                stockAmount = int(stockAmount)  # Convert stockAmount to an integer
            if stockAmount > user_item[2]:
                return "You don't have enough stocks to sell!"
                

            # If the user sells all their stocks, delete the record from the userStocks table
            if stockAmount == user_item[2]:
                await c.execute("DELETE FROM userStocks WHERE userID = ? AND stockName = ?", (userID, stockName))
                await c.execute("UPDATE business SET stocksSold = stocksSold + ? WHERE stockName = ?", (stockAmount, stockName,))
                await c.execute("UPDATE userData SET cash = cash + ? WHERE userID = ?", (price * stockAmount, userID,))
                await conn.commit()
                return f"You have successfully sold {stockAmount} of {stockName} for {price * stockAmount}!"
            else:
                # If the user sells some of their stocks, update the record in the userStocks table
                await c.execute("UPDATE userStocks SET quantity = quantity - ? WHERE userID = ? AND stockName = ?", (stockAmount, userID, stockName))
                
                #Calculate the new number of sold stocks
                
                await c.execute("UPDATE business SET stocksSold = stocksSold + ? WHERE stockName = ?", (stockAmount, stockName,))
                await c.execute("UPDATE userData SET cash = cash + ? WHERE userID = ?", (price * stockAmount, userID,))
                await conn.commit()
                return f"You have successfully sold {stockAmount} of {stockName} for {price * stockAmount}!"
        else:
            return "You don't own this stock!"
    except Exception as e:
        print(e)
    finally:
        await conn.close()

async def addItemDB(itemname, itemdescription, price, message, roleid):
    try:         
        conn = await aiosqlite.connect(database)
        c = await conn.cursor()

        # Insert the new item into the shop table
        await c.execute("""
        INSERT INTO shop (itemName, itemDescription, price, message, roleID) 
        VALUES (?, ?, ?, ?, ?)
        """, (itemname, itemdescription, price, message, roleid))
        await conn.commit()
    except Exception as e:
        print(e)
    finally:
        await conn.close()

async def removeItemDB(itemid):
    try:           
        # Connect to the database
        conn = await aiosqlite.connect(database)
        c = await conn.cursor()

        # Insert the new item into the shop table
        await c.execute("""
        DELETE FROM userItems WHERE itemID=?
        """, (itemid,))

        await c.execute("""
        DELETE FROM shop WHERE itemID=?
        """, (itemid,))

        await conn.commit()
    except Exception as e:
        print(e)
    finally:
        await conn.close()