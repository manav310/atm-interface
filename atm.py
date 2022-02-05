from user import User
from account import Account
from card import Card
import logging
import random

class ATM:
    
    def __init__(self):
        self.df = pd.read_csv('account_database.csv', index_col=0)
        logging.info('Database read successfully!')
    
    def update_dataframe(self):
        self.df.to_csv('account_database.csv')
        logging.info('Database updated successfully!')
    
    def get_number_of_users(self):
        try:
            with open('number_of_users.txt','r') as f:
                users = f.read()
            f.close()
            logging.info('Number of users read successfully!')
            return int(users)
        except:
            logging.error('Text file containing number of users not found! Exiting....')
        return None
    
    def update_number_of_users(self):
        users = self.get_number_of_users()
        users = users + 1
        with open('number_of_users.txt','w') as f:
            f.write(str(users))
        f.close()
        logging.info('Number of users updated successfully!')
        
    def welcome_message(self):
        print("Welcome to the BITS ATM!\n")
    
    def inp(self):
        
        n = int(input("Enter 1 to login to an existing account\nEnter 2 to create a new account\nEnter 3 to exit\n"))
        
        if n==1:
            logging.info('User chose to login to an existing account')
            query_card = int(input("Enter card number: "))
            if self.df[self.df['Card Number']==query_card].shape[0]==0:
                print("Card number does not exist! Exiting....")
                self.inp()
            self.enterpin(self.df.loc[self.df['Card Number']==query_card,'PIN'], query_card)
            
        elif n==2:
            logging.info('User chose to creat a new account')
            account_name = input("Enter account name: ")
            card = random.randint(10**15, 10**16-1) ## generating 16 digit card number for user
            print("Your card number: ", card)
            logging.info("Card number generated!")
            while(True):
                pin = int(input("Enter a PIN: "))
                cpin = int(input("Re-enter PIN to confirm creation of account: "))
                if(pin==cpin):
                    break
                else:
                    print("PIN did not match, enter new PIN!")
                    logging.warning("PIN did not match")
            user = User(account_name, card, pin)
            account = Account(card)
            current_number_of_users = self.get_number_of_users()
            if current_number_of_users==None:
                print('Text file containing number of users not found! Exiting...')
                print("Thanks for visiting BITS ATM!")
                exit(0)
            self.df.loc[current_number_of_users, 'Account Name'] = account_name
            self.df.loc[current_number_of_users, 'Card Number'] = int(card)
            self.df.loc[current_number_of_users, 'PIN'] = int(pin)
            self.df.loc[current_number_of_users, 'Balance'] = 0
            self.update_number_of_users()
            self.update_dataframe()
            print("Account created successfully!")
            logging.info('New account created!')
            self.transaction(card, account)
            
        elif n==3:
            logging.info('User chose to exit')
            print("Thanks for visiting BITS ATM!")
            
        else:
            logging.info('User entered wrong choice')
            print("Invalid Choice!")
            self.inp()
            
    def enterpin(self, ground_truth_pin, query_card):
        n = 0
        
        while(n<5):
            p = int(input("Enter PIN: "))
            if(Card.validate(ground_truth_pin, p)==True):
                logging.info('PIN matched! Logging in....')
                print("\nAccount Details: ")
                print("\nAccount name: ", self.df.loc[self.df['Card Number']==query_card, 'Account Name'].values[0])
                print("\nCard number: ", query_card)
                user = User(self.df.loc[self.df['Card Number']==query_card, 'Account Name'].values[0], query_card, self.df.loc[self.df['Card Number']==query_card, 'PIN'].values[0])
                account = Account(query_card)
                account.balance = self.df.loc[self.df['Card Number']==query_card, 'Balance'].values[0]
                self.transaction(query_card, account)
                break
            else:
                n+=1
                print("PIN does not match with an existing account")
                print("You have "+str(6-n)+" more tries left")
                logging.warning("PIN does not match with an existing account")
                logging.warning("User "+str(6-n)+" more tries left")
                
        if(n==5):
            print("Session terminated!")
            logging.error("Session terminated! Entered pin did not match with the existing account")
            self.welcome_message()
            self.inp()
        
    def transaction(self, card, account):
        choice = input("Enter 'd' for deposit, 'w' for withdraw or 'b' to check account balance: ")
        choice = choice.lower()
        if(choice=='d'):
            logging.info("User chose to deposit money")
            self.deposit(card, account)
        elif(choice=='w'):
            logging.info("User chose to withdraw money")
            self.withdraw(card, account)
        elif(choice=='b'):
            logging.info("User chose to check the balance of his/her account")
            self.checkbalance(card, account)
        else:
            logging.warning("User entered invalid choice when asked to choose between types of transaction!")
            print('Invalid choice!')
            self.transaction(card, account)
    
    def take_user_choice(self):
        ch = input("Do you want to make any further transactions? Enter(y/n)")
        if ch=='y' or ch=='n':
            return ch
        else:
            print("Invalid Choice!")
            logging.warning("User entered invalid choice when asked if he/she wants to continue performing transactions!")
            return None
    
    def deposit(self, card, account):
        
        print("Your current account balance: ", self.df.loc[self.df['Card Number']==card, 'Balance'].values[0])
        amount = float(input("\nEnter the amount you want to deposit: Rs."))
        account.change(amount)
        self.df.loc[self.df['Card Number']==card,'Balance'] = account.balance
        print("Your changed account balance: Rs.", account.balance)
        print("Transaction successful!")
        self.update_dataframe()
        print("Database update successful!")
        ch = self.take_user_choice()
        while ch == None:
            ch = self.take_user_choice()
        if(ch=='y'):
            logging.info("User wants to continue transactions!")
            self.transaction(card, account)
        elif(ch=='n'):
            logging.info("User exited!")
            print("Thanks for visiting BITS ATM!")
            self.welcome_message()
            self.inp()           
            
        
    def withdraw(self, card, account):
        print("Your current account balance: ", self.df.loc[self.df['Card Number']==card, 'Balance'].values[0])
        amount = float(input("\nEnter the amount you want to withdraw: Rs."))
        if(amount>account.balance):
            logging.warning("Amount exceeds current balance")
            print("Insufficient balance! Please try again")
            self.transaction(card, account)
        am = -amount
        account.change(am)
        print("Your changed account balance: Rs.", account.balance)
        self.df.loc[self.df['Card Number']==card,'Balance'] = account.balance
        print("Transaction successful!")
        self.update_dataframe()
        print("Database update successful!")
        ch = self.take_user_choice()
        while ch == None:
            ch = self.take_user_choice()
        if(ch=='y'):
            logging.info("User wants to continue transactions!")
            self.transaction(card, account)
        elif(ch=='n'):
            logging.info("User exited!")
            print("Thanks for visiting BITS ATM!")
            self.welcome_message()
            self.inp()
        
     
    def checkbalance(self, card, account):
        print("Your current account balance: ", self.df.loc[self.df['Card Number']==card,'Balance'].values[0])
        ch = self.take_user_choice()
        print("choice == ", ch)
        while ch == None:
            ch = self.take_user_choice()
        if(ch=='y'):
            logging.info("User wants to continue transactions!")
            self.transaction(card, account)
        elif(ch=='n'):
            logging.info("User exited!")
            print("Thanks for visiting BITS ATM!")
            self.welcome_message()
            self.inp()
            

atm = ATM()
atm.inp()