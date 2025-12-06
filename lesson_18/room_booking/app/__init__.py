
"""
Fabryka aplikacji Flask dla systemu rezerwacji sal.
"""
from flask import Flask, render_template
from config import config
from app.models import db
from sqlalchemy.orm import joinedload

# Import blueprints
from app.routes.bookings import bookings_bp
from app.routes.dashboard import dashboard_bp


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    # Rejestracja blueprintów
    app.register_blueprint(bookings_bp)
    app.register_blueprint(dashboard_bp)

    # ✅ Dodaj trasę główną
    
    @app.route('/')
    def home():
        return render_template('home.html')
    

    @app.route('/rooms')
    def rooms():
        from app.models import Room
        rooms = Room.query.all()
        return render_template('rooms.html', rooms=rooms)
    
    @app.route('/bookings')
    def bookings():
        from app.models import Booking
        bookings = Booking.query.options(
            joinedload(Booking.room),
            joinedload(Booking.user)
        ).all()
        return render_template('bookings.html', bookings=bookings)

    
    return app


    # NOTE: If you prefer to set cache headers for development, you can
    # register an `after_request` handler here. Example (uncomment to enable):
    #
    # @app.after_request
    # def add_no_cache_headers(response):
    #     response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    #     response.headers['Pragma'] = 'no-cache'
    #     response.headers['Expires'] = '0'
    #     return response


