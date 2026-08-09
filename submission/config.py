import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    #used for = login sessions,Cookies,Flash messages,Security
    SECRET_KEY = "change_this_to_a_random_secret_key"
    #use an SQLite database located at instance/trekking.db
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR,"instance","trekking.db")
    #this disables an unnecessary feature and avoids extra memory usage and warnings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    