def show_menu():
  print("""Welcome to the ATM Machine. Please choose an option:
 1 to check for balance.
 2 for deposit.
 3 for withdrawal.
 4 to change pin
 5 to exit. """)

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

def change_pin(correct_pin):
  user_choice = input("Do you want to change your PIN? (yes/no): ").strip().lower()
  if user_choice == "yes":
    while True:
      confirmation = input("Please enter your current PIN to confirm: ").strip()
      if not confirmation.isdigit() or len(confirmation) != 4:
        print("Invalid PIN format. Please enter a 4-digit numeric PIN.")
        continue
      if confirmation != correct_pin:
        print("Incorrect current PIN. PIN change cancelled.")
        return correct_pin
      while True:
        new_pin = input("Enter your new 4-digit PIN: ").strip()
        if len(new_pin) != 4 or not new_pin.isdigit():
          print("Invalid PIN format. Please enter a 4-digit numeric PIN.")
          continue
        confirm_pin = input("Confirm your new PIN: ").strip()
        if new_pin != confirm_pin:
          print("PINs do not match. Please try again.")
          continue
        print("PIN changed successfully!")
        return new_pin
    return correct_pin

  if user_choice == "no":
    print("PIN change cancelled.")
    return correct_pin

def account_number():
  while True:
    acc_num = input("Please enter your 5-digit account number: ").strip()
    if len(acc_num) != 5 or not acc_num.isdigit():
      print("Invalid account number. Please enter a 5-digit numeric account number.")
      continue
    return acc_num

def run_atm():
  accounts = {
    "12345": {"pin": "1234", "balance": 1000},
    "67890": {"pin": "5678", "balance": 500},
    "11345": {"pin": "4321", "balance": 1500},
    "54321": {"pin": "8765", "balance": 2000},
    "98765": {"pin": "9439", "balance": 30000},
    "00001": {"pin": "9203", "balance": 10000000}
  }
  
  total_deposit = 0
  total_withdrawal = 0
  
  if not accounts:
    print("No accounts available. Exiting program.")
    return
  
  while True:
    acc_num = account_number()
    
    if acc_num in accounts:
      correct_pin = accounts[acc_num]["pin"]
      balance = accounts[acc_num]["balance"]
    verified = verify_pin(correct_pin)
    
    if verified:
      break
    else:
      print("Please try again or type 'cancel' to exit.")
      continue
    
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
      correct_pin = change_pin(correct_pin)
    
    elif user_choice == "5":
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