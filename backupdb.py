import aiosqlite
import asyncio

async def backup_db():
    while True:
        async with aiosqlite.connect("C:/Users/User/Desktop/python/glumbo.db") as db:
            async with aiosqlite.connect("C:/Users/User/Desktop/db backups/glumbo_backup.db") as backup_db:
                await db.backup(backup_db)
                print("Backup complete!")
        await asyncio.sleep(600)  # wait for 10 minutes

loop = asyncio.get_event_loop()
loop.run_until_complete(backup_db())
