# seed.py  (place this in the project root)
from run import create_app
from app.models import db, Profile

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    demo1 = Profile(name='Alice', age=30, description='Loves hiking.')
    demo2 = Profile(name='Bob',   age=25, description='Coffee addict.')
    db.session.add_all([demo1, demo2])
    db.session.commit()

    print('✅ Seeded profiles.')
