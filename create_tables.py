from database import Base,engine
from models import Order,Refund

Base.metadata.create_all(bind=engine)

print("Tables created successfully")