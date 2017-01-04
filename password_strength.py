import string
import sys
from getpass import getpass


def input_password():
    password = getpass('Введите ваш пароль: ')
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


def get_score_for_password_length(password):
    return int(len(password) >= 4) + int(len(password) >= 8) + int(len(password) >= 14)


def get_score_for_both_capital_lowercase_chars(password):
    return 3 * int(password.lower() != password or password.upper() != password)


def get_score_for_digits(password):
    return int(len([char for char in password if char in string.digits]) > 0) * 2


def get_score_for_special_chars(password):
    return int(len([char for char in password if char in string.punctuation]) > 0) * 2


def get_password_strength(password, blacklist):
    if password in blacklist:
        sys.exit("Пароль находится в черном списке, попробуйте другой.")
    else:
        score = get_score_for_password_length(password) + get_score_for_both_capital_lowercase_chars(password) + \
                get_score_for_digits(password) + get_score_for_special_chars(password)
    return "Оценка степени защиты пароля - {}/10".format(score)


if __name__ == '__main__':
    try:
        blacklist = get_blacklisted_passwords(sys.argv[1])
        password = input_password()
        password_strength = get_password_strength(password, blacklist)
        print(password_strength)
    except IndexError:
        print('Не указан путь к файлу')
