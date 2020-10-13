# Write your code here
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
# cur.execute('''CREATE TABLE card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0); ''')
card_numbers = []
associated_pins = []
associated_balance = []
random_card_number = 0
random_pin = 0
sql_number_list = []
sql_pin_list = []
id = 0


def option_menu():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")


def account_menu():
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")


def luhn_algo(x):
    x = str(x)
    if sum([sum(int(i) for i in x[::-2])] + [sum(divmod(int(d) * 2, 10)) for d in x[-2::-2]]) % 10 == 0:
        return True


def generate_card_numbers():
    import random
    global random_card_number
    global random_pin
    global id
    # using format
    # num_with_zeros = '{:03}'.format(num)
    # using string's zfill
    while True:
        num = random.randrange(1, 10 ** 10)
        first_digits = "400000"
        check_sum = 0
        num_with_zeros = str(num).zfill(10)
        random_card_number = str(first_digits + num_with_zeros)
        if sum([sum(int(i) for i in random_card_number[::-2])] + [sum(divmod(int(d) * 2, 10)) for d in
                                                                  random_card_number[-2::-2]]) % 10 == 0:
            if random_card_number not in card_numbers:
                random_card_number = int(random_card_number)
                break

    id = id + 1
    pin_num = str(random.randrange(1000, 10 ** 4))
    pin_num_with_zeros = pin_num.zfill(4)
    random_pin = int(pin_num_with_zeros)


condition = True
condition_1 = True
condition_2 = True
while condition:
    option_menu()
    choice = int(input())
    if choice == 2:
        while condition_1:
            user_card_number = str(input("Enter your card number: \n"))
            user_pin = str(input("Enter your PIN: \n"))
            sql_number_check = cur.execute(''' SELECT number, pin FROM card WHERE ? = number;''', [user_card_number])
            conn.commit()
            row = [item for item in sql_number_check.fetchall()]
            if len(row) == 0:
                print("Wrong card number or PIN! \n")
                break
            else:
                sql_number_check = row[0][0]
                sql_pin_check = row[0][1]
                if str(user_card_number) == str(sql_number_check):
                    if str(sql_pin_check) == str(user_pin):
                        print("")
                        print("You have successfully logged in! \n")
                        while condition_2:
                            account_menu()
                            account_choice = int(input())
                            if account_choice == 1:
                                sql_balance = cur.execute('''
                                        SELECT balance
                                        FROM card
                                        WHERE ? = number;
                                        ''', [user_card_number])

                                print(sql_balance)
                                print("")
                            elif account_choice == 2:
                                input_income = int(input("Enter income: \n"))
                                sql_balance = cur.execute('''
                                                            SELECT balance
                                                            FROM card
                                                            WHERE ? = number;
                                                            ''', [user_card_number])
                                row = [item for item in sql_balance.fetchall()]
                                sql_balance = row[0][0]
                                new_balance = input_income + int(sql_balance)
                                cur.execute('''UPDATE card
                                                       SET balance = ?
                                                       WHERE ? = number;                       
                                                    ''', [new_balance, user_card_number])
                                conn.commit()
                                print("Income was added!")
                            elif account_choice == 3:
                                print("Transfer")
                                transfer_card_input = str(input("Enter card number:\n"))
                                sql_balance = cur.execute('''
                                                                      SELECT balance
                                                                      FROM card
                                                                      WHERE ? = number;
                                                                   ''', [user_card_number])
                                row = [item for item in sql_balance.fetchall()]
                                sql_balance = row[0][0]
                                if transfer_card_input == user_card_number:
                                    print("You can't transfer money to the same account!")
                                else:
                                    if luhn_algo(transfer_card_input):
                                        sql_number = cur.execute('''
                                                SELECT number
                                                FROM card;''')
                                        row = [list(i) for i in sql_number.fetchall()]
                                        row = list(row)
                                        empty_list = []
                                        for i in row:
                                            empty_list.append(i[0])
                                        if str(transfer_card_input) not in empty_list:
                                            print("Such a card does not exist.")
                                        else:
                                            transfer_money_input = int(input("Enter how much money you want to transfer:\n"))
                                            if transfer_money_input <= int(sql_balance):
                                                user_balance_post_transfer = int(sql_balance) - transfer_money_input
                                                cur.execute('''UPDATE card
                                                                        SET balance = ?
                                                                        WHERE ? = number;
                                                                        ''', [user_balance_post_transfer, user_card_number])
                                                conn.commit()
                                                cur.execute('''UPDATE card
                                                                       SET balance = ?
                                                                       WHERE ? = number;
                                                                       ''', [transfer_money_input, transfer_card_input])
                                                conn.commit()
                                                print("Success!\n")
                                            else:
                                                print("Not enough money!\n")
                                    else:
                                        print("Probably you made a mistake in the card number. Please try again!\n")

                            elif account_choice == 4:
                                cur.execute('''DELETE FROM card WHERE ? = number; ''', [user_card_number])
                                conn.commit()
                                condition_1 = False
                                print("The account has been closed!")
                                condition_2 = False

                            elif account_choice == 5:
                                print("You have successfully logged out! \n")
                                break
                            elif account_choice == 0:
                                condition = False
                                condition_1 = False
                                condition_2 = False
                                print("Bye! \n")
                            else:
                                print("Invalid Input \n")
                    else:
                        print("Wrong card number or PIN! \n")
                        condition_1 = False
                        condition_2 = False
                else:
                    print("Wrong card number or PIN! \n")
                    break

    elif choice == 1:
        generate_card_numbers()
        print("Your card number: ")
        print(random_card_number)
        print("Your card PIN: ")
        print(random_pin)
        print("")
        id = int(id)
        cur.execute('''INSERT INTO card (id, number, pin, balance)
                        VALUES (?,?,?,?);
                    ''', [(id), (random_card_number), (random_pin), (0)])
        conn.commit()
        card_numbers.append(str(random_card_number))
        associated_pins.append((str(random_pin)))
        associated_balance.append("0")

    elif choice == 0:
        print("Bye! \n")
        condition = False
        break
    else:
        print("Invalid Input \n")
