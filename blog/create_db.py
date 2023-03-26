#blog/create_db.py
from blog.models import Entry
from blog import create_app, db
import datetime

app = create_app()

with app.app_context():
    db.create_all()

    first_post = Entry(title="Перша публікація, ще з консолі!", body="Це вміст моєї першої публікації в блозі", is_published=False)
    db.session.add(first_post)
    db.session.commit()

