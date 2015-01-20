# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import render_template, request
from flask_user import login_required, roles_required

from app.app_and_db import app

from app.pages.adminpage import render_admin_page
from app.pages.adminpagecontroller import process_admin_page_request



# The Home page is accessible to anyone
@app.route('/')
def home_page():
    return render_template('pages/home_page.html')

# The Member page is accessible to authenticated users (users that have logged in)
@app.route('/member')
@login_required             # Limits access to authenticated users
def member_page():
    return render_template('pages/member_page.html')

# The Admin page is accessible to users with the 'admin' role
@app.route('/admin', methods=['GET', 'POST'])
@roles_required('admin')    # Limits access to users with the 'admin' role
def admin_page():
    if request.method == "POST" :
        process_admin_page_request(request)
    return render_admin_page()
