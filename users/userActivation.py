from random import randint
# from users.models import CodeActivation

def get_random_code(count=6):
    code = []
    for n in range(count):
        code.append(randint(1, 9))
    return int("".join(str(v) for v in code))

