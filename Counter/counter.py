import time

duration = 5

while duration >= 0:
    if duration == 0:
        print("Time", "Out", sep=" is ")
    else:
        print(duration)
    duration -= 1
    time.sleep(1)