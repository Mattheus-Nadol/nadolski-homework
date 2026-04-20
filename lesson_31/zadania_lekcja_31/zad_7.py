import asyncio
import random

async def pobierz_pogode(miasto):
    await asyncio.sleep(1.5)
    temperatura = random.uniform(-4, 26)
    stan = random.choice(["słonecznie", "deszczowo", "burze", "tornado"])
    return {
        "miasto": miasto,
        "temperatura": round(temperatura, 2),
        "stan": stan
        }

async def main():
    miasta = ["Warszawa", "Kraków", "Gdańsk"]
    pogoda = [pobierz_pogode(x) for x in miasta]
    wynik = await asyncio.gather(*pogoda)
    
    for prognoza in wynik:
        print("Pogoda", prognoza)

asyncio.run(main())