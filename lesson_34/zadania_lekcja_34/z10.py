

"""
Przykładowe API GraphQL z użyciem Strawberry i aiohttp.

Typy:
- User: id, name, email, posts (lista postów użytkownika)
- Post: id, title, content, author (użytkownik będący autorem)

Baza danych to proste słowniki/fake listy w pamięci.

Instrukcja uruchomienia i testowania:
1. Zainstaluj wymagane pakiety:
   pip install strawberry-graphql aiohttp
2. Uruchom ten plik:
   python z10.py
3. Otwórz przeglądarkę i przejdź do:
   http://localhost:8000/graphql
4. Przykładowe zapytania do GraphiQL:

query {
  users {
    id
    name
    email
    posts {
      id
      title
      content
    }
  }
}

query {
  posts {
    id
    title
    content
    author {
      id
      name
      email
    }
  }
}
"""

import strawberry
from typing import List, Optional
from aiohttp import web
from strawberry.aiohttp.views import GraphQLView

# Fake baza danych - przykładowi użytkownicy i posty
FAKE_USERS = [
    {"id": 1, "name": "Ala", "email": "ala@example.com"},
    {"id": 2, "name": "Bartek", "email": "bartek@example.com"},
]

FAKE_POSTS = [
    {"id": 1, "title": "Pierwszy post", "content": "To jest pierwszy post!", "author_id": 1},
    {"id": 2, "title": "Drugi post", "content": "To jest drugi post!", "author_id": 1},
    {"id": 3, "title": "Post Bartka", "content": "Witajcie!", "author_id": 2},
]


@strawberry.type
class Post:
    """
    Typ reprezentujący post.
    """
    id: int
    title: str
    content: str

    @strawberry.field(description="Autor tego posta")
    def author(self) -> "User":
        # Wyszukaj użytkownika na podstawie author_id
        author_id = None
        for post in FAKE_POSTS:
            if post["id"] == self.id:
                author_id = post["author_id"]
                break
        if author_id is not None:
            user_data = next((u for u in FAKE_USERS if u["id"] == author_id), None)
            if user_data:
                return User(**user_data)
        # Jeśli nie znaleziono, zwróć None (GraphQL zwróci null)
        return None


@strawberry.type
class User:
    """
    Typ reprezentujący użytkownika.
    """
    id: int
    name: str
    email: str

    @strawberry.field(description="Lista postów tego użytkownika")
    def posts(self) -> List[Post]:
        # Zwraca listę postów, których author_id = self.id
        return [
            Post(id=p["id"], title=p["title"], content=p["content"])
            for p in FAKE_POSTS if p["author_id"] == self.id
        ]


@strawberry.type
class Query:
    """
    Główne zapytania GraphQL.
    """
    @strawberry.field(description="Lista wszystkich użytkowników")
    def users(self) -> List[User]:
        return [User(**u) for u in FAKE_USERS]

    @strawberry.field(description="Lista wszystkich postów")
    def posts(self) -> List[Post]:
        return [Post(id=p["id"], title=p["title"], content=p["content"]) for p in FAKE_POSTS]

    @strawberry.field(description="Wyszukaj użytkownika po ID")
    def user_by_id(self, id: int) -> Optional[User]:
        user_data = next((u for u in FAKE_USERS if u["id"] == id), None)
        if user_data:
            return User(**user_data)
        return None

    @strawberry.field(description="Wyszukaj post po ID")
    def post_by_id(self, id: int) -> Optional[Post]:
        post_data = next((p for p in FAKE_POSTS if p["id"] == id), None)
        if post_data:
            return Post(id=post_data["id"], title=post_data["title"], content=post_data["content"])
        return None


schema = strawberry.Schema(query=Query)

# Tworzenie aplikacji aiohttp i dodanie endpointu GraphQL
app = web.Application()
app.router.add_route(
    "GET", "/graphql", GraphQLView(schema=schema)
)
app.router.add_route(
    "POST", "/graphql", GraphQLView(schema=schema)
)

if __name__ == "__main__":
    # Uruchom serwer na localhost:8000
    web.run_app(app, host='localhost', port=8000)