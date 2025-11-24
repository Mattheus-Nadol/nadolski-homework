# Zasób na serwerze pod adresem /users/1:
source = {
    "name": "Katarzyna",
    "email": "k.nowak@example.com",
    "city": "Warszawa"
    }

# Zmiana "name" na "Kasia":

# PUT – pełna aktualizacja zasobu; zastępuje cały obiekt nową wersją.
# Nawet jeśli zmieniamy tylko jedno pole, musimy wysłać CAŁY obiekt.
put_request_body = {
    "name": "Kasia",
    "email": "k.nowak@example.com",
    "city": "Warszawa"
}

# PATCH – częściowa aktualizacja zasobu; aktualizuje tylko wskazane pola.
# Wysyłamy tylko to, co się zmienia – w tym przypadku pole "name".
patch_request_body = {
    "name": "Kasia"
}

# Różnice:
# - PUT wymaga przesłania całego obiektu, co jest mniej efektywne,
#   szczególnie gdy obiekt ma wiele pól.
# - PATCH jest bardziej "oszczędny", bo przesyła tylko zmienione dane.
