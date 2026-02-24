from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    full_name = db.Column(db.String(255), nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

class Bus(db.Model):
    __tablename__ = 'buses'
    
    id = db.Column(db.Integer, primary_key=True)
    bus_number = db.Column(db.String(50), unique=True, nullable=False)
    registration_number = db.Column(db.String(50), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    bus_type = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

class Route(db.Model):
    __tablename__ = 'routes'
    
    id = db.Column(db.Integer, primary_key=True)
    route_number = db.Column(db.String(50), unique=True, nullable=False)
    route_name = db.Column(db.String(255), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'))
    start_location = db.Column(db.String(255), nullable=False)
    end_location = db.Column(db.String(255), nullable=False)
    distance_km = db.Column(db.Numeric(5, 2))
    estimated_duration_minutes = db.Column(db.Integer)
    fare = db.Column(db.Numeric(10, 2), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'))
    booking_reference = db.Column(db.String(50), unique=True, nullable=False)
    passenger_name = db.Column(db.String(255), nullable=False)
    passenger_category = db.Column(db.String(50))
    seat_number = db.Column(db.String(10))
    journey_date = db.Column(db.DateTime, nullable=False)
    fare_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20))
    qr_code = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'))
    payment_method = db.Column(db.String(50), nullable=False)
    transaction_id = db.Column(db.String(100))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20))
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LiveBusLocation(db.Model):
    __tablename__ = 'live_bus_locations'
    
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'))
    latitude = db.Column(db.Numeric(9, 6), nullable=False)
    longitude = db.Column(db.Numeric(9, 6), nullable=False)
    speed = db.Column(db.Numeric(5, 2))
    heading = db.Column(db.Numeric(5, 2))
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class Wallet(db.Model):
    __tablename__ = 'wallets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    balance = db.Column(db.Numeric(10, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

class Stop(db.Model):
    __tablename__ = 'stops'
    
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'))
    stop_name = db.Column(db.String(255), nullable=False)
    stop_order = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Numeric(9, 6))
    longitude = db.Column(db.Numeric(9, 6))
    estimated_arrival_time = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Driver(db.Model):
    __tablename__ = 'drivers'
    
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255))
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    license_expiry = db.Column(db.Date)
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.Text)
    experience_years = db.Column(db.Integer)
    assigned_bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'))
    assigned_route_id = db.Column(db.Integer, db.ForeignKey('routes.id'))
    shift = db.Column(db.String(20))  # Morning, Evening, Night
    status = db.Column(db.String(20), default='Active')  # Active, On Leave, Inactive
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

class Conductor(db.Model):
    __tablename__ = 'conductors'
    
    id = db.Column(db.Integer, primary_key=True)
    conductor_id = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255))
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.Text)
    experience_years = db.Column(db.Integer)
    assigned_bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'))
    assigned_route_id = db.Column(db.Integer, db.ForeignKey('routes.id'))
    shift = db.Column(db.String(20))  # Morning, Evening, Night
    role = db.Column(db.String(50), default='Conductor')  # Conductor, Ticket Collector
    status = db.Column(db.String(20), default='Active')  # Active, On Leave, Inactive
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
