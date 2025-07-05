import random
secret_number = random.randint(1,100)
print("Welcome to the number guessing game!!")
print("let me guess a number between(1-100)")
while True:
    guess= int(input("enter your guess:"))
    if guess > secret_number:
        print("too high guess!! TRY AGAIN!!!!")
    elif guess < secret_number:
        print("too low guess!! TRY AGAIN!!!!")  
    else:
        print("WOW... YOU GUESSED IT RIGHT...YOU WON")
        break
              