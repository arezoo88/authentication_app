from random import Random


def generate_digit_code(length=6):
    a = Random().randint(pow(10, length - 1), pow(10, length))
    print('code', a)
    return a
