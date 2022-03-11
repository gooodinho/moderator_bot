import random
import string


def get_random_string(length: int):
    # create random sequence that contains both uppercase and lowercase characters
    seq = random.choices(string.ascii_letters, k=length)
    result_string = "".join(seq)
    return result_string
