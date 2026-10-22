import random

def guessing_game():
  while True:
    user_min = input("Enter your Minimum amount here: ")
    user_max = input("Enter your Maximum amount here: ")
    if user_max.lower() == 'e' or user_min.lower() == 'e':
      print("Exiting program.")
      exit()
      
    try:
      user_min = int(user_min)
      user_max = int(user_max)
      if user_max > user_min:
        break
      else:
        print("Max must be greater than Minimum.")
        
    except ValueError:
      print("Input integers only.")

  num = random.randint(min, max)
  guesses = 0
  
  while True:
    
    user_input = input("Enter your number here (type 'e' to quit): ")
    
    if user_input.lower() == 'e':
      print("Exiting Program.")
      exit()
      
    try:
      user_num = int(user_input)
      guesses += 1

      if user_num > num:
        print("Lower! Try again: ")
      elif user_num < num:
        print("Higher! Try again: ")
      else:
        print(f"You guessed it! The number was {num}. The total times you guessed are {guesses}")
        break
        
    except ValueError:
      print("Input integers only.")

def main():
  print("Guessing the number game! To exit, enter 'e'.")

  while True:
    guessing_game()

    while True:
      next_action = input("Would you like to continue? (Y/N): ").upper()
      
      if next_action == 'Y':
        print("Continuing to play.")
        break
      elif next_action == 'N':
        print("Exiting Program.")
        exit()
      
      else:
        print("Error. Please input Y or N.")
      
if __name__ == "__main__":
  main()
  