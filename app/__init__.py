from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.facebook import make_facebook_blueprint
import os

file_path = os.path.abspath(os.getcwd())+"/todo.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


google_bp = make_google_blueprint(
    client_id="",
    client_secret="",
    redirect_to="google_login",
    scope=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
)
facebook_bp = make_facebook_blueprint(
    client_id="",
    client_secret="",
    redirect_to="facebook_login"
)
github_bp = make_github_blueprint(
    client_id="",
    client_secret="",
    redirect_to="github_login",
    scope="read:user,user:email"
)

app.register_blueprint(google_bp, url_prefix="/google_login")
app.register_blueprint(facebook_bp, url_prefix="/facebook_login")
app.register_blueprint(github_bp, url_prefix="/github_login")


from app import routes, models
