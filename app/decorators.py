"""
####### custom decorators that check user permissions #######
* These decorators are built with the help of the functools package from the Python standard library 
* and return a 403 response, 
* the “Forbidden” HTTP status code, when the current user does not have the requested permission.
"""

from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)


# Usage Eamples:

"""
from .decorators import admin_required, permission_required

@main.route('/admin') 
@login_required 
@admin_required
def for_admins_only():
    return "For administrators!"
    
@main.route('/moderate')
@login_required 
@permission_required(Permission.MODERATE) 
def for_moderators_only():
    return "For comment moderators!"

"""