from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# DATABASE_URL = "mysql+mysqlconnector://root:sagar@localhost/referral_db"

DATABASE_URL = "mysql+pymysql://root:sagar@localhost/referral_db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
