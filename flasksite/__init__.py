import os
from flasksite.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# Extentions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'



def create_app(config_class=Config):
    # Creation of App
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extentions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Blueprint stuff
    from flasksite.main.routes import main
    from flasksite.users.routes import users
    from flasksite.posts.routes import posts
    from flasksite.reservations.routes import reservations
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(reservations)

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)