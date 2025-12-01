"""
Endpointy API dla rezerwacji.
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models import db, Booking, Room, User

bookings_bp = Blueprint('bookings', __name__, url_prefix='/api/bookings')


@bookings_bp.route('/', methods=['GET'])
def get_bookings():
    """
    Pobierz listę rezerwacji z filtrami.
    
    Query params:
        room_id: Filtruj po sali
        user_id: Filtruj po użytkowniku
        date: Filtruj po dacie (YYYY-MM-DD)
        status: Filtruj po statusie
    """
    from sqlalchemy.orm import joinedload
    
    query = Booking.query.options(
        joinedload(Booking.room),
        joinedload(Booking.user)
    )
    
    # Filtry
    if room_id := request.args.get('room_id'):
        query = query.filter(Booking.room_id == room_id)
    
    if user_id := request.args.get('user_id'):
        query = query.filter(Booking.user_id == user_id)
    
    if date_str := request.args.get('date'):
        date = datetime.strptime(date_str, '%Y-%m-%d')
        query = query.filter(
            db.func.date(Booking.start_time) == date.date()
        )
    
    if status := request.args.get('status'):
        query = query.filter(Booking.status == status)
    
    # Sortowanie
    query = query.order_by(Booking.start_time.desc())
    
    # Paginacja
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'bookings': [b.to_dict(include_room=True, include_user=True) 
                     for b in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@bookings_bp.route('/', methods=['POST'])
def create_booking():
    """
    Utwórz nową rezerwację.
    
    Body JSON:
        room_id: int
        user_id: int
        title: str
        start_time: str (ISO format)
        end_time: str (ISO format)
        description: str (optional)
        attendees_count: int (optional)
    """
    data = request.get_json()
    
    # Walidacja wymaganych pól
    required = ['room_id', 'user_id', 'title', 'start_time', 'end_time']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Brak wymaganego pola: {field}'}), 400
    
    try:
        start_time = datetime.fromisoformat(data['start_time'])
        end_time = datetime.fromisoformat(data['end_time'])
    except ValueError:
        return jsonify({'error': 'Niepoprawny format daty. Użyj ISO format.'}), 400
    
    # Walidacja logiczna
    if start_time >= end_time:
        return jsonify({'error': 'Czas rozpoczęcia musi być przed czasem zakończenia'}), 400
    
    if start_time < datetime.now():
        return jsonify({'error': 'Nie można rezerwować w przeszłości'}), 400
    
    # Sprawdź czy sala istnieje
    room = Room.query.get(data['room_id'])
    if not room:
        return jsonify({'error': 'Sala nie istnieje'}), 404
    
    if not room.is_active:
        return jsonify({'error': 'Sala jest nieaktywna'}), 400
    
    # Sprawdź czy użytkownik istnieje
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'Użytkownik nie istnieje'}), 404
    
    # Sprawdź dostępność sali
    if not room.is_available(start_time, end_time):
        return jsonify({
            'error': 'Sala jest już zarezerwowana w tym czasie',
            'conflicts': get_conflicts(room.id, start_time, end_time)
        }), 409
    
    # Sprawdź pojemność
    attendees = data.get('attendees_count', 1)
    if attendees > room.capacity:
        return jsonify({
            'error': f'Zbyt wielu uczestników. Pojemność sali: {room.capacity}'
        }), 400
    
    # Utwórz rezerwację
    try:
        booking = Booking(
            room_id=room.id,
            user_id=user.id,
            title=data['title'],
            description=data.get('description'),
            start_time=start_time,
            end_time=end_time,
            attendees_count=attendees
        )
        
        db.session.add(booking)
        db.session.commit()
        
        return jsonify({
            'message': 'Rezerwacja utworzona',
            'booking': booking.to_dict(include_room=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Błąd tworzenia rezerwacji: {str(e)}'}), 500


@bookings_bp.route('/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    """Anuluj rezerwację."""
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.status == 'cancelled':
        return jsonify({'error': 'Rezerwacja już anulowana'}), 400
    
    if booking.start_time < datetime.now():
        return jsonify({'error': 'Nie można anulować przeszłej rezerwacji'}), 400
    
    try:
        booking.status = 'cancelled'
        db.session.commit()
        return jsonify({'message': 'Rezerwacja anulowana'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bookings_bp.route('/available-rooms', methods=['GET'])
def find_available():
    """
    Znajdź dostępne sale.
    
    Query params:
        start_time: str (ISO format)
        end_time: str (ISO format)
        capacity: int (optional)
        equipment: str (comma-separated, optional)
    """
    from app.models import find_available_rooms
    try:
        start_time = datetime.fromisoformat(request.args['start_time'])
        end_time = datetime.fromisoformat(request.args['end_time'])
    except (KeyError, ValueError):
        return jsonify({'error': 'Wymagane: start_time i end_time w formacie ISO'}), 400
    
    capacity = request.args.get('capacity', 1, type=int)
    
    equipment = None
    if eq_param := request.args.get('equipment'):
        equipment = [e.strip() for e in eq_param.split(',')]
    
    rooms = find_available_rooms(start_time, end_time, capacity, equipment)
    
    return jsonify({
        'available_rooms': [r.to_dict() for r in rooms],
        'search_criteria': {
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'min_capacity': capacity,
            'required_equipment': equipment
        }
    })
def get_conflicts(room_id, start_time, end_time):
    """Pomocnicza funkcja zwracająca konfliktujące rezerwacje."""
    conflicts = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.status != 'cancelled',
        Booking.start_time < end_time,
        Booking.end_time > start_time
    ).all()
    
    return [
        {
            'id': b.id,
            'title': b.title,
            'start': b.start_time.isoformat(),
            'end': b.end_time.isoformat()
        }
        for b in conflicts
    ]
