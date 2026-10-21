from datetime import datetime,timedelta,timezone
from database import SessionLocal
from models import Order

def seed_orders():
    db = SessionLocal()

    try:
        existing_order = db.query(Order).first()
        
        if existing_order:
            print("Orders already exist, skip seeding.")
            return

        orders = [
            Order(
                order_id="A1001",
                customer_name="Alice",
                product_name="Ceramic Egg Coddler",
                amount=29.99,
                status="shipped",
                paid=True,
                created_at=datetime.now(timezone.utc) - timedelta(days=3)
            ),
            Order(
                order_id="A1002",
                customer_name="Bob",
                product_name="Ceramic Egg Coddler",
                amount=29.99,
                status="processing",
                paid=True,
                created_at=datetime.now(timezone.utc) - timedelta(days=2)
            ),
            Order(
                order_id="A1003",
                customer_name="Charlie",
                product_name="Ceramic Egg Coddler",
                amount=29.99,
                status="cancelled",
                paid=False,
                created_at=datetime.now(timezone.utc) - timedelta(days=10)
            )
        ]

        db.add_all(orders)
        db.commit()

        print("Seed data inserted successfully.")

    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
    
    finally:
        db.close()

if __name__ == "__main__":
    seed_orders()