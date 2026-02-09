import asyncio
import random

async def ping(host):
    # Symulacja ping
    czas = random.uniform(0.1, 1.0)
    await asyncio.sleep(czas)
    return f"Host {host} odpowiada w czasie {czas:.2f} sek."

async def main():
    hosty = [
    "alpha.example.com",
    "beta.testserver.net",
    "gamma.localhost",
    "delta.example.org",
    "epsilon.devserver.io"
    ]
    pingowanie = [ping(x) for x in hosty]
    wynik = await asyncio.gather(*pingowanie)

    for i in wynik:
        print(i)

asyncio.run(main())