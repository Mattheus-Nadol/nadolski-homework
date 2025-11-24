from app import db, app, User
# SQLAlchemy potrzebuje kontekstu aplikacji Flask
with app.app_context():
    db.create_all()
    u1 = User(username="alice", email="alice@example.com")
    u2 = User(username="bob", email="bob@example.com")
    db.session.add_all([u1, u2])
    db.session.commit()