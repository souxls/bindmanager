import re
import json
from application.models import  DnsRecords, addrecords, delrecords, db
from flask import request, Response, Blueprint, render_template, jsonify

settings = Blueprint('settings', __name__,
                    template_folder='templates/settings',
                    static_folder='static')

RET = {"success": {"status": "success"},
      "fail": {"status": "fail"}}

@settings.route('/settings/', methods=['POST','GET'])
def index():
    return render_template('settings/index.html')
