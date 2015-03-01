from app.app_and_db import db

from flask import render_template
from app.users.models import User, Role, UserRoles

def create_label(user):
    roles=[db_row.Role.name for db_row in db.session.query(UserRoles, Role)\
        .filter(UserRoles.role_id == Role.id, UserRoles.user_id == user.id)]
    return {
        'id' : user.id,
        'name': user.first_name + ' ' + user.last_name,
        'admin':'admin' in roles,
        'regular_user':'regular' in roles
    }

def get_users_and_roles():
    return [create_label(user) for user in db.session.query(User).all()]

def render_admin_page():
    users_and_roles = get_users_and_roles()
    print users_and_roles
    return render_template('pages/admin_page.html', usersAndRoles=users_and_roles)