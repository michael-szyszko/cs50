import cs50

number = cs50.get_string("Number: ")

digits = list(number)

digit_count = len(digits)

digits_reversed = []
for digit in digits:
    digits_reversed.append(int(digit))
digits_reversed.reverse()

check_sum_1 = 0
check_sum_2 = 0

for i in range(0, digit_count):
    if i % 2 == 0:
        check_sum_1 += digits_reversed[i]
    else:
        multiplied = digits_reversed[i] * 2
        check_sum_2 += (multiplied % 10) + int((multiplied / 10))

digits = digits_reversed
digits.reverse()

if (check_sum_1 + check_sum_2) % 10 != 0:
    print("INVALID")
elif digit_count == 15 and digits[0] == 3 and (digits[1] in [4, 7]):
    print("AMEX")
elif digits[0] == 4 and (digit_count in [13, 16]):
    print("VISA")
elif digits[0] == 5 and digits[1] in [1, 2, 3, 4, 5]:
    print("MASTERCARD")
else:
    print("INVALID")
