def prime_checker(num):
  if num <= 1:
    print(f"{num} is not a prime number.")
    return
  
  for i in range(2,int(num**0.5) + 1):
    if num%i == 0:
      print(f"{num} is not a prime number.")
      return
    
  print(f"{num} is a prime number!")

def main():

  while True: 
    user_input = input("Enter number here (If you wish to exit, type 'e'): ")

    if user_input == 'e':
      print("Exiting program.")
      break

    try:
      num = int(user_input)
      prime_checker(num)
      
    except ValueError:
      print("Please Enter an Integer.")
    

if __name__ == '__main__':
  main()
