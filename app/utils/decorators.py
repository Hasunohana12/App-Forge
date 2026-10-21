from functools import wraps
from flask import session, redirect, url_for, flash

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session or 'role' not in session:
                return redirect(url_for('login'))
            
            if session.get('role') not in roles:
                user_role = session.get('role')
                if user_role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                elif user_role == 'dev':
                    return redirect(url_for('dev_dashboard'))
                elif user_role == 'cliente':
                    return redirect(url_for('cliente_dashboard'))
                return redirect(url_for('home'))
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator