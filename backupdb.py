import aiosqlite
import asyncio

async def backup_db():
    try:
        while True:
            async with aiosqlite.connect("glumbo.db") as db:
                async with aiosqlite.connect("C:/Users/2008a/OneDrive/Рабочий стол/db backups/glumbo_backup.db") as backup_db:
                    await db.backup(backup_db)
                    print("Backup complete!")
            await asyncio.sleep(600)  # wait for 10 minutes
    except Exception as e:
        print(e)

loop = asyncio.get_event_loop()
loop.run_until_complete(backup_db())
