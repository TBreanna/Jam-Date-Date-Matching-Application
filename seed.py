# seed.py (at project root)
from run import create_app
from app.models import db, Profile

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add_all([
      Profile(name='Alice', age=30, description='Loves hiking.'),
      Profile(name='Bob',   age=25, description='Coffee addict.')
    ])
    db.session.commit()
    print('✅ Seeded profiles.')
