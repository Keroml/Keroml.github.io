from app import app, db
with app.app_context():  # <- Это обязательно!
    db.create_all()
