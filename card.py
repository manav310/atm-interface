class Card:
    def validate(user_pin, p):
        if(p==user_pin):
            print("Card Authenticated")
            return True
        return False