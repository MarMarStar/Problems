print("Number divisibility calculator. Enter 'exit' to quit.")
divisor = []

while True:
  
  num = input("Enter your number here: ")
  
  if num.lower().strip() == 'exit':
    break
    
  divisor.clear()
  
  try:
    num = int(num)
    
    for i in range(1,num+1):
      if num%i == 0:
        divisor.append(i)
        
    print(f"This number is divisible by: {divisor} ")
        
  except:
    print("Error please enter a number.")
