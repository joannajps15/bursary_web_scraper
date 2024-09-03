from flask import Flask
from config import Config

test = Flask(__name__) #test is Flask app name
test.config.from_object(Config) #import configs to Flask aspp
    
from app import routes #app is Flask library
