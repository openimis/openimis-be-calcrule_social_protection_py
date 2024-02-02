import random


def generate_unique_code(length):
    allowed_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
    code = ''.join(random.choice(allowed_chars) for _ in range(length))
    return code
