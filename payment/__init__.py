from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS
import certifi
import os


app = Flask(__name__)
CORS (app)


#configuring payment database 
app.config['MONGODB_SETTINGS'] = {
    "db": "bbsm",
    "host": os.environ.get('MONGO_HOST'),
    "port": 27017,
    "tlsCAFile": certifi.where()
}

db = MongoEngine()
db.init_app(app)

from payment.routes import userpayment

