from flask import Blueprint, render_template, jsonify
from app import db
from app.models import User, Bus, Route, Booking, Payment, LiveBusLocation, Driver, Conductor
from sqlalchemy import func, extract
from datetime import datetime, timedelta

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/')
def dashboard():
    """Admin dashboard home"""
    return render_template('admin/dashboard.html')

@bp.route('/api/stats')
def get_stats():
    """Get dashboard statistics"""
    try:
        # Total counts
        total_users = User.query.count()
        total_buses = Bus.query.filter_by(is_active=True).count()
        total_routes = Route.query.filter_by(is_active=True).count()
        total_bookings = Booking.query.count()
        
        # Today's bookings
        today = datetime.now().date()
        today_bookings = Booking.query.filter(
            func.date(Booking.created_at) == today
        ).count()
        
        # Revenue statistics
        total_revenue = db.session.query(func.sum(Payment.amount)).filter(
            Payment.status == 'completed'
        ).scalar() or 0
        
        today_revenue = db.session.query(func.sum(Payment.amount)).filter(
            Payment.status == 'completed',
            func.date(Payment.payment_date) == today
        ).scalar() or 0
        
        # Booking status distribution
        booking_statuses = db.session.query(
            Booking.status,
            func.count(Booking.id)
        ).group_by(Booking.status).all()
        
        status_data = {status: count for status, count in booking_statuses}
        
        # Active buses
        active_buses = LiveBusLocation.query.count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_users': total_users,
                'total_buses': total_buses,
                'total_routes': total_routes,
                'total_bookings': total_bookings,
                'today_bookings': today_bookings,
                'total_revenue': float(total_revenue),
                'today_revenue': float(today_revenue),
                'booking_statuses': status_data,
                'active_buses': active_buses
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/bookings/recent')
def get_recent_bookings():
    """Get recent bookings with route information"""
    try:
        # Get bookings with route details
        bookings = db.session.query(
            Booking.id,
            Booking.booking_reference,
            Booking.passenger_name,
            Booking.passenger_category,
            Booking.fare_amount,
            Booking.status,
            Booking.journey_date,
            Booking.created_at,
            Route.route_number,
            Route.route_name,
            Route.start_location,
            Route.end_location
        ).outerjoin(
            Route, Booking.route_id == Route.id
        ).order_by(Booking.created_at.desc()).limit(10).all()
        
        data = []
        for b in bookings:
            # Create activity description
            if b.route_number and b.start_location and b.end_location:
                activity_desc = f"Route {b.route_number}: {b.start_location} → {b.end_location}"
            elif b.route_name:
                activity_desc = f"Route: {b.route_name}"
            else:
                activity_desc = "Bus Booking"
            
            # Determine fare (use route fare if booking fare is 0)
            fare = float(b.fare_amount) if b.fare_amount and b.fare_amount > 0 else 0.0
            
            data.append({
                'id': b.id,
                'booking_reference': b.booking_reference,
                'passenger_name': b.passenger_name,
                'passenger_category': b.passenger_category or 'General',
                'activity_description': activity_desc,
                'route_number': b.route_number or 'N/A',
                'fare_amount': fare,
                'status': b.status or 'pending',
                'journey_date': b.journey_date.strftime('%Y-%m-%d %H:%M') if b.journey_date else 'N/A',
                'created_at': b.created_at.strftime('%Y-%m-%d %H:%M') if b.created_at else 'N/A'
            })
        
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/revenue/monthly')
def get_monthly_revenue():
    """Get monthly revenue data for chart"""
    try:
        # Get last 6 months revenue
        six_months_ago = datetime.now() - timedelta(days=180)
        
        revenue_data = db.session.query(
            extract('month', Payment.payment_date).label('month'),
            extract('year', Payment.payment_date).label('year'),
            func.sum(Payment.amount).label('total')
        ).filter(
            Payment.status == 'completed',
            Payment.payment_date >= six_months_ago
        ).group_by('month', 'year').order_by('year', 'month').all()
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        data = [{
            'month': months[int(r.month) - 1],
            'revenue': float(r.total)
        } for r in revenue_data]
        
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/buses/active')
def get_active_buses():
    """Get active buses with location"""
    try:
        buses = db.session.query(
            Bus.bus_number,
            Bus.bus_type,
            LiveBusLocation.latitude,
            LiveBusLocation.longitude,
            LiveBusLocation.speed,
            LiveBusLocation.last_updated
        ).join(
            LiveBusLocation, Bus.id == LiveBusLocation.bus_id
        ).filter(Bus.is_active == True).limit(20).all()
        
        data = [{
            'bus_number': b.bus_number,
            'bus_type': b.bus_type,
            'latitude': float(b.latitude),
            'longitude': float(b.longitude),
            'speed': float(b.speed) if b.speed else 0,
            'last_updated': b.last_updated.strftime('%Y-%m-%d %H:%M:%S')
        } for b in buses]
        
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/bookings')
def bookings_page():
    """Bookings management page"""
    return render_template('admin/bookings.html')

