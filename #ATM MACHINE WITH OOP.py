  #ATM MACHINE WITH OOP

class ATM:
  def __init__(self, balance=5000, total_deposit=0, total_withdrawal=0, correct_pin="1123"):
    self.balance = balance
    self.total_deposit = total_deposit
    self.total_withdrawal = total_withdrawal
    self.correct_pin = correct_pin

  def show_menu(self):
    print("""Welcome to the ATM Machine. Please choose an option:
    1 to check for balance.
    2 for deposit.
    3 for withdrawal.
    4 to exit. """)

  def show_balance(self):
    print(f"This is your balance {self.balance}.\n")

  def user_deposit(self):
    print("Please note that the minimum deposit amount is 100 pesos and must be in denominations of 100 pesos.\n If you wish to cancel the transaction, type 'cancel'.")
    while True:
      deposit = input("Deposit:").strip().lower()
      if deposit == "cancel":
        print("Transaction cancelled.")
        return self.balance
      
      if not deposit.isdigit():
        print("Invalid input. Please enter a numeric value.")
        continue
      deposit = int(deposit)

      if deposit < 100 or deposit % 100 != 0:
        print("Deposit must be at least 100 pesos AND in a valid denomination of 100.")
        continue

      self.balance += deposit
      self.total_deposit += deposit
      print(f"Successfully deposited {deposit}. New balance is {self.balance}")
      return

  def withdraw(self):
    print("Please note that the minimum withdrawal amount is 100 pesos and must be in denominations of 100 pesos.\n If you wish to cancel the transaction, type 'cancel'.")
    while True:
      withdrawal = input("Withdraw:").strip().lower()

      if withdrawal == "cancel":
        print("Transaction cancelled.")
        return self.balance

      if not withdrawal.isdigit():
        print("Invalid input. Please enter a numeric value.")
        continue

      withdrawal = int(withdrawal)

      if withdrawal < 100  or withdrawal % 100 != 0: 
        print("Withdrawal must be at least 100 pesos AND in a valid denomination of 100.")
        continue

      if withdrawal > self.balance:
        print(f"Insufficient balance. Your current balance is {self.balance}")
        continue

      self.balance -= withdrawal
      self.total_withdrawal += withdrawal
      print(f"Successfully withdrawn {withdrawal}. Remaining balance is {self.balance}")
      return

  def user_exit(self):
    print("Exiting program and printing receipt...")

  def print_receipt(self):
    print(f"Your remaining balance is {self.balance}. The amount withdrawn is {self.total_withdrawal}. The amount deposited is {self.total_deposit}. Thank you for using our ATM service!")

  def verify_pin(self, correct_pin):
    print("ATM PIN System. If you wish to cancel the transaction, type 'cancel'.")
    attempts = 3
    
    while attempts > 0:
      user_pin = input("Please enter your 4-digit PIN: ").strip().lower()
    
      if user_pin == "cancel":
        print("Transaction cancelled. Ejecting card...")
        return False

      if not user_pin:
        print("PIN cannot be empty. Please try again.")
        continue

      if len(user_pin) != 4 or not user_pin.isdigit():
        print("Invalid PIN format. Please enter a 4-digit numeric PIN.")
        continue

      if user_pin == correct_pin:
        print("PIN verified successfully! \n")
        return True
      else:
        attempts -= 1
        print(f"Incorrect PIN. Attempts remaining: {attempts}")
      
    print("Too many incorrect attempts. Your card has been blocked for security.")
    return False

  def run_atm(self):
    if not self.verify_pin(self.correct_pin):
      return
    
    while True:
    
      self.show_menu()
      user_choice = input("Choose: ").strip().lower()
      
      if user_choice == "1":
        self.show_balance()
      elif user_choice == "2":
        self.user_deposit()
      elif user_choice == "3":
        self.withdraw()
      elif user_choice == "4":
        self.user_exit()
        self.print_receipt()
        return
      
      else: 
        print("Invalid option. Try again.")
        continue
      
      while True:
        next_action = input("Please input 1 for another transaction\nor\n2 to exit the program and print receipt:  ").strip()
        if next_action == "2":
          self.user_exit()
          self.print_receipt()
          return 
        elif next_action == "1":
          break
        else:
          print("Invalid input. Please type '1' or '2'.")

if __name__ == "__main__":
  atm = ATM()
  atm.run_atm()