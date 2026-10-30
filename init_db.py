from database import Base, engine
from models import Employee

Base.metadata.create_all(bind=engine)
print("Database tables created.")
