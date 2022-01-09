import os

for i in range(1,16):
    print(i)
    os.rename(f"l{i}",f"leaf{i}")