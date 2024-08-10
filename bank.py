# Only current account user can take loan from bank
# Admin name : admin
# Admin pass : 123

from abc import ABC, abstractmethod

class Bank:
    def __init__(self) -> None:
        self.accounts = []
        self.total_loan_amount = 0
        self.loan_feature = True
        self.bankRput = False

    def create_savings_account(self, name, email, address, interestRate):
        newAccount = SavingsAccount(self, name, email, address, interestRate)
        return newAccount
    
    def create_current_account(self, name, email, address, limit):
        newAccount = CurrentAccount(self, name, email, address, limit)
        return newAccount
    
    def delete_account(self, userId):
        accExists = False

        for account in self.accounts:
            if account.id == userId:
                accExists = True
        
        if accExists:
            updated_accounts = []

            for account in self.accounts:
                if account.id != userId:
                    updated_accounts.append(account)
                
                self.accounts = updated_accounts

            print(f'\n\t->Account with id {userId} deleted!')
        
        else:
            print('\n\t->No such Account ')

            
    def get_total_balance(self):
        total_balance = 0
        for account in self.accounts:
            total_balance += account.balance
        
        print(f'\t->Total bank balance : {total_balance}') 
    
    def get_total_loan(self):
         print(f'\t->Total Loan Amount : {self.total_loan_amount}') 

    def show_all_accounts(self):
        return self.accounts

    def change_loan_feature(self, key):
        if key == 'off':
            self.loan_feature = False
        else:
            self.loan_feature = True

    def change_bank_status(self, key):
        if key == 'ds':
            self.bankRput = False
        else:
            self.bankRput = True

class Account(ABC):
    
    def __init__(self, bank, name, email, address, type) -> None:
        self.id = len(bank.accounts) + 1001
        self.name = name
        self.email = email
        self.address = address
        self.type = type
        self.balance = 0
        self.transactions = []
        
        bank.accounts.append(self)

        print(f'\n\t->Account Inserted with id {self.id}')

    @abstractmethod
    def show_info(self):
        raise NotImplementedError
        
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f'\n\t->{amount} Tk depostied')
            self.transactions.append(f'{amount} Tk depostied')
        else:
            print('\nInvalid Account')

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            print(f'\n\t->{amount} Tk withdrawed')
            self.transactions.append(f'{amount} Tk withdrawed')
        else:
            print('Withdrawal amount exceeded')

    def check_balance(self):
        print(f'\n\t->Account balance: {self.balance}')

    def see_tarnsaction_history(self):
        for transaction in self.transactions:
            print(transaction)

    def show_transaction_history(self):
        print(f'\n\t-> Transaction history <-')
        for transaction in self.transactions:
            print(f'\t{transaction}')

    def user_exists(self, bank, receiver_id):
        for account in bank.accounts:
            if account.id == receiver_id:
                return account
        return None
    
    def transfer_balance(self, bank, receiver_id, amount):
        receiver = self.user_exists(bank, receiver_id)
        if not receiver:
            print(f'\n\t->Account not exist.')
        
        elif self.balance < amount:
            print(f'\n\t->Not enough balance')
        
        else:
            self.balance -= amount
            receiver.balance += amount
            print(f'\n\t-> {amount} Tk sent')
            self.transactions.append(f'{amount} Tk sent to account {receiver.id}')
            receiver.transactions.append(f'{amount} Tk received from account {self.id}')

class SavingsAccount(Account):
    def __init__(self, bank, name, email, address, interestRate) -> None:
        self.interestRate = interestRate
        super().__init__(bank, name, email, address, 'savings')
        
    def show_info(self):
        print('\n\t------> Showing info <------')
        print(f'\tId: {self.id}\n\tName: {self.name}\n\tEmail: {self.email}\n\tBalance: {self.balance}\n\tInterest rate: {self.interestRate}')

    def applyInterest(self):
        interest = self.balance * (self.interestRate/100)
        print(f'\n\tApplied interest of {interest}')
        self.deposit(interest)

class CurrentAccount(Account):
    def __init__(self, bank, name, email, address, limit) -> None:
        self.limit = limit
        self.loan_taken = 0
        super().__init__(bank, name, email, address, 'current')

    def take_loan(self, bank, amount):
        if bank.loan_feature:
            if self.loan_taken >= 2:
                print('\n\t->Loan can be taken at most 2 times\n')
            else:
                self.loan_taken += 1
                self.balance += amount
                bank.total_loan_amount += amount
                print(f'\n\t->{amount} Tk Loan Received')
                self.transactions.append(f'{amount} Tk loan received')
        else:
            print('\n\t->Loan feature Disabled')

    
    def withdraw(self, amount, limit):
        if amount > 0 and amount <= limit:
            if amount > self.balance:
                overdraft = amount - self.balance
                self.limit -= overdraft
                self.balance -= amount
                print(f'\n\t-> {amount} Tk withdrawed')
                self.transactions.append(f'{amount} Tk withdrawed')

            else:
                self.balance -= amount
                print(f'\n\t-> {amount} Tk withdrawed')
                self.transactions.append(f'{amount} Tk withdrawed')
        
        elif amount > limit:
            print('\n\t->Limit Over! Deposit Balance')

        else:
            print('\n\t->Invalid amount')

    def show_info(self):
        print('\n\t------> Showing Current Ac Info <------')
        print(f'\tId: {self.id}\n\tName: {self.name}\n\tEmail: {self.email}\n\tBalance: {self.balance}\n\tOverdraft Left: {self.limit}')
            
class Admin:
    def __init__(self, bank) -> None:
        self.bank = bank

    
    def show_all_accounts(self):
        accs = self.bank.show_all_accounts()
        print('\n\t-----> Showing all acounts <-----')
        for account in accs:
            print(f'\tAccount id: {account.id} Account Name: {account.name} Type: {account.type}')

        print('')

    def check_total_bank_balance(self):
        self.bank.get_total_balance()

    def check_lotal_loan_amount(self):
        self.bank.get_total_loan()

    def change_loan_feature(self, key):
        self.bank.change_loan_feature(key)
        if key == 'off':
            print('\n\t->Loan feature Disabled')
        else:
            print('\n\t->Loan feature Enabled')

    def change_bank_status(self, key):
        self.bank.change_bank_status(key)
        if key == 'en':
            print('\n\t->Bankrupt')
        else:
            print('\n\t->Solvent')


bank = Bank()
admin = Admin(bank)

currentUser = None

while(True):
    if not currentUser:
        print(f'\n\tNo logged in User !\n')
        ch = input('Admin or Login or Register(A\L\R):')
        print('')

        if ch == 'R':
            name = input('Enter name: ')
            gmail = input('Enter gmail: ')
            address = input('Enter Address: ')
            type = input('Enter account type (sv/cr):')

            if type == 'sv':
                interestRate = int(input("Interest rate: "))
                newUser = bank.create_savings_account(name, gmail, address, interestRate)
                currentUser = newUser

            elif type == 'cr':
                limit = int(input('Overdraft Limit:'))
                newUser = bank.create_current_account(name, gmail, address, limit)
                currentUser = newUser
                   
        elif ch == 'L':
            id = int(input('Account Number: '))

            for account in bank.accounts:
                if id == account.id:
                    currentUser = account
                    break
        
        elif ch == 'A':
            nm = input('Admin name: ')
            if nm == 'admin':
                ps = input('Admin pass: ')
                if ps == '123':
                    currentUser = 'admin'
                else:
                    print (f'Wrong password!\n')
            else:
                print('\nNo such admin\n')
        
        else:
            print('\nInvalid Choice\n')

    elif currentUser == 'admin':

        print('\n-----> Welcome Admin <------')
        print('[1] Create account')
        print('[2] Delete account')
        print('[3] Sell all accounts')
        print('[4] Check availabe balance')
        print('[5] Check loan amount')
        print('[6] Change loan feature')
        print('[7] Change bank status')
        print('[8] Logout')

        op = int(input('\nChoose option: '))

        print('')

        if(op == 1):
            name = input('Enter name: ')
            email = input('Enter email: ')
            address = input('Enter address: ')
            type = input('Enter account type(sv/cr): ')

            if type == 'sv':
                interestRate = int(input("Interest rate: "))
                bank.create_savings_account(name, email, address, interestRate)
               
            elif type == 'cr':
                limit = int(input('Overdraft Limit: '))
                bank.create_current_account(name, email, address, limit)

        elif op == 2:
            userId = int(input('Enter user id: '))
            bank.delete_account(userId)

        elif op == 3:
            admin.show_all_accounts()

        elif op == 4:
            admin.check_total_bank_balance()

        elif op == 5:
            admin.check_lotal_loan_amount()

        elif op == 6:
            print(f'\nCurrent Loan feature status: {bank.loan_feature}\n')
            status = input('Enter choice(on/off): ')

            admin.change_loan_feature(status)
        
        elif op == 7:
            status = input('Enter choice(en/ds): ')
            admin.change_bank_status(status)

        
        elif op == 8:
            
            currentUser = None

    else:
        if currentUser.type == 'savings':
            print(f'\n-----> Welcome {currentUser.name} <------\n')
            print("[1] Show info")
            print("[2] Deposit")
            print("[3] Withdraw")
            print("[4] Check balance")
            print("[5] Tansaction history")
            print("[6] Apply interest")
            print("[7] Tansfer balance")
            print("[8] Log out")

            op = int(input('\nChoose option: '))

            print('')

            if op == 1:
                currentUser.show_info()
            
            elif op == 2:
                amount = int(input('Enter amount: '))
                currentUser.deposit(amount)

            elif op == 3:
                if not bank.bankRput:
                    amount = int(input('Enter amount: '))
                    currentUser.withdraw(amount)
                
                else:
                    print('\n\t->Bankrupt')

            elif op == 4:
                currentUser.check_balance()

            elif op == 5:
                currentUser.show_transaction_history()
            
            elif op == 6:
                currentUser.applyInterest()
            
            elif op == 7:
                receiver_id = int(input("Enter reciver id: "))
                amount = int(input("Enter amount: "))
                currentUser.transfer_balance(bank, receiver_id, amount)

            elif op == 8:
                currentUser = None

        elif currentUser.type == 'current':
            print(f'\n-----> Welcome {currentUser.name} <------\n')
            print("[1] Show info")
            print("[2] Deposit")
            print("[3] Withdraw")
            print("[4] Check balance")
            print("[5] Tansaction history")
            print("[6] Take loan")
            print("[7] Tansfer balance")
            print("[8] Log out")

            op = int(input('\nChoose option: '))

            if op == 1:
                currentUser.show_info()
            
            elif op == 2:
                amount = int(input('\nEnter amount: '))
                currentUser.deposit(amount)

            elif op == 3:
                if not bank.bankRput:
                    amount = int(input('\nEnter amount: '))
                    currentUser.withdraw(amount, currentUser.limit)
                
                else:
                    print('\t->Bankrupt')

            elif op == 4:
                currentUser.check_balance()

            elif op == 5:
                currentUser.show_transaction_history()
            
            elif op == 6:
                amount = int(input('\nEnter amount: '))
                currentUser.take_loan(bank, amount)
                
            elif op == 7:
                receiver_id = int(input("\nEnter reciver id: "))
                amount = int(input("Enter amount: "))
                currentUser.transfer_balance(bank, receiver_id, amount)

            elif op == 8:
                currentUser = None







