from app.app_and_db import db
from app.users.models import Role, UserRoles
from sqlalchemy import func
from flask_user import current_user

def process_admin_page_request(req):
    user_id = req.form.get('user-id', default=None, type=int)
    action = req.form.get('action-type', default=None).encode('ascii','ignore')
    print "######## user-id: %s, action: %s"%(user_id, action)
    if user_id and action:
        if current_user.id == user_id:
            # raise some exception
            return
        if action == 'add-admin':
            add_admin_role_to_user(user_id)
        elif action == 'remove-admin':
            remove_admin_role_from_user(user_id)
        else:
            print "This should not happen"

def remove_admin_role_from_user(user_id):
    admin_role_id = get_admin_role_id()
    if admin_role_id:
        user_role_id = get_user_role_id_by_user_and_role(user_id, admin_role_id)
        if user_role_id:
            remove_user_role(user_role_id)

def add_admin_role_to_user(user_id):
    admin_role_id = get_admin_role_id()
    if admin_role_id:
        if not user_role_already_exists(user_id, admin_role_id):
            insert_user_role(user_id,admin_role_id)

def get_admin_role_id():
    admin_role_id = db.session.query(Role).filter(Role.name=="admin").first()
    if admin_role_id:
        return admin_role_id.id
    return None

def user_role_already_exists(user_id, role_id):
    user_role_id = get_user_role_id_by_user_and_role(user_id, role_id)
    return True if user_role_id else False

def get_user_role_id_by_user_and_role(user_id, role_id):
    db_entry_instance = db.session.query(UserRoles).filter(UserRoles.user_id == user_id, UserRoles.role_id == role_id).first()
    return db_entry_instance.id if db_entry_instance else None

def insert_user_role(user_id, role_id):
    next_id = db.session.query(func.max(UserRoles.id)).first()[0] + 1
    new_user_role = UserRoles(id = next_id, user_id = user_id, role_id = role_id)
    db.session.add(new_user_role)
    db.session.commit()

def remove_user_role(user_role_id):
    db.session.query(UserRoles).filter(UserRoles.id == user_role_id).delete(synchronize_session=False)
    db.session.commit()
