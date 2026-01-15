from django.core.cache import cache
import time
from random import randint


def get_very_complex_calculation_result():
    # Definiujemy unikalny klucz dla naszego cache
    cache_key = 'complex_calculation'
    
    # Próbujemy pobrać dane z cache
    result = cache.get(cache_key)
    # Jeśli danych nie ma w cache (cache miss)
    if result is None:
        # Wykonujemy "drogą" operację
        print("Wykonuję skomplikowane obliczenia...")
        time.sleep(5) # Symulacja długiej operacji
        result = {"data": 67, "source": "Obliczone na żywo"}
        
        # Zapisujemy wynik do cache na 1 godzinę (3600 sekund)
        cache.set(cache_key, result, timeout=3600)
    else:
        print("Zwracam wynik z cache!")
        result['source'] = 'Pobrane z cache'
        
    return result

# (27) Zadanie 7 (ulepszone podczas lekcji 28)
def get_complex_query():
    cache_key = 'complex_query'

    result = cache.get(cache_key)

    if result is None:
        # Wykonujemy "drogą" operację
        print("Wykonuję kompleksowe query...")
        time.sleep(3) # Symulacja długiej operacji
        print('Ufff, skończyłem')
        result = {"data": randint(1, 50), "source": "Query kompleksowe"}
        
        # Zapisujemy wynik do cache na 1 godzinę (90 sekund)
        cache.set(cache_key, result, timeout=90)
    else:
        print("Zwracam wynik z complex cache!")
        result['source'] = 'Pobrane z complex cache'
        
    return result