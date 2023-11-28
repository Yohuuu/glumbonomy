import asyncio
import aiosqlite
import random

async def changeStockPrice():
    try:
        while True:  # This will keep the function running indefinitely
            conn = await aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db")
            c = await conn.cursor()

            # Fetch all stock names, stocks sold and bought
            await c.execute("SELECT stockName, stockPrice, stocksSold, stocksBought FROM business")
            stocks = await c.fetchall()

            # Iterate over each stock and update its price
            for stock in stocks:
                stock_name, stock_price, stocks_sold, stocks_bought = stock

                # Calculate new price based on stocks sold and bought
                random_percentage = random.uniform(-0.1, 0.1)  # A random percentage between -10% and +10%
                random_fluctuation = stock_price * random_percentage
            
                buy_effect = stocks_bought / stock_price
                sell_effect = stocks_sold / stock_price

                new_price = round(max(1, stock_price + random_fluctuation + sell_effect - buy_effect))

                # Update the stock price in the database
                update_query = "UPDATE business SET stockPrice = ? WHERE stockName = ?"
                await c.execute(update_query, (new_price, stock_name))

            # Commit the changes and close the connection
            await conn.commit()
            await conn.close()

            # Wait for 6 minutes (360 seconds) before running again
            await asyncio.sleep(360)
    except Exception as e:
        print(e)
asyncio.run(changeStockPrice())
