from user import User
class Account(User):
    def __init__(self, card):
        self.card = card
        self.balance = 0
        
    def change(self, amount):
        self.balance += amount