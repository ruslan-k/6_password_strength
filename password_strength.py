import re
import string
import sys
import getpass


def input_password():
    password = input('Введите ваш пароль: ')
    if not password:
        sys.exit('Введен пустой пароль, попробуй снова.')
    return password

def get_blacklisted_passwords(filepath):
    try:
        with open(filepath) as infile:
            blacklist = infile.read().split("\n")
            return blacklist
    except FileNotFoundError:
        sys.exit('Неверный путь к файлу словаря с наиболее частыми паролями.')

def get_password_strength(password, blacklist):
    score = 0
    while not score:
        if password in blacklist:
            print("Пароль находится в черном списке, попробуйте другой.")
            password = input_password()
        else:
            # plus 1 to score if password lenght >= 4, 2 if >= 8, 3 if >= 14
            score += int(len(password) >= 4) + int(len(password) >= 8) + int(len(password) >= 14)
            # plus 3 to score if password contains both lower-case and upper-case characters
            score += 3 * int(password.lower() != password or password.upper() != password)
            # plus 2 to score if password contains digits
            score += int(len([char for char in password if char in string.digits]) > 0) * 2
            # plus 2 to score if password contains special characters, such as '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
            score += int(len([char for char in password if char in string.punctuation]) > 0) * 2
    return "Оценка степени защиты пароля - {}/10".format(score)


if __name__ == '__main__':
    try:
        blacklist = get_blacklisted_passwords(sys.argv[1])
        password = input_password()
        password_strength = get_password_strength(password, blacklist)
        print(password_strength)
    except IndexError:
        print('Не указан путь к файлу')
