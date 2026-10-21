import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from database import Base,get_db
from main import app
from models import Order

TEST_DATABASE_URL =  "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread":False
    }
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

@pytest.fixture
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    orders = [
                Order(
            order_id="A1001",
            customer_name="Alice",
            product_name="Ceramic Egg Coddler",
            amount=29.99,
            status="shipped",
            paid=True
        ),
        Order(
            order_id="A1002",
            customer_name="Bob",
            product_name="Ceramic Egg Coddler",
            amount=29.99,
            status="processing",
            paid=True
        ),
        Order(
            order_id="A1003",
            customer_name="Charlie",
            product_name="Ceramic Egg Coddler",
            amount=29.99,
            status="cancelled",
            paid=False
        )
    ]

    session.add_all(orders)
    session.commit()

    try:
        yield session
    finally:
        session.close()

        Base.metadata.drop_all(
            bind=engine
        )

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass


    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()