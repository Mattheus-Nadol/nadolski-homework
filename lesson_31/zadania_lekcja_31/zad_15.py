import asyncio
import aiofiles

async def logowanie(lock, nr_korutyny, ilosc_wpisow=5):
    for i in range(1, ilosc_wpisow + 1):
        async with lock:  # tylko jedna korutyna może pisać do pliku w tym momencie
            async with aiofiles.open("log_zad_15.txt", "a") as f:
                await f.write(f"Log z korutyny {nr_korutyny}, wpis {i}\n")
        await asyncio.sleep(0.1)  # symulacja pracy korutyny

async def main():
    lock = asyncio.Lock()  # tworzymy lock do synchronizacji zapisu
    korutyny = [asyncio.create_task(logowanie(lock, i+1)) for i in range(5)]

    await asyncio.gather(*korutyny)
    print(f"Zapisano do pliku log_zad_15.txt")

asyncio.run(main())