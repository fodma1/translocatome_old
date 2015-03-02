# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import render_template, request
from flask_user import login_required, roles_required

from app.app_and_db import app

from app.pages.admin_page import render_admin_page
from app.pages.admin_page_controller import process_admin_page_request

from app.comppi.views import query_database

import json

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
    if request.method == "POST":
        process_admin_page_request(request)
    return render_admin_page()

@app.route('/viewer', methods=['GET', 'POST'])
def viewer_page():
    if request.method == "POST":
        search_keyword = request.form['searchKeyword']
        query_result = query_database(search_keyword)
        return query_result
    return render_template('pages/viewer_page.html')