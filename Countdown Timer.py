import time

seconds = int(input("Enter countdown time in seconds: "))

while seconds:
    mins, secs = divmod(seconds, 60)
    print(f"{mins:02}:{secs:02}", end='\r')
    time.sleep(1)
    seconds -= 1

print("⏳ Time's up!")

