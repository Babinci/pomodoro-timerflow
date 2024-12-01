from app.database import init_db
from app.models import Base

if __name__ == "__main__":
    init_db()
    print("Database initialized")