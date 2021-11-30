#https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
import os
from flask_msearch import Search
from flask_login import LoginManager
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
app.config['SECRET_KEY'] = 'my_super_secret_key'

#UPLOAD_FOLDER = f'{basedir}\\static\\images'# windows
UPLOAD_FOLDER = f'{basedir}/static/images'# linux

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

photos = UploadSet('photos', IMAGES)
#configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)

migrate = Migrate(app, db)# work for mysql and sqlite3 for added column
with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    
    else:
        migrate.init.init_app(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerlogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u'Please login first'


import shop.routes
from shop.products import routes
from shop.admin import routes
from shop.carts import carts
from shop.customers import routes
from shop.paypal_stuff import routes