@bp.route('/api/bookings/all')
def get_all_bookings():
    """Get all bookings with route info"""
    try:
        bookings = db.session.query(
            Booking.id,
            Booking.booking_reference,
            Booking.passenger_name,
            Booking.passenger_category,
            Booking.journey_date,
            Booking.fare_amount,
            Booking.status,
            Route.route_number
        ).outerjoin(
            Route, Booking.route_id == Route.id
        ).order_by(Booking.created_at.desc()).all()
        
        data = [{
            'id': b.id,
            'booking_reference': b.booking_reference,
            'passenger_name': b.passenger_name,
            'passenger_category': b.passenger_category or 'general',
            'journey_date': b.journey_date.isoformat(),
            'fare_amount': float(b.fare_amount),
            'status': b.status or 'pending',
            'route_number': b.route_number or 'N/A'
        } for b in bookings]
        
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/bookings/stats')
def get_booking_stats():
    """Get booking statistics"""
    try:
        total = Booking.query.count()
        confirmed = Booking.query.filter_by(status='confirmed').count()
        pending = Booking.query.filter_by(status='pending').count()
        cancelled = Booking.query.filter_by(status='cancelled').count()
        
        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'confirmed': confirmed,
                'pending': pending,
                'cancelled': cancelled
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/bookings/<int:booking_id>/confirm', methods=['POST'])
def confirm_booking(booking_id):
    """Confirm a booking"""
    try:
        booking = Booking.query.get(booking_id)
        if booking:
            booking.status = 'confirmed'
            db.session.commit()
            return jsonify({'success': True, 'message': 'Booking confirmed'})
        return jsonify({'success': False, 'error': 'Booking not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/bookings/<int:booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id):
    """Cancel a booking"""
    try:
        booking = Booking.query.get(booking_id)
        if booking:
            booking.status = 'cancelled'
            db.session.commit()
            return jsonify({'success': True, 'message': 'Booking cancelled'})
        return jsonify({'success': False, 'error': 'Booking not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/buses')
def buses_page():
    """Buses management page"""
    return render_template('admin/buses.html')

@bp.route('/routes')
def routes_page():
    """Routes management page"""
    return render_template('admin/routes.html')

@bp.route('/users')
def users_page():
    """Users management page"""
    return render_template('admin/users.html')

@bp.route('/payments')
def payments_page():
    """Payments management page"""
    return render_template('admin/payments.html')

@bp.route('/chatbot')
def chatbot_page():
    """Chatbot management page"""
    return render_template('admin/chatbot.html')

@bp.route('/api/buses/all')
def get_all_buses():
    """Get all buses"""
    try:
        buses = Bus.query.all()
        data = [{
            'id': b.id,
            'bus_number': b.bus_number,
            'registration_number': b.registration_number,
            'capacity': b.capacity,
            'bus_type': b.bus_type or 'Standard',
            'is_active': b.is_active
        } for b in buses]
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/buses/stats')
def get_bus_stats():
    """Get bus statistics"""
    try:
        total = Bus.query.count()
        active = Bus.query.filter_by(is_active=True).count()
        ac_buses = Bus.query.filter(Bus.bus_type.ilike('%AC%')).count()
        avg_capacity = db.session.query(func.avg(Bus.capacity)).scalar() or 0
        
        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'active': active,
                'ac_buses': ac_buses,
                'avg_capacity': int(avg_capacity)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/routes/all')
def get_all_routes():
    """Get all routes"""
    try:
        routes = Route.query.all()
        data = [{
            'id': r.id,
            'route_number': r.route_number,
            'route_name': r.route_name,
            'start_location': r.start_location,
            'end_location': r.end_location,
            'distance_km': float(r.distance_km) if r.distance_km else 0,
            'fare': float(r.fare),
            'is_active': r.is_active
        } for r in routes]
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/users/all')
def get_all_users():
    """Get all users"""
    try:
        users = User.query.all()
        data = [{
            'id': u.id,
            'full_name': u.full_name,
            'email': u.email,
            'phone': u.phone,
            'role': u.role or 'passenger',
            'is_active': u.is_active,
            'created_at': u.created_at.isoformat() if u.created_at else None
        } for u in users]
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/payments/all')
def get_all_payments():
    """Get all payments"""
    try:
        payments = db.session.query(
            Payment.id,
            Payment.transaction_id,
            Payment.amount,
            Payment.payment_method,
            Payment.status,
            Payment.payment_date,
            Booking.booking_reference
        ).join(
            Booking, Payment.booking_id == Booking.id
        ).order_by(Payment.payment_date.desc()).all()
        
        data = [{
            'id': p.id,
            'transaction_id': p.transaction_id,
            'amount': float(p.amount),
            'payment_method': p.payment_method,
            'status': p.status,
            'payment_date': p.payment_date.isoformat() if p.payment_date else None,
            'booking_reference': p.booking_reference
        } for p in payments]
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/routes/stats')
def get_route_stats():
    """Get route statistics"""
    try:
        total = Route.query.count()
        active = Route.query.filter_by(is_active=True).count()
        total_distance = db.session.query(func.sum(Route.distance_km)).scalar() or 0
        avg_fare = db.session.query(func.avg(Route.fare)).scalar() or 0
        
        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'active': active,
                'total_distance': int(total_distance),
                'avg_fare': int(avg_fare)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/users/stats')
def get_user_stats():
    """Get user statistics"""
    try:
        total = User.query.count()
        active = User.query.filter_by(is_active=True).count()
        admins = User.query.filter_by(role='admin').count()
        passengers = User.query.filter_by(role='passenger').count()
        
        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'active': active,
                'admins': admins,
                'passengers': passengers
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/payments/stats')
def get_payment_stats():
    """Get payment statistics"""
    try:
        total = Payment.query.count()
        completed = Payment.query.filter_by(status='completed').count()
        
        total_revenue = db.session.query(func.sum(Payment.amount)).filter(
            Payment.status == 'completed'
        ).scalar() or 0
        
        today = datetime.now().date()
        today_revenue = db.session.query(func.sum(Payment.amount)).filter(
            Payment.status == 'completed',
            func.date(Payment.payment_date) == today
        ).scalar() or 0
        
        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'completed': completed,
                'total_revenue': float(total_revenue),
                'today_revenue': float(today_revenue)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/drivers')
def drivers_page():
    """Drivers & Staff management page"""
    return render_template('admin/drivers.html')

@bp.route('/live-tracking')
def live_tracking_page():
    """Live bus tracking page"""
    return render_template('admin/live_tracking.html')

@bp.route('/api/staff')
def get_all_staff():
    """Get all drivers and conductors"""
    try:
        # Get drivers with bus and route info
        drivers = db.session.query(
            Driver.id,
            Driver.driver_id,
            Driver.full_name,
            Driver.phone,
            Driver.email,
            Driver.license_number,
            Driver.experience_years,
            Driver.shift,
            Driver.status,
            Driver.assigned_bus_id,
            Driver.assigned_route_id,
            Bus.bus_number.label('assigned_bus_number'),
            Route.route_number.label('assigned_route_number'),
            Route.route_name.label('assigned_route_name')
        ).outerjoin(
            Bus, Driver.assigned_bus_id == Bus.id
        ).outerjoin(
            Route, Driver.assigned_route_id == Route.id
        ).filter(Driver.is_active == True).all()
        
        # Get conductors with bus and route info
        conductors = db.session.query(
            Conductor.id,
            Conductor.conductor_id,
            Conductor.full_name,
            Conductor.phone,
            Conductor.email,
            Conductor.employee_id,
            Conductor.experience_years,
            Conductor.shift,
            Conductor.role,
            Conductor.status,
            Conductor.assigned_bus_id,
            Conductor.assigned_route_id,
            Bus.bus_number.label('assigned_bus_number'),
            Route.route_number.label('assigned_route_number'),
            Route.route_name.label('assigned_route_name')
        ).outerjoin(
            Bus, Conductor.assigned_bus_id == Bus.id
        ).outerjoin(
            Route, Conductor.assigned_route_id == Route.id
        ).filter(Conductor.is_active == True).all()
        
        drivers_data = [{
            'id': d.id,
            'driver_id': d.driver_id,
            'full_name': d.full_name,
            'phone': d.phone,
            'email': d.email,
            'license_number': d.license_number,
            'experience_years': d.experience_years,
            'shift': d.shift,
            'status': d.status,
            'assigned_bus_id': d.assigned_bus_id,
            'assigned_route_id': d.assigned_route_id,
            'assigned_bus_number': d.assigned_bus_number,
            'assigned_route_number': d.assigned_route_number,
            'assigned_route_name': d.assigned_route_name
        } for d in drivers]
        
        conductors_data = [{
            'id': c.id,
            'conductor_id': c.conductor_id,
            'full_name': c.full_name,
            'phone': c.phone,
            'email': c.email,
            'employee_id': c.employee_id,
            'experience_years': c.experience_years,
            'shift': c.shift,
            'role': c.role,
            'status': c.status,
            'assigned_bus_id': c.assigned_bus_id,
            'assigned_route_id': c.assigned_route_id,
            'assigned_bus_number': c.assigned_bus_number,
            'assigned_route_number': c.assigned_route_number,
            'assigned_route_name': c.assigned_route_name
        } for c in conductors]
        
        return jsonify({
            'success': True,
            'drivers': drivers_data,
            'conductors': conductors_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/staff/stats')
def get_staff_stats():
    """Get staff statistics"""
    try:
        total_drivers = Driver.query.filter_by(is_active=True).count()
        total_conductors = Conductor.query.filter_by(is_active=True).count()
        active_drivers = Driver.query.filter_by(status='Active', is_active=True).count()
        active_conductors = Conductor.query.filter_by(status='Active', is_active=True).count()
        on_leave_drivers = Driver.query.filter_by(status='On Leave', is_active=True).count()
        on_leave_conductors = Conductor.query.filter_by(status='On Leave', is_active=True).count()
        
        return jsonify({
            'success': True,
            'data': {
                'total_drivers': total_drivers,
                'total_conductors': total_conductors,
                'active_drivers': active_drivers,
                'active_conductors': active_conductors,
                'on_leave_drivers': on_leave_drivers,
                'on_leave_conductors': on_leave_conductors,
                'total_staff': total_drivers + total_conductors,
                'active_staff': active_drivers + active_conductors
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
