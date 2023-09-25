import cs50

symbol = "#"
seperator = "  "

while True:
    height = cs50.get_int("Height: ")
    if height >= 1 and height <= 8:
        break


for i in range(1, height + 1):
    blank_spaces = " " * (height - i)
    symbols = symbol * i
    print(blank_spaces + symbols + seperator + symbols)
