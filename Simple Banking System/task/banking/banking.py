import random
import sqlite3
import exeptions


class CreditCard:
    list = dict()

    def __init__(self):
        self.number = '400000' + self.generate_luhn()
        self.PIN = str(random.random())[2:6]
        self.balance = 0
        self.list[self.number] = {'pin': self.PIN, 'balance': self.balance}
        print('Your card has been created')
        print(f'Your card number:\n'
              f'{self.number}')
        print(f'Your card PIN:\n'
              f'{self.PIN}\n')

    @staticmethod
    def generate_luhn():
        string = str(random.random())[2:11]
        pos = 1
        check_sum = 8
        for i in string:
            num = int(i)
            if pos % 2 == 1:
                num *= 2
            if num > 9:
                num -= 9
            check_sum += num
            pos += 1
        if check_sum % 10 != 0:
            check_sum = 10 - check_sum % 10
        else:
            check_sum = 0
        string += str(check_sum)
        return string

    @staticmethod
    def check_luhn(string):
        pos = 1
        check_sum = 0
        for i in string:
            num = int(i)
            if pos % 2 == 1:
                num *= 2
            if num > 9:
                num -= 9
            check_sum += num
            pos += 1
        if check_sum % 10 == 0:
            return True
        else:
            return False


connection = sqlite3.connect('card.s3db')
cur = connection.cursor()
try:
    connection.execute('create table card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
except sqlite3.OperationalError:
    pass

menu = '1. Create an account\n2. Log into account\n0. Exit\n'
logged_menu = '1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit'

menu_point = -1
while menu_point != 0:
    print(menu)
    menu_point = int(input())
    if menu_point == 1:
        card = CreditCard()
        while cur.fetchone() is not None:
            card = CreditCard()
        cur.execute(f'insert into card (number,pin) values (\'{card.number}\', \'{card.PIN}\')')
        connection.commit()
    elif menu_point == 2:
        try:
            print('Enter your card number:')
            login = input()
            print('Enter your PIN:')
            pin = input()
            cur.execute(f"select number, pin, balance from card where number = '{login}'")
            _card = cur.fetchone()
            if _card is None or pin != _card[1]:
                raise exeptions.WrongPIN
            print('You have successfully logged in!')
            logged_in = True
            while logged_in:
                print(logged_menu)
                logged_menu_point = int(input())
                # balance
                if logged_menu_point == 1:
                    print('Balance: '+str(_card[2]))
                # add income
                elif logged_menu_point == 2:
                    income = int(input('Enter income:'))
                    new_balance = _card[2] + income
                    cur.execute(f"UPDATE card SET balance = {new_balance} WHERE number = '{login}' ")
                    connection.commit()
                    cur.execute(f"select number, pin, balance from card where number = '{login}'")
                    _card = cur.fetchone()
                    print('Income was added!')
                elif logged_menu_point == 3:
                    print("Transfer\nEnter card number:")
                    transfer_to = input()
                    try:
                        if not CreditCard.check_luhn(transfer_to):
                            raise exeptions.IsNotLuhn
                        cur.execute(f"select number, pin, balance from card where number = '{transfer_to}'")
                        transfer_to = cur.fetchone()
                        if transfer_to is None:
                            raise exeptions.NoSuchCard
                        transfer_amt = int(input('Enter how much money you want to transfer:\n'))
                        if transfer_amt > _card[2]:
                            raise exeptions.NoMoney
                        # cur.execute(f"select number, pin, balance from card where number = '{login}'")
                        # _card = cur.fetchone()
                        new_balance = _card[2] - transfer_amt
                        cur.execute(f"UPDATE card SET balance = {new_balance} WHERE number = '{login}'")
                        connection.commit()
                        cur.execute(f"select number, pin, balance from card where number = '{login}'")
                        _card = cur.fetchone()
                        new_balance = transfer_to[2] + transfer_amt
                        cur.execute(f"UPDATE card SET balance = {new_balance} WHERE number = '{transfer_to[0]}'")
                        connection.commit()
                        cur.execute(f"select number, pin, balance from card where number = '{transfer_to[0]}'")
                        transfer_to = cur.fetchone()
                        print('Success!\n')


                    except exeptions.IsNotLuhn as ex:
                        print(ex)
                    except exeptions.NoSuchCard as ex:
                        print(ex)
                    except exeptions.NoMoney as ex:
                        print(ex)
                elif logged_menu_point == 4:
                    cur.execute(f"delete from card where number = {login}")
                    connection.commit()
                    logged_in = False
                elif logged_menu_point == 5:
                    logged_in = False
                elif logged_menu_point == 0:
                    logged_in = False
                    menu_point = 0



        except exeptions.WrongPIN as ex3:
            print(ex3)
            logged_in = False

    if menu_point == 0:
        print('Bye!')
        cur.close()
