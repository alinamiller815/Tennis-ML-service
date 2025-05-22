import sqlalchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class UserDB(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    ident = Column(Integer, nullable=True)

    # один пользователь - много предсказаний
    predictions = relationship("PredictionDB", back_populates="user")
    
    # один пользователь - много транзакций
    transactions = relationship("TransactionDB", back_populates="user")


class ModelDB(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    cost = Column(Float, nullable=False)

    # одна модель - много предсказаний
    predictions = relationship("PredictionDB", back_populates="model")


class PredictionDB(Base):
    __tablename__ = 'predictions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    model_id = Column(Integer, ForeignKey("models.id"))
    input_data = Column(String, nullable=False)
    output_data = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("UserDB", back_populates="predictions")
    model = relationship("ModelDB", back_populates="predictions")


class TransactionDB(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Исправленное отношение - теперь оно ссылается на "transactions" в UserDB
    user = relationship("UserDB", back_populates="transactions")