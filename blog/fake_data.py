#blog/fake_data.py
from faker import Faker
from blog.models import Entry, db
from blog import create_app

def generate_entries():
    app = create_app()
    with app.app_context():
        fake = Faker()
        for i in range(10):
            post = Entry(title=fake.text(30), body=fake.text(300), is_published=True)
            db.session.add(post)
        db.session.commit()




