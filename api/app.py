from flask import Flask, request, abort, send_file
from flask_socketio import SocketIO
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

from routes.create_award_info_tables import *
from routes.scrape import *
from routes.query_db import *
from routes.create_sheet import *

connection = None
cursor = None

# --- App Start ---
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
app.socketio = SocketIO(app, cors_allowed_origins="*")
load_dotenv() 

# --- API Calls ---

# defacto table display 
@app.route('/bursary/table', methods=['GET'])
def bursary_display():
    if request.method == "GET":
        return query_db(None)
    abort(400) 

# search API - to query the results db
@app.route('/bursary/search', methods=['POST'])
def bursary_search():
    if request.method == "POST":
        req_data = request.get_json()['filters']
        if all(v == ['All'] for v in req_data.values()):
            return query_db(None)
        if 'All' not in req_data['citizenship']:
            req_data['citizenship'].append('All Students') # add all because citizenship has 1:1 matching
        if 'All' in req_data['program']:
            if 'All' in req_data['faculty']:
                req_data['program'].append('Open to any program')
            else:
                req_data['program'].remove('All')
        return query_db(req_data)
    abort(400) 

# spreadsheet API - return a spreadsheet with queried data info
@app.route('/bursary/sheet', methods=['POST'])
def bursary_sheet():
    if request.method == "POST":
        res = []

        req_data = request.get_json()['filters']
        if all(v == ['All'] for v in req_data.values()):
            res = query_db(None)
        else:
            if req_data['citizenship'] is not ['All']:
                req_data['citizenship'].append('All Students') # add all because citizenship has 1:1 matching
            res = query_db(req_data)

        output = io.BytesIO()
        create_sheet(output, res)
        output.seek(0)  # rewind buffer to start

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='bursary_web_scraper_results.xlsx'
        )

    abort(400) 