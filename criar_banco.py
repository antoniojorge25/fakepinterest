from fakepinterest import database, app
from fakepinterest.models import Usuario, Fotos

with app.app_context():
    database.create_all()