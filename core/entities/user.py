# from dataclasses import dataclass

# @dataclass
class User:
    def __init__(self, id: int = None, email: str = None, name: str = None, 
                 hashed_password: str = None, balance: float = 0.0, ident: int = None):
        self.id = id
        self.email = email
        self.name = name
        self.hashed_password = hashed_password
        self.balance = balance
        self.ident = ident

    def deduct_balance(self, amount: float) -> bool:
        # Списание средств
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False
    
    def add_balance(self, amount: float) -> None:
        # Пополнение баланса
        self.balance += amount
