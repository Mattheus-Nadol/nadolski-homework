"""
Dashboard ze statystykami.
"""
from flask import Blueprint, render_template, jsonify
from datetime import datetime, timedelta
from sqlalchemy import desc, extract
from sqlalchemy.sql import func
from sqlalchemy.orm import joinedload
from app.models import db, Room, Booking, User, get_booking_statistics

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
def dashboard():
    """Strona główna dashboardu."""
    
    # Statystyki ogólne
    stats = {
        'total_rooms': Room.query.filter_by(is_active=True).count(),
        'total_users': User.query.count(),
        'total_bookings': Booking.query.filter_by(status='confirmed').count(),
        'bookings_today': Booking.query.filter(
            func.date(Booking.start_time) == datetime.today().date(),
            Booking.status == 'confirmed'
        ).count()
    }
    
    # Najbliższe rezerwacje (następne 24h)
    now = datetime.now()
    upcoming = Booking.query.options(
        joinedload(Booking.room),
        joinedload(Booking.user)
    ).filter(
        Booking.start_time >= now,
        Booking.start_time <= now + timedelta(hours=24),
        Booking.status == 'confirmed'
    ).order_by(Booking.start_time).limit(10).all()
    
    # Top użytkownicy (najwięcej rezerwacji)
    top_users = db.session.query(
        User.name,
        func.count(Booking.id).label('booking_count')
).join(Booking).filter(
        Booking.status != 'cancelled'
    ).group_by(User.id).order_by(desc('booking_count')).limit(5).all()
    
    # Wykorzystanie sal (% czasu zarezerwowanego w ostatnim miesiącu)
    month_ago = now - timedelta(days=30)
    
    room_utilization = []
    active_rooms = Room.query.filter_by(is_active=True).all()
    
    for room in active_rooms:
        # Suma godzin rezerwacji
        total_hours = db.session.query(
            func.sum(
                extract('epoch', Booking.end_time - Booking.start_time) / 3600
            )
        ).filter(
            Booking.room_id == room.id,
            Booking.start_time >= month_ago,
            Booking.status != 'cancelled'
        ).scalar() or 0
        
        # Maksymalnie 8h dziennie * 22 dni robocze = 176h
        max_hours = 176
        utilization = (total_hours / max_hours) * 100
        
        room_utilization.append({
            'room': room.name,
            'hours': round(total_hours, 1),
            'utilization': round(utilization, 1)
        })
    
    # Sortuj po wykorzystaniu
    room_utilization.sort(key=lambda x: x['utilization'], reverse=True)
    
    return render_template(
        'dashboard.html',
        stats=stats,
        upcoming=upcoming,
        top_users=top_users,
        room_utilization=room_utilization
    )


@dashboard_bp.route('/api/dashboard/stats')
def api_stats():
    """API endpoint dla statystyk (do wykresów JS)."""
    stats = get_booking_statistics()
    return jsonify(stats)
