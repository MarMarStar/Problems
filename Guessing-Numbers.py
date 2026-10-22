import random

def guessing_game():
  
  num = random.randint(1, 9)
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
      print("Please input only numbers.")

def main():
  print("Guessing the number game!")

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
  