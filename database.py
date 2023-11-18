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
        print(e)

    return conn


async def create_table(create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
        c = conn.cursor()
        await c.execute(""" CREATE TABLE userData (
                                username VARCHAR2(32) PRIMARY KEY NOT NULL,
                                glumboAmount integer DEFAULT 0
                            );


                        """)
    except Error as e:
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
    await cur.execute(f"SELECT COUNT(*) FROM userData WHERE username='{username}'")
    user_exists = await cur.fetchone()
    
    if user_exists[0] > 0:
        # If the username exists, update the glumboAmount
        sql = f'''UPDATE userData SET glumboAmount = glumboAmount + {glumboAmount} WHERE username = '{username}' '''
    else:
        # If the username does not exist, insert a new user
        sql = f'''INSERT INTO userData(username, glumboAmount) VALUES('{username}', {glumboAmount})'''
    
    await cur.execute(sql)
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
    await cur.execute(f"SELECT COUNT(*) FROM userData WHERE username='{username}'")
    user_exists = await cur.fetchone()
    
    if user_exists[0] > 0:
        # If the username exists, update the glumboAmount
        sql = f'''UPDATE userData SET glumboAmount = glumboAmount - {glumboAmount} WHERE username = '{username}' '''
        await cur.execute(sql)
        await conn.commit()
        return f"Removed {glumboAmount} glumbo from {username}"
    else:
        return "This user doesn't have any money to remove!"  
    await conn.close()

async def get_glumbo_data(username):
    # create a database connection
    conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
    c = await conn.cursor()
    await c.execute(f"SELECT glumboAmount FROM userData WHERE username = '{username}'")
    glumbo = await c.fetchone()
    # close the connection
    await conn.close()
    # return the fetched data
    if glumbo == None:
        return "You don't have any glumbo!"
    else:
        return glumbo[0] 