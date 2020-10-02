from sqlalchemy import Column, Integer, String, Date, Float, DateTime
from db import Base, USE_SQLITE
from sqlalchemy.dialects.postgresql import UUID

USE_SQLITE = True

class Transactions(Base):
    __tablename__ = "transaction_data"

    player_id = (
        Column(String, index=True, unique=False, primary_key=True)
        if USE_SQLITE
        else Column(UUID(as_uuid=True), index=True, unique=False, primary_key=True)
    )
    time = Column(DateTime, primary_key=True, unique=False)
    amount = Column(Float)
    net_amount = Column(Float)
    transaction_type = Column(Float)
