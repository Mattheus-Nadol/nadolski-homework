"""
Zadanie 4 – GraphQL (Strawberry) - Query użytkownika

Tworzymy API GraphQL z typem User(id, name, email) i query user(id: ID!)
zwracającym użytkownika z fake listy.
"""

import strawberry
from aiohttp import web
from strawberry.aiohttp.views import GraphQLView

# FAKE BAZA DANYCH
fake_users_db = [
    {"id": 1, "name": "Jan Kowalski", "email": "jan@example.com"},
    {"id": 2, "name": "Anna Nowak", "email": "anna@example.com"},
    {"id": 3, "name": "Piotr Zieliński", "email": "piotr@example.com"},
]

# DEFINICJA TYPU
@strawberry.type
class User:
    id: int
    name: str
    email: str

# QUERY
@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User | None:
        """Zwraca użytkownika o podanym ID"""
        for user in fake_users_db:
            if user["id"] == id:
                return User(**user)
        return None

    @strawberry.field
    def users(self) -> list[User]:
        """Zwraca listę wszystkich użytkowników"""
        return [User(**user) for user in fake_users_db]

# MUTACJE
@strawberry.type
class Mutation:
    @strawberry.mutation
    def createUser(self, name: str, email: str) -> User:
        """
        Dodaje nowego użytkownika do fake_users_db i zwraca go.

        :param name: Imię i nazwisko użytkownika
        :param email: Adres email użytkownika
        :return: Nowo utworzony obiekt User
        """
        new_id = max(user["id"] for user in fake_users_db) + 1 if fake_users_db else 1
        new_user = {"id": new_id, "name": name, "email": email}
        fake_users_db.append(new_user)
        return User(**new_user)

# SCHEMA
schema = strawberry.Schema(query=Query, mutation=Mutation)

# TWORZENIE APLIKACJI
app = web.Application()
app.router.add_route(
    "*",
    "/graphql",
    GraphQLView(schema=schema)  # GraphiQL dla interaktywnego testowania
)

if __name__ == "__main__":
    print("Serwer GraphQL (Strawberry) uruchomiony na http://localhost:8000/graphql")
    web.run_app(app, host="localhost", port=8000)