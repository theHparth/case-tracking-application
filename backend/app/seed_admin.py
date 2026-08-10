from app.database import SessionLocal
from app import models
from app.auth import hash_password

db = SessionLocal()

existing = db.query(models.User).filter(models.User.username == "admin").first()
if existing:
    print("Admin user already exists.")
else:
    admin = models.User(
        username="admin",
        hashed_password=hash_password("admin123"),
        role=models.UserRole.admin,
    )
    db.add(admin)
    db.commit()
    print("Admin user created: username=admin password=admin123")

db.close()