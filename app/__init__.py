from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
import cloudinary

app = Flask(__name__)

cloudinary.config(
    cloud_name="dh5jcbzly",
    api_key="956284944785852",
    api_secret="ZYqL_9IS8N4a6uZ1esDJUBHNeq4"
)

app.secret_key = "14124512B3JKB12IBTIB3214TNY23KLBJ4TB3JKT3B4TUB3T43%%#%^46%$#^#$%@$%2"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/student-data?charset=utf8mb4" % quote(
    '123456a@A')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# Phân trang
app.config["PAGE_SIZE"] = 1

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
admin = Admin(app=app, name='QUẢN TRỊ TRƯỜNG HỌC', template_mode='bootstrap4')

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
