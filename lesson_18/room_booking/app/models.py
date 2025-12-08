"""
Modele bazy danych dla systemu rezerwacji sal.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, extract
from sqlalchemy.orm import joinedload

db = SQLAlchemy()


# TABELA ŁĄCZĄCA: Sale i Wyposażenie (M:N)
room_equipment = db.Table(
    'room_equipment',
    db.Column('room_id', db.Integer, db.ForeignKey('rooms.id'), 
primary_key=True),
    db.Column('equipment_id', db.Integer, db.ForeignKey('equipment.id'), 
primary_key=True)
)


class User(db.Model):
    """Model użytkownika systemu."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacja 1:N z rezerwacjami
    bookings = db.relationship('Booking', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'department': self.department,
            'is_admin': self.is_admin
        }


class Equipment(db.Model):
    """Model wyposażenia sali (projektor, tablica, wideokonferencja 
itp.)."""
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    icon = db.Column(db.String(50))  # np. "projector", "whiteboard"
    
    def __repr__(self):
        return f'<Equipment {self.name}>'


class Room(db.Model):
    """Model sali konferencyjnej."""
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    hourly_rate = db.Column(db.Numeric(10, 2), default=0)  # Koszt za godzinę
    
    # Relacja 1:N z rezerwacjami
    bookings = db.relationship('Booking', backref='room', lazy='dynamic',
                               cascade='all, delete-orphan')
    
    # Relacja M:N z wyposażeniem
    equipment = db.relationship(
        'Equipment',
        secondary=room_equipment,
        lazy='subquery',
        backref=db.backref('rooms', lazy=True)
    )
    
    def __repr__(self):
        return f'<Room {self.name} (cap: {self.capacity})>'
    
    def to_dict(self, include_equipment=True):
        data = {
            'id': self.id,
            'name': self.name,
            'capacity': self.capacity,
            'floor': self.floor,
            'description': self.description,
            'is_active': self.is_active,
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate else 0
        }
        if include_equipment:
            data['equipment'] = [e.name for e in self.equipment]
        return data
    
    def is_available(self, start_time, end_time, exclude_booking_id=None):
        """
        Sprawdza, czy sala jest dostępna w podanym przedziale czasowym.
        
        Args:
            start_time: Początek rezerwacji (datetime)
            end_time: Koniec rezerwacji (datetime)
            exclude_booking_id: ID rezerwacji do pominięcia (przy edycji)
        
        Returns:
            bool: True jeśli sala jest dostępna
        """
        query = Booking.query.filter(
            Booking.room_id == self.id,
            Booking.status != 'cancelled',
            # Sprawdzenie nakładania się przedziałów czasowych
            Booking.start_time < end_time,
            Booking.end_time > start_time
        )
        
        if exclude_booking_id:
            query = query.filter(Booking.id != exclude_booking_id)
        
        return query.count() == 0


class Booking(db.Model):
    """Model rezerwacji sali."""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    
    status = db.Column(
        db.String(20), 
        default='confirmed',
        nullable=False
    )  # confirmed, cancelled, completed
    
    attendees_count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,onupdate=datetime.utcnow)
    
    # Indeks dla szybkiego wyszukiwania
    __table_args__ = (
        db.Index('idx_booking_room_time', 'room_id', 'start_time', 'end_time'),
    )
    
    def __repr__(self):
        return f'<Booking {self.title} ({self.start_time})>'
    
    @property
    def duration_hours(self):
        """Czas trwania rezerwacji w godzinach."""
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 3600
    
    @property
    def total_cost(self):
        """Całkowity koszt rezerwacji."""
        if self.room and self.room.hourly_rate:
            return float(self.room.hourly_rate) * self.duration_hours
        return 0
    
    def to_dict(self, include_room=False, include_user=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'status': self.status,
            'attendees_count': self.attendees_count,
            'duration_hours': round(self.duration_hours, 2),
            'total_cost': round(self.total_cost, 2)
        }
        if include_room:
            data['room'] = self.room.to_dict(include_equipment=False)
        if include_user:
            data['user'] = self.user.to_dict()
        return data

# --- FUNKCJE POMOCNICZE ---

def find_available_rooms(start_time, end_time, min_capacity=1,
                         required_equipment=None):
    """
    Znajdź dostępne sale spełniające kryteria.
    
    Args:
        start_time: Początek (datetime)
        end_time: Koniec (datetime)
        min_capacity: Minimalna pojemność
        required_equipment: Lista nazw wymaganego wyposażenia
    
    Returns:
        Lista dostępnych sal
    """

    
    # Podstawowe zapytanie z eager loading
    query = Room.query.options(
        joinedload(Room.equipment)
    ).filter(
        Room.is_active == True,
        Room.capacity >= min_capacity
    )
    
    # Filtruj po wyposażeniu
    if required_equipment:
        for eq_name in required_equipment:
            query = query.filter(
                Room.equipment.any(Equipment.name == eq_name)
            )
    
    # Pobierz kandydatów
    candidate_rooms = query.all()
    
    # Sprawdź dostępność każdej sali
    available = []
    for room in candidate_rooms:
        if room.is_available(start_time, end_time):
            available.append(room)
    
    return available
def get_booking_statistics(start_date=None, end_date=None):
    """
    Pobierz statystyki rezerwacji.
    
    Returns:
        dict: Słownik ze statystykami
    """
    
    base_query = db.session.query(Booking).filter(
        Booking.status != 'cancelled'
    )
    
    if start_date:
        base_query = base_query.filter(Booking.start_time >= start_date)
    if end_date:
        base_query = base_query.filter(Booking.end_time <= end_date)
    
    # Ogólne statystyki
    total_bookings = base_query.count()

    # Statystyki per sala
    room_stats = db.session.query(
        Room.name,
        func.count(Booking.id).label('booking_count'),
        func.sum(
            extract('epoch', Booking.end_time - Booking.start_time) / 3600
        ).label('total_hours')
    ).join(Booking).filter(
        Booking.status != 'cancelled'
    ).group_by(Room.name).all()
    
    # Statystyki per dzień tygodnia
    weekday_stats = db.session.query(
        extract('dow', Booking.start_time).label('weekday'),
        func.count(Booking.id).label('count')
    ).filter(
        Booking.status != 'cancelled'
    ).group_by('weekday').order_by('weekday').all()
    
    weekdays = ['Nd', 'Pn', 'Wt', 'Śr', 'Cz', 'Pt', 'Sb']
    
    return {
        'total_bookings': total_bookings,
        'room_stats': [
            {
                'room': r.name,
                'bookings': r.booking_count,
                'hours': round(float(r.total_hours or 0), 1)
            }
            for r in room_stats
        ],
        'weekday_stats': [
            {
                'day': weekdays[int(w.weekday)],
                'count': w.count
            }
            for w in weekday_stats
        ]
    }
