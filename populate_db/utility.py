from nanoid import generate

def numeric_nanoid(length=10):
    numbers_only = "0123456789"
    return generate(numbers_only, length)

