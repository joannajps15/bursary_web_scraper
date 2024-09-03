import os

#for Flask forms

#configuration class to store config variables
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    