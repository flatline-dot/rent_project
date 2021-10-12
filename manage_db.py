from webapp.model import db, User
from webapp import create_app

app = create_app()
with app.app_context():
    flat = User.query.filter_by(username='Ivan').delete()
    db.session.commit()
