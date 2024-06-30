from ext import app, db
from models import Product, Comments, User
with app.app_context():
    db.create_all()

    admin_user = User("Irakli", "adminpassword", "Admin")
    db.session.add(admin_user)
    db.session.commit()