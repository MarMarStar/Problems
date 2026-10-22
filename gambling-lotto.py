import random

print("""Welcome to gambling lotto simulation.
If your number is present in the random numbers, you will win!
  """)

def gambling():
  while True:
    user_input = input("Enter your numbers here (seperate each numbers by a space): ")
      
    a_str = user_input.split()
    low = input("Enter the lower limit: ")
    upper = input("Enter the upper limit: ")
    amount = input("Enter how many numbers: ")
    
    try:
      low = int(low)
      upper = int(upper)
      amount = int(amount)
  
      a = [int(x) for x in a_str]
      
      if low > upper:
        print("Please make sure the lower limit is less than the upper limit.")
      else:
        break
        
    except ValueError:
      print("Please only numbers.")
  
  
  b = [random.randint(low, upper) for _ in range(amount)]
  
  matches = list(set(a).intersection(b))
  
  if len(matches) > 0:
    print(f"Congratulations! You matched {len(matches)} number(s): {matches}")
    print(f"The winning numbers were: {b}")
    print(f"Your numbers were: {a}")
  else:
    print(f"Better luck next time! The numbers are: {b}, while your numbers are {a}")

def main():
  while True:
    gambling()

    while True:
      next_action = input("Would you like to continue? Enter Y/N: ")

      if next_action.upper() == 'Y':
        print("Continuing.")
        break
      elif next_action.upper() == 'N':
        print("Exiting program.")
        sys.exit()
      else:
        print("Invalid input. Please choose Y or N.")

if __name__ == "__main__":
  main()