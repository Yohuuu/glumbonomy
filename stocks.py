import random
import aiosqlite
import asyncio

async def changeStockPrice():
    try:
        while True:  # This will keep the function running indefinitely
            conn = await aiosqlite.connect("C:/Users/2008a/OneDrive/Рабочий стол/python/glumbo.db")
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
                if total_quantity < 10:  # not a lot of stocks bought
                    random_percentage = random.uniform(-0.05, 0.05)  # A random percentage between -5% and +5%
                elif stocks_bought > stocks_sold:  # demand is high
                    random_percentage = random.uniform(0.01, 0.1)  # A random percentage between 0% and +3%
                else:  # supply is high
                    random_percentage = random.uniform(-0.05, 0)  # A random percentage between -5% and 0%
                
                random_fluctuation = random.uniform(-30, 30)  # A random value between -3 and +3 glumbo
            
                buy_effect = min(stocks_bought * random_percentage, stock_price * 0.1)
                sell_effect = min(stocks_sold / random_percentage if random_percentage != 0 else 0, stock_price * 0.05)
                quantity_effect = min(total_quantity * random_percentage, stock_price * 0.1)

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
