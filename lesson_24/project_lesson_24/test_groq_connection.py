#!/usr/bin/env python
"""
Skrypt testowy do sprawdzenia połączenia z Groq API
"""

import os
import django

# Konfiguracja Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_websites.settings')
django.setup()

from django.conf import settings
from groq import Groq

print("="*70)
print("  TEST POŁĄCZENIA Z GROQ API")
print("="*70)

# Test 1: Sprawdź czy klucz API istnieje
print("\n1. Sprawdzanie klucza API...")
api_key = getattr(settings, 'GROQ_API_KEY', None)

if not api_key:
    print("❌ BŁĄD: Brak GROQ_API_KEY w settings.py")
    print("\nSprawdź:")
    print("  1. Czy plik .env istnieje?")
    print("  2. Czy w .env jest linia: GROQ_API_KEY=gsk_...")
    print("  3. Zdobądź klucz na: https://console.groq.com/keys")
    exit(1)

# Ukryj większość klucza
masked_key = api_key[:10] + "..." + api_key[-8:]
print(f"✅ Klucz API znaleziony: {masked_key}")

# Test 2: Sprawdź długość klucza
print("\n2. Sprawdzanie formatu klucza...")
if not api_key.startswith('gsk_'):
    print(f"⚠️  UWAGA: Klucz Groq powinien zaczynać się od 'gsk_' (zaczyna się od '{api_key[:5]}')")
else:
    print("✅ Format klucza wygląda poprawnie")

# Test 3: Testuj połączenie z Groq
print("\n3. Testowanie połączenia z Groq API...")
print("   (Groq jest BARDZO szybki - zwykle < 2 sekundy!)")

try:
    client = Groq(api_key=api_key)
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "Odpowiedz jednym słowem: OK"}
        ],
        max_tokens=10
    )
    
    result = response.choices[0].message.content.strip()
    print(f"✅ Połączenie działa! Odpowiedź Groq: '{result}'")
    print(f"   Model: {response.model}")
    print(f"   Użyte tokeny: {response.usage.total_tokens}")
    
except Exception as e:
    print(f"❌ BŁĄD połączenia: {str(e)}")
    print("\nMożliwe przyczyny:")
    print("  1. Nieprawidłowy klucz API")
    print("  2. Problem z połączeniem internetowym")
    print("  3. Klucz API został dezaktywowany")
    print("\nSprawdź:")
    print("  - Klucz na: https://console.groq.com/keys")
    print("  - Dokumentacja: https://console.groq.com/docs")
    exit(1)

# Test 4: Test dłuższego zapytania (jak w rzeczywistej akcji)
print("\n4. Test generowania treści...")
print("   (Groq jest ultra-szybki - zazwyczaj 2-5 sekund!)")

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "Napisz krótki akapit (3 zdania) o sztucznej inteligencji po polsku."}
        ],
        max_tokens=200
    )
    
    result = response.choices[0].message.content.strip()
    print(f"✅ Generowanie treści działa!")
    print(f"\nPrzykładowa wygenerowana treść:")
    print("-" * 70)
    print(result)
    print("-" * 70)
    print(f"\nUżyte tokeny: {response.usage.total_tokens}")
    print(f"💰 Groq często ma darmowy tier!")
    
except Exception as e:
    print(f"❌ BŁĄD: {str(e)}")
    exit(1)

# Podsumowanie
print("\n" + "="*70)
print("  PODSUMOWANIE")
print("="*70)
print("\n✅ Wszystkie testy przeszły pomyślnie!")
print("\n📊 Co to znaczy:")
print("  - Klucz API jest poprawny")
print("  - Połączenie z Groq działa")
print("  - Generowanie treści działa")
print("  - Akcje AI w admin powinny działać!")
print("\n⚡ Zalety Groq:")
print("  - ZNACZNIE szybszy niż OpenAI (5-10x)")
print("  - Często darmowy tier")
print("  - Świetna jakość (llama-3.3-70b)")
print("\n🎯 Następne kroki:")
print("  1. Uruchom serwer: python manage.py runserver")
print("  2. Przejdź do: http://localhost:8000/admin/blog/entry/")
print("  3. Zaznacz wpis z tytułem")
print("  4. Użyj akcji: '🤖 Wygeneruj treść artykułu'")
print("  5. Poczekaj tylko 5-10 sekund (Groq jest szybki!)")
print("  6. Ciesz się wygenerowaną treścią!")
print("\n" + "="*70)

