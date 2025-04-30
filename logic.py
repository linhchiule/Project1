from PyQt6.QtWidgets import *

from gui import *
from accounts import *
import csv


class Logic(QMainWindow, Ui_Welcome):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.button_login.clicked.connect(self.login)
        self.button_enter.clicked.connect(self.enter)
        self.button_exit.clicked.connect(self.exit)
        self.button_signup.clicked.connect(self.signup)

        # Hide everything except the login form
        for w in (self.button_enter, self.button_exit, self.button_withdraw,
                  self.button_deposit, self.entry_amount, self.label_amount,
                  self.label_accountbalance, self.label_reenterpin, self.entry_reenterpin):
            w.hide()

    def login(self) -> None:
        """
        This login method is used to validate and access the customer's account in the database.
        """
        # customer login, enter firstname, lastname, and password to verify
        firstname = self.entry_firstname.text().strip()
        lastname = self.entry_lastname.text().strip()
        pin = self.entry_enterpin.text().strip()

        # validate name and PIN. Make sure information entered match with info in the database.
        valid = False
        accountbalance = 0

        if not firstname or not lastname  or not pin:
            self.label_startmessage.setStyleSheet("color: red;")
            self.label_startmessage.setText("Missing information. Please enter First name, Last name and PIN.")
            return

        try:
            with open('customer.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if firstname == row[0] and lastname == row[1] and pin == row[2]:
                        valid = True
                        accountbalance = float(row[3])
                        break
        except FileNotFoundError:
            self.label_startmessage.setStyleSheet("color: red;")
            self.label_startmessage.setText("Incorrect information. Re-enter First name, Last name and PIN.")
            return

        # If customers enter wrong info
        if not valid:
            self.label_startmessage.setStyleSheet("color: red;")
            self.label_startmessage.setText("Incorrect information. Re-enter First name, Last name and PIN.")
            self.entry_firstname.clear()
            self.entry_lastname.clear()
            self.entry_enterpin.clear()
            return

        # Display welcome message after validation

        #Create the account for the customer
        self.user_firstname = firstname
        self.user_lastname = lastname
        self.user_pin = pin
        full_name = f'{firstname} {lastname}'
        self.account = Account(full_name, accountbalance)

        #set display for the customer
        self.label_startmessage.setStyleSheet("color: blue;")
        self.label_startmessage.setText(f'Welcome {firstname} {lastname} !')
        self.label_actionmessage.setStyleSheet("color: blue;")
        self.label_actionmessage.setText('What would you like to do?')
        self.label_accountbalance.setText(f'Your account balance is $ {self.account.get_balance():,.2f}')

        # after authentication, show all available options
        self.button_enter.show()
        self.button_exit.show()
        self.button_withdraw.show()
        self.button_deposit.show()
        self.entry_amount.show()
        self.label_amount.show()
        self.label_accountbalance.show()

    def signup(self) -> None:
        """
        This method is used to sign up for a new customer account.
        """

        # Hide everything except the signup form and change label for signup form
        self.label_firstname.setText('First name *')
        self.label_lastname.setText('Last name *')
        self.label_enterpin.setText('Set a new PIN *')
        self.label_reenterpin.show()
        self.label_enterpin.setText('Enter new PIN *')
        self.entry_reenterpin.show()
        self.button_login.hide()
        self.label_startmessage.hide()
        self.button_enter.hide()
        self.button_exit.hide()
        self.button_withdraw.hide()
        self.button_deposit.hide()
        self.entry_amount.hide()
        self.label_amount.hide()
        self.label_accountbalance.hide()

        #Validate: All fields required
        first_name = self.entry_firstname.text().strip()
        last_name = self.entry_lastname.text().strip()
        pin = self.entry_enterpin.text().strip()
        repin = self.entry_reenterpin.text().strip()


        if first_name == "" or last_name == "" or pin =="":
            self.label_startmessage.show()
            self.label_startmessage.setStyleSheet("color: red;")
            self.label_startmessage.setText("Please enter all required information *")
            return

        # Validate: Names must be letters
        if not first_name.isalpha() or not last_name.isalpha():
            self.label_startmessage.show()
            self.label_startmessage.setStyleSheet("color: red;")
            self.label_startmessage.setText("Names can only contain letters.")
            return

        # Validate: PIN must be number and 4 digits
        if not pin.isdigit() or len(pin) !=4:
            self.label_startmessage.show()
            self.label_startmessage.setStyleSheet("color: red;")
            self.label_startmessage.setText("PIN must be exactly 4 digits.")
            return

        # Validate: PIN must be matched with re-enter PIN
        if pin != repin:
            self.label_startmessage.show()
            self.label_startmessage.setStyleSheet("color: red;")
            self.label_startmessage.setText("PINs do not match. Please try again.")
            return

        # Validate: capitalize first letter
        if first_name and last_name and (not first_name[0].isupper() or not last_name[0].isupper()):
            self.label_startmessage.show()
            self.label_startmessage.setStyleSheet("color: red;")
            self.label_startmessage.setText("First letters should be capitalized.")

        #After validation,create a new account and notify customers to login.
        self.user_firstname = first_name
        self.user_lastname = last_name
        self.user_pin = pin
        self.user_accountbalance = 0.00
        fullname = f'{first_name} {last_name}'
        self.account = Account(fullname, self.user_accountbalance)

        # After validation, update info to the customer database.
        self.updatedata()

        # Set up the new login form
        for w in (self.label_firstname, self.label_lastname,
                  self.label_enterpin, self.entry_firstname,
                  self.entry_lastname, self.entry_enterpin,
                  self.button_login, self.label_startmessage,
                  self.button_signup):
            w.show()

        for w in (
                    self.button_enter,self.button_exit,
                    self.button_withdraw,self.button_deposit,
                    self.entry_amount,self.label_amount,
                    self.label_accountbalance,self.label_reenterpin,
                    self.entry_reenterpin):
                w.hide()

        for i in (self.entry_firstname, self.entry_lastname, self.entry_enterpin):
            i.clear()

        self.label_startmessage.show()
        self.label_startmessage.setStyleSheet("color: blue;")
        self.label_startmessage.setText(f"Account created! Please log in.")
        self.label_firstname.setText("First name")
        self.label_lastname.setText("Last name")
        self.label_enterpin.setText("Enter PIN")

        # After validation, update info to the customer database.
        self.updatedata()



    def enter(self) -> None:
        """
        This method is used to perform action according to the customer's request.
        """
        #Validate amount entry
        amt_text = self.entry_amount.text().strip()
        try:
            amount = float(amt_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            self.label_startmessage.setStyleSheet("color: red;")
            self.label_startmessage.setText('Please enter amount greater than 0.')
            return

        # Validate if either button is checked
        if self.button_withdraw.isChecked():
            success = self.account.withdraw(amount)
            action = 'Withdrawal'
        elif self.button_deposit.isChecked():
            success = self.account.deposit(amount)
            action = 'Deposit'
        else:
            self.label_accountbalance.setStyleSheet("color: red;")
            self.label_accountbalance.setText('Please select Withdrawal or Deposit.')
            return


        # Update data
        if success:
            self.updatedata()
            self.label_accountbalance.setStyleSheet("color: green;")
            self.label_accountbalance.setText(f'Your account balance is $ {self.account.get_balance():,.2f}')
        else:
            self.label_startmessage.setStyleSheet("color: red;")
            self.label_startmessage.setText(f'{action} failed.')
            return

        # Reset input and radiobuttons
        self.entry_amount.clear()
        self.button_withdraw.setChecked(False)
        self.button_deposit.setChecked(False)
        self.label_startmessage.clear()

    def updatedata(self) -> None:
        """
        The method is used to update the customer account balance.or to append a new customer account
        """

        # Load the data
        with open('customer.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        # Identify headers and data rows
        header, data_rows = rows[0], rows[1:]

        # Find & update an existing customer
        found = False
        for row in data_rows:
            fn,ln, p, b = row
            if (fn == self.user_firstname and ln == self.user_lastname and p == self.user_pin):
                row[3] = f'{self.account.get_balance():.2f}'
                found = True
                break  #stop once updated

        # if not found, append a new data record
        if not found:
            data_rows.append([self.user_firstname, self.user_lastname,self.user_pin, f'{self.account.get_balance():.2f}'])

        # Write back header  + all data rows
        with open('customer.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(data_rows)

    def exit(self) -> None:
        """
        Clear all forms and reset the interface back to login state.
        """
        # Clear input fields
        self.entry_firstname.clear()
        self.entry_lastname.clear()
        self.entry_enterpin.clear()
        self.entry_amount.clear()

        # Reset labels
        self.label_startmessage.setStyleSheet("")
        self.label_startmessage.setText("Create a new account?")
        self.label_actionmessage.setStyleSheet("")
        self.label_actionmessage.setText("")
        self.label_accountbalance.setText("")

        # Uncheck radio buttons
        self.button_withdraw.setChecked(False)
        self.button_deposit.setChecked(False)

        # Hide everything except the login form
        for w in (
            self.button_enter,
            self.button_exit,
            self.button_withdraw,
            self.button_deposit,
            self.entry_amount,
            self.label_amount,
            self.label_accountbalance,
            self.label_reenterpin,
            self.entry_reenterpin
        ):
            w.hide()

