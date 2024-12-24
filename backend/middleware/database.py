import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Sessionの作成
# session = Session(autocommit=False, autoflush=True, bind=engine)

# engine の作成
engine = create_engine(
    url=os.environ.get("DB_URL"),
    echo=bool(os.environ.get("DB_ECHO")),
)

SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
