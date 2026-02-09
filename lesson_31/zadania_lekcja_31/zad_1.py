import asyncio

# Definicja korutyny za pomocą 'async def'
async def powitanie():
    print("Gotowy do nauki asyncio!")

# Wywołanie funkcji nie uruchamia jej, tylko tworzy obiekt korutyny
korutyna_obj = powitanie()

print("Uruchamiam korutynę...")
asyncio.run(korutyna_obj)