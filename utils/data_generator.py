import random
import string

from faker import Faker

fake = Faker(["en_US"])
fake.seed_instance(12345)


def generate_first_name():
    return fake.first_name()


def generate_last_name():
    return fake.last_name()


def generate_post_code(length: int = 10) -> str:
    """Generating a random post code with given number of digits"""
    return "".join(random.choices(string.digits, k=length))


def post_code_to_name(post_code: str) -> str:
    """
    Turn the post code to a name with the corresponding algorithm
    1. Split into two-digit numbers
    2. Convert each number to a letter (0=a, 1=b, ..., 25=z)
    3. If the number is > 25, use the remainder of the division by 26
    """
    name = ""

    for i in range(0, len(post_code), 2):
        if i + 1 < len(post_code):
            two_digit = int(post_code[i : i + 2])
        else:
            two_digit = int(post_code[i])

        letter_index = two_digit % 26
        name += chr(ord("a") + letter_index)

    return name


def find_closest_name_to_average(names: list[str]) -> str:
    if not names:
        raise ValueError("Names list cannot be empty")

    name_lengths = [len(name) for name in names]
    average_length = sum(name_lengths) / len(name_lengths)
    closest_name = min(names, key=lambda name: abs(len(name) - average_length))

    return closest_name
