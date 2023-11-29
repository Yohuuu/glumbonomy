import random
import aiosqlite
import asyncio

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

                # Fetch the total quantity of this stock owned by all users
                await c.execute("SELECT SUM(quantity) FROM userStocks WHERE stockName = ?", (stock_name,))
                total_quantity = await c.fetchone()
                total_quantity = total_quantity[0] if total_quantity[0] is not None else 0

                # Calculate new price based on stocks sold, bought and total quantity
                random_percentage = random.uniform(-0.03, 0.03)  # A random percentage between -3% and +3%             
                random_fluctuation = stock_price * random_percentage
            
                buy_effect = stocks_bought * random_percentage
                sell_effect = stocks_sold / random_percentage if random_percentage != 0 else 0
                quantity_effect = total_quantity * random_percentage

                new_price = round(max(1, stock_price + random_fluctuation - sell_effect + buy_effect + quantity_effect))

                stockPercentage = ((new_price - stock_price) / stock_price) * 100
                formatted_stockPercentage = "{:.2f}".format(stockPercentage)
                update_query = "UPDATE business SET stockPercentage = ? WHERE stockName = ?"
                await c.execute(update_query, (formatted_stockPercentage, stock_name))

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
