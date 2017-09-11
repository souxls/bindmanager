#-*-coding:utf8-*-
import re
import json
from application.models.Database import searchrecords, searchiprecords
from application.models.utils import checkdata
from flask import Blueprint, render_template, request, Response
from flask_login import login_required, current_user

dashboard = Blueprint('dashboard', __name__,
                    template_folder='templates/dashboard',
                    static_folder='static')

@dashboard.route('/')
@login_required
def index():
    return render_template('dashboard/index.html', current_user=current_user)

@dashboard.route('/s')
@login_required
def search():
    url = request.full_path
    print(request.url)
    print(request.query_string)
    content = request.args.get('wd')
    if checkdata("ip", content): 
        records = searchiprecords(content)
    else:
        zone = '.'.join(re.split('\.', content)[-2:])
        host = '.'.join(re.split('\.', content)[:-2])
        records = searchrecords(zone, host)
    return render_template("dashboard/index.html", records=records, zone=zone, host=host)
