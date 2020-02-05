from app import app
from models import db, User, Feedback

db.drop_all()
db.create_all()

user1 = User.register(
    username='padawan',
    password='apprentice',
    email='ilovejedis@jedihotmail.com',
    first_name='leia',
    last_name='solo'
)

user2 = User.register(
    username='padawan2',
    password='apprentice2',
    email='ilovejedis2@jedihotmail.com',
    first_name='Han',
    last_name='Solo'
)

feedback1 = Feedback(
    title='Han so so sexy',
    content='SUCH SWAG',
    username='padawan'
)

feedback2 = Feedback(
    title='Lei so so amazing',
    content='SUCH BEAUTY',
    username='padawan2'
)

db.session.add_all([user1, user2, feedback1, feedback2])
db.session.commit()