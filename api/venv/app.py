import time
from flask import Flask

import psycopg2
from psycopg2 import Error

from create_tables import *
from scrape import *

connection = None
cursor = None

app = Flask(__name__)

# refresh API - to re-ingest data through webscraper
@app.route('/bursary/refresh')
def refresh_db():

    #calls create_tables.py and scrapes
    if create_tables() == 0:
        # print("create table error") 
        return   
    if scrape() == 0:
        # print("scrape error")
        return

    #returns a statement - figure out how to return a statement!

# ingest API - to add new awards to database
# @app.route('/bursary/ingest')
# def add_db():
#     #inserts new entries to table

# search API - to query the results db
@app.route('/bursary/search', methods=['GET', 'POST'])
def get_current_time():
    if request.method == "POST":
        #on post request - parse data and query the db
        print(request.form)
    #get user info via an array
    
    #connect to db
    #query the db via user info

