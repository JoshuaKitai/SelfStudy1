from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import UUID, String, DateTime
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from flask_bcrypt import Bcrypt
import uuid

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    __tablename__ = "users"
    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = mapped_column(String(254), unique=True)
    hash = mapped_column(String(60))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

def init(app):
    db.init_app(app)
    with app.app_context():
        try: # idk why, but sometimes this fails but its ok????
            db.create_all()
        except:
            pass

def signup(app, bcrypt, email, password):
    with app.app_context():
        user = User(
            email=email,
            hash=bcrypt.generate_password_hash(password).decode("utf-8")
        )
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(e, flush=True)
            return None
        return user.uuid

def login(app, bcrypt, email, password):
    with app.app_context():
        try:
            user = db.session.execute(db.select(User).where(User.email == email)).first()[0]
            if bcrypt.check_password_hash(user.hash, password):
                return user.uuid
        except Exception as e:
            print(e, flush=True)
        return None

def get_user_email(app, uuid):
    with app.app_context():
        user = db.session.execute(db.select(User).where(User.uuid == uuid)).first()
        return user.email
