def show_menu():
  print("""Welcome to the ATM Machine. Please choose an option:
 1 to check for balance.
 2 for deposit.
 3 for withdrawal.
 4 to exit. """)

def show_balance(balance):
  print(f"This is your balance {balance}.\n")

def user_deposit(balance):
  print("Please note that the minimum deposit amount is 100 pesos and must be in denominations of 100 pesos. If you wish to cancel the transaction, type 'cancel'.")
  while True:
    deposit = input("Deposit:").strip().lower()
    if deposit == "cancel":
      print("Transaction cancelled.")
      return balance
    
    if not deposit.isdigit():
      print("Invalid input. Please enter a numeric value.")
      continue
    deposit = int(deposit)

    if deposit < 100 or deposit % 100 != 0:
      print("Deposit must be at least 100 pesos AND in a valid denomination of 100.")
      continue

    balance += deposit
    print(f"Successfully deposited {deposit}. New balance is {balance}")
    return balance

def withdraw(balance):
  print("Please note that the minimum withdrawal amount is 100 pesos and must be in denominations of 100 pesos. If you wish to cancel the transaction, type 'cancel'.")
  while True:
    withdrawal = input("Withdraw:").strip().lower()

    if withdrawal == "cancel":
      print("Transaction cancelled.")
      return balance
    
    if not withdrawal.isdigit():
      print("Invalid input. Please enter a numeric value.")
      continue

    withdrawal = int(withdrawal)

    if withdrawal < 100  or withdrawal % 100 != 0: 
      print("Withdrawal must be at least 100 pesos AND in a valid denomination of 100.")
      continue

    if withdrawal > balance:
      print(f"Insufficient balance. Your current balance is {balance}")
      continue

    balance -= withdrawal
    print(f"Successfully withdrawn {withdrawal}. Remaining balance is {balance}")
    return balance

def user_exit():
  print("Exiting program and printing receipt...")

def print_receipt(balance, total_deposit, total_withdrawal):
  print(f"Your remaining balance is {balance}. The amount withdrawn is {total_withdrawal}. The amount deposited is {total_deposit}. Thank you for using our ATM service!")

def verify_pin(correct_pin):
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

def run_atm():
  balance = 5000
  total_deposit = 0
  total_withdrawal = 0
  correct_pin = "1123"

  if not verify_pin(correct_pin):
    return
  
  while True:
  
    show_menu()
    user_choice = input("Choose: ").strip().lower()
    
    if user_choice == "1":
      show_balance(balance)
    elif user_choice == "2":
      new_balance = user_deposit(balance)
      total_deposit += new_balance - balance
      balance = new_balance

    elif user_choice == "3":
      new_balance = withdraw(balance)
      total_withdrawal += balance - new_balance
      balance = new_balance

    elif user_choice == "4":
      user_exit()
      print_receipt(balance, total_deposit, total_withdrawal)
      return
    
    else: 
      print("Invalid option. Try again.")
      continue
    
    while True:
      next_action = input("Please input 1 for another transaction\nor\n2 to exit the program and print receipt:  ").strip()
      if next_action == "2":
        user_exit()
        print_receipt(balance, total_deposit, total_withdrawal)
        return 
      elif next_action == "1":
        break
      else:
        print("Invalid input. Please type '1' or '2'.")

if __name__ == "__main__":
  run_atm()