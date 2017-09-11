#-*-coding:utf8-*-
import json
from flask import ( request, Response, Blueprint, render_template, 
     jsonify )
from sqlalchemy import not_
from application.models.Database import ( DnsRecords, addrecords, 
     adddomain, delrecords, db )
from application.models.utils import checkdata, checkdomain

dns = Blueprint('dns', __name__,
                    template_folder='templates/dns',
                    static_folder='static')

@dns.route('/dns/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        postdata = request.form
        domain = checkdata('domain', postdata['domain'])
        if domain and not checkdomain(domain):
            adddomain(domain)
            data = {"status": "success", "message": "域名添加成功"}
        else:
            data = {"status": "fail", "error": "域名已存在或输入有误，请重新输入"}
        return Response(json.dumps(data), mimetype='application/json',
                       content_type='application/json')
    dns = db.session.query(DnsRecords.zone).all()
    domains = set([ ''.join(i) for i in dns ])
    return render_template('dns/index.html', domains = domains)


PER_PAGE = 15
@dns.route('/dns/<domain>', defaults={'page': 1}, methods=['POST', 'GET'])
@dns.route('/dns/<domain>/<int:page>')
def add(domain, page):
    zone = checkdata('domain', domain)
    if request.method == 'POST':
        postdata = request.form
        host = checkdata('host', postdata['host'])
        data = checkdata('ip', postdata['data'])
        ttl = checkdata('num', postdata['ttl'])
        type = postdata['type']
        linetype = postdata['linetype']
        status = postdata['status']
        if host and data and ttl and not checkdomain(host):
            ret = addrecords(zone=zone, host=host, type=type, data=data, \
                  ttl=ttl, linetype=linetype, status=status)
            data = {"status": "success", "message": "记录添加成功"} if ret else \
                   {"status": "fail", "error": "记录已存在或输入有误，请重新输入"}
        else:
            data = {"status": "fail", "error": "记录已存在或输入有误，请重新输入"}
        return Response(json.dumps(data), mimetype='application/json', 
                        content_type='application/json')
    pagination = DnsRecords.query.filter_by(zone=zone).filter(not_(DnsRecords.type=='SOA')). \
                 order_by(DnsRecords.host.desc()).paginate(page, PER_PAGE, error_out=False)
    records = pagination.items
    return render_template('dns/add.html', records=records, domain=zone, pagination=pagination)


@dns.route('/dns/delete', methods=['POST'])
@dns.route('/dns/<domain>/delete', methods=['POST'])
def delete(domain):
    postdata = request.get_json()
    if domain:
        zone = domain
        host = checkdata('host', postdata['host'])
        data = checkdata('ip', postdata['data'])
        type = postdata['type']
        linetype = postdata['linetype']
        if host and data and type and linetype:
            ret = delrecords(zone, host, data, type, linetype)
            data = {"status": "success", "message": "记录已删除"} if ret else \
                   {"status": "fail", "error": "请求错误"}
        else:
            data = {"status": "fail", "error": "请求错误"}
    else:
        delrecords(zone)
        data = {"status": "success", "message": "域名已删除"}
    return Response(json.dumps(data), mimetype='application/json',
                    content_type='application/json')

@dns.route('/dns/<domain>/s')
def search(domain):
    data = request.args.get("wd")
    if checkdata('ip', data):        
        records = DnsRecords.query.filter_by(zone=domain, data=data). \
                     order_by(DnsRecords.host.desc()).all()
    else:
        records = DnsRecords.query.filter_by(zone=domain, host=data). \
                     order_by(DnsRecords.host.desc()).all()
    return render_template('dns/add.html', records=records, domain=domain)
