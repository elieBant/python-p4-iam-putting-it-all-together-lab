from flask_migrate import upgrade
from config import app

with app.app_context():
    upgrade()
