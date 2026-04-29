import random

allowed_symbols = "+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

while True:
    password_length = int(input("Введите желаемую длину пароля: "))
    if password_length <= 0:
        print("Длина пароля должна быть положительным числом. Попробуйте ещё раз.")
    else:
        break


generated_password = ""

for i in range(password_length):
    random_symbol = random.choice(allowed_symbols)
    generated_password += random_symbol 

print("Сгенерированный пароль:", generated_password)