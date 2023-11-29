import pytest
import aiosqlite

@pytest.mark.asyncio()
async def test():
    conn = await aiosqlite.connect("C:/Users/User/Desktop/python/Glumbonomy/test db/glumbo_backup.db")
    glumboToWithdraw = 10
    assert await buy_stocks(conn, 413024747920556061, "GLUG", glumboToWithdraw) == f"You have successfully bought {glumboToWithdraw} GLUM stocks!"
