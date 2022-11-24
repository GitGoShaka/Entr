from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from webApp.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    #Initialize databases and flask-migrate
    db.init_app(app)
    migrate.init_app(app, db)
    
    #Initialize blueprints
    from webApp.main.routes import main
    app.register_blueprint(main)

    return app