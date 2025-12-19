from django.contrib import admin
from django.conf import settings
from groq import Groq

# Register your models here.
from .models import Entry, Blog, Author, Category  # Importujemy nasz model

 # Rejestrujemy model
admin.site.register(Blog)
admin.site.register(Author)
admin.site.register(Category)

# EntryAdmin zmodyfikowany przy użyciu AI, celem zaimplementowania OpenAI/Groq
@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('headline', 'blog', 'pub_date', 'rating')
    list_filter = ('blog', 'pub_date', 'rating')
    search_fields = ('headline', 'body_text')
    date_hierarchy = 'pub_date'
    filter_horizontal = ('authors', 'category')
    
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('blog', 'headline', 'body_text', 'pub_date', 'mod_date')
        }),
        ('Tłumaczenie i tagi', {
            'fields': ('body_text_en', 'tags'),
            'classes': ('collapse',)
        }),
        ('Relacje', {
            'fields': ('authors', 'category')
        }),
        ('Statystyki', {
            'fields': ('rating', 'number_of_comments', 'number_of_pingbacks'),
            'classes': ('collapse',)
        }),
    )
    
    # Lista akcji AI (niestandardowa implementacja)
    actions = [
        'ai_generate_content',
        'ai_translate_to_english',
        'ai_suggest_tags',
    ]
    
    def _call_groq(self, prompt, max_tokens=1000):
        """Pomocnicza metoda do wywoływania Groq API"""
        try:
            # Sprawdź czy klucz API istnieje
            api_key = getattr(settings, 'GROQ_API_KEY', None)
            if not api_key:
                return "BŁĄD: Brak klucza GROQ_API_KEY w settings.py"
            
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Szybki i darmowy model Groq
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"BŁĄD: {str(e)}"
    
    @admin.action(description="🤖 Wygeneruj treść artykułu na podstawie tytułu")
    def ai_generate_content(self, request, queryset):
        """Generuje treść artykułu używając AI"""
        count = 0
        errors = []
        
        for entry in queryset:
            if not entry.headline:
                errors.append(f"Wpis #{entry.id}: brak tytułu")
                continue
            
            prompt = f"""Napisz angażujący i merytoryczny artykuł na bloga o następującym tytule:

"{entry.headline}"

Wymagania:
- Artykuł powinien mieć około 300-400 słów
- Napisz go w języku polskim
- Użyj profesjonalnego i przystępnego stylu
- Podziel treść na kilka akapitów dla lepszej czytelności
- Zakończ artykuł podsumowaniem lub refleksją

Zwróć tylko samą treść artykułu, bez dodatkowych komentarzy."""
            
            content = self._call_groq(prompt, max_tokens=800)
            
            # Sprawdź czy są błędy
            if content.startswith("BŁĄD"):
                errors.append(f"Wpis '{entry.headline}': {content}")
                continue
            
            # Zapisz wygenerowaną treść
            entry.body_text = content
            entry.save()
            count += 1
        
        # Pokaż komunikat
        if count > 0:
            self.message_user(request, f"✅ Wygenerowano treść dla {count} artykułu/ów!")
        
        if errors:
            for error in errors:
                self.message_user(request, f"❌ {error}", level='error')
    
    @admin.action(description="🌍 Przetłumacz treść na język angielski")
    def ai_translate_to_english(self, request, queryset):
        """Tłumaczy treść artykułu na angielski"""
        count = 0
        errors = []
        
        for entry in queryset:
            if not entry.body_text:
                errors.append(f"Wpis '{entry.headline}': brak treści do tłumaczenia")
                continue
            
            prompt = f"""Przetłumacz poniższy tekst na język angielski.
Zachowaj profesjonalny styl i strukturę akapitów.

Tekst do tłumaczenia:
{entry.body_text}

Zwróć tylko przetłumaczony tekst, bez dodatkowych komentarzy."""
            
            translation = self._call_groq(prompt, max_tokens=1000)
            
            if translation.startswith("BŁĄD"):
                errors.append(f"Wpis '{entry.headline}': {translation}")
                continue
            
            entry.body_text_en = translation
            entry.save()
            count += 1
        
        if count > 0:
            self.message_user(request, f"✅ Przetłumaczono {count} artykuł(ów)!")
        
        if errors:
            for error in errors:
                self.message_user(request, f"❌ {error}", level='error')
    
    @admin.action(description="🏷️ Zasugeruj tagi dla artykułu")
    def ai_suggest_tags(self, request, queryset):
        """Sugeruje tagi używając AI"""
        count = 0
        errors = []
        
        for entry in queryset:
            if not entry.headline or not entry.body_text:
                errors.append(f"Wpis #{entry.id}: brak tytułu lub treści")
                continue
            
            # Ograniczamy treść do 500 znaków aby nie przekroczyć limitu tokenów
            content_preview = entry.body_text[:500] + ("..." if len(entry.body_text) > 500 else "")
            
            prompt = f"""Na podstawie poniższego tytułu i treści artykułu, zasugeruj 5-7 trafnych tagów.

Tytuł: {entry.headline}

Treść: {content_preview}

Wymagania:
- Tagi powinny być w języku polskim
- Zwróć je jako listę oddzieloną przecinkami
- Tagi powinny być jednymi słowami lub krótkim zwrotami (2-3 słowa max)
- Przykład: "technologia, programowanie, sztuczna inteligencja, Django, Python"

Zwróć tylko listę tagów oddzielonych przecinkami, bez dodatkowych wyjaśnień."""
            
            tags = self._call_groq(prompt, max_tokens=100)
            
            if tags.startswith("BŁĄD"):
                errors.append(f"Wpis '{entry.headline}': {tags}")
                continue
            
            entry.tags = tags
            entry.save()
            count += 1
        
        if count > 0:
            self.message_user(request, f"✅ Zasugerowano tagi dla {count} artykułu/ów!")
        
        if errors:
            for error in errors:
                self.message_user(request, f"❌ {error}", level='error')