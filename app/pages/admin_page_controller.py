from app.app_and_db import db
from app.users.models import Role, UserRoles
from sqlalchemy import func
from flask_user import current_user


def process_admin_page_request(req):
    user_id = req.form.get('user-id', default=None, type=int)
    action_and_role = req.form.get('action', default=None).encode('ascii', 'ignore')
    if user_id and action_and_role:
        action, role = get_action_and_role(action_and_role)
        if current_user.id == user_id:
            return
        if action == 'give':
            add_role_to_user(user_id, role)
        elif action == 'remove':
            remove_role_from_user(user_id, role)
        else:
            print "This should not happen"


def get_action_and_role(action_and_role):
    get_action_and_role_arr = action_and_role. split(';')
    return get_action_and_role_arr[0], get_action_and_role_arr[1]


def remove_role_from_user(user_id, role):
    role_id = get_role_id(role)
    if role_id:
        user_role_id = get_user_role_id_by_user_and_role(user_id, role_id)
        if user_role_id:
            remove_user_role(user_role_id)


def add_role_to_user(user_id, role):
    role_id = get_role_id(role)
    if role_id:
        print user_id, role_id
        if not user_role_already_exists(user_id, role_id):
            insert_user_role(user_id, role_id)


def get_role_id(role):
    role_id = db.session.query(Role).filter(Role.name==role).first()
    if role_id:
        return role_id.id
    return None


def user_role_already_exists(user_id, role_id):
    user_role_id = get_user_role_id_by_user_and_role(user_id, role_id)
    print user_role_id
    return True if user_role_id else False


def get_user_role_id_by_user_and_role(user_id, role_id):
    db_entry_instance = db.session.query(UserRoles).filter(UserRoles.user_id == user_id, UserRoles.role_id == role_id).first()
    return db_entry_instance.id if db_entry_instance else None


def insert_user_role(user_id, role_id):
    next_id = db.session.query(func.max(UserRoles.id)).first()[0] + 1
    new_user_role = UserRoles(id=next_id, user_id=user_id, role_id=role_id)
    db.session.add(new_user_role)
    db.session.commit()


def remove_user_role(user_role_id):
    db.session.query(UserRoles).filter(UserRoles.id == user_role_id).delete(synchronize_session=False)
    db.session.commit()
