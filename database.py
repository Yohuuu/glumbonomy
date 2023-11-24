import aiosqlite
from aiosqlite import Error

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
        conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
        c = await conn.cursor()
        await c.execute("""CREATE TABLE userItems (
                            userID BIGINT NOT NULL,
                            itemID INTEGER NOT NULL,
                            FOREIGN KEY (userID) REFERENCES userData(userID),
                            FOREIGN KEY (itemID) REFERENCES shop(itemID)
                            );

                        """)
        await conn.commit()
        await conn.close()
    except Error as e:
        await conn.close()
        print(e)


async def insert_glumbo(conn, username, glumboAmount):
    """
    Insert a new user or update the glumboAmount for an existing user in the userData table
    :param conn:
    :param username:
    :param glumboAmount:
    :return: None
    """
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
    await conn.close()

async def remove_glumbo(conn, username, glumboAmount):
    """
    Insert a new user or update the glumboAmount for an existing user in the userData table
    :param conn:
    :param username:
    :param glumboAmount:
    :return: None
    """
    cur = await conn.cursor()
    
    # Check if the username exists in the database
    await cur.execute(f"SELECT COUNT(*) FROM userData WHERE userID='{username}'")
    user_exists = await cur.fetchone()
    
    if user_exists[0] > 0:
        # If the username exists, update the glumboAmount
        sql = "UPDATE userData SET cash = cash - ? WHERE userID = ?"
        await cur.execute(sql, (glumboAmount, str(username)))
        await conn.commit()
        await conn.close()
        return glumboAmount
    else:
        await conn.close()
        return "This user doesn't have any money to remove!" 
        

async def get_cash_data(conn, userID):
    c = await conn.cursor()
    await c.execute(f"SELECT cash FROM userData WHERE userID = '{userID}'")
    glumbo = await c.fetchone()
    if glumbo == None or glumbo[0] <=0:
        return 0
    else:
        return glumbo[0]
    
async def get_bank_data(conn, username):
    c = await conn.cursor()
    await c.execute(f"SELECT bank FROM userData WHERE userID = '{username}'")
    glumbo = await c.fetchone()
    if glumbo == None:
        return "You don't have any glumbo!"
    else:
        return glumbo[0]


async def dep(conn, userID, glumboToDeposit):
    try:
        c = await conn.cursor()

        # Convert glumboToDeposit to an integer if it's a digit string
        if isinstance(glumboToDeposit, str) and glumboToDeposit.isdigit():
            glumboToDeposit = int(glumboToDeposit)

        # If the user types "all", get all the glumbo in the cash
        if isinstance(glumboToDeposit, str) and glumboToDeposit.lower() == "all":
            glumboToDeposit = await get_cash_data(conn, userID)
            if glumboToDeposit == "You don't have any glumbo!":
                int(glumboToDeposit)
                return  # If get_cash_data returned a string message

        # Check if glumboToDeposit is an integer and greater than 0
        if isinstance(glumboToDeposit, int) and glumboToDeposit > 0:
            # Check if the user has enough glumbo in cash
            glumboInCash = await get_cash_data(conn, userID)
            if isinstance(glumboInCash, str):  # In case get_cash_data returned a string message
                return glumboInCash

            if glumboInCash < glumboToDeposit:
                return "You don't have enough glumbo in your cash!"

            # Transfer the specified amount of glumbo from cash to bank
            sql = "UPDATE userData SET bank = bank + ?, cash = cash - ? WHERE userID = ?"
            await c.execute(sql, (glumboToDeposit, glumboToDeposit, userID))
            await conn.commit()

            return
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
        if isinstance(glumboToWithdraw, str) and glumboToWithdraw.lower() == "all":
            glumboToWithdraw = await get_bank_data(conn, userID)
        elif isinstance(glumboToWithdraw, str) and glumboToWithdraw.isdigit():
            glumboToWithdraw = int(glumboToWithdraw)

        if isinstance(glumboToWithdraw, int) and glumboToWithdraw > 0:
            # Check if the user has enough Glumbos in their Bank account 
            currentBankBalance = await get_bank_data(conn ,userID) 
            if currentBankBalance < glumboToWithdraw:
                return 'You do not have enough Glumbos to withdraw'

            sql = 'UPDATE userData SET bank=bank-?, cash=cash+? WHERE userID=?'
            await c.execute(sql,(glumboToWithdraw,glumboToWithdraw,userID))
            await conn.commit()

            return f"Successfully withdrawn <:glumbol:1003615679200645130> {glumboToWithdraw}!"
        else:
            return "You can't withdraw 0 or less Glumbo"
    except Exception as e:
        print(e)  # Print is not an async function.
        raise e    # It's better to raise exception so that caller can handle it properly.
    finally:
        await conn.close()

    

    




    