from config import get_number_base

def int_to_str(n: int) -> str:
    base = get_number_base()
    if base == 10:
        return str(n)
    elif base == 12:
        return to_base12(n)
    raise ValueError(f"Unsupported base: {base}")

def str_to_int(s: str) -> int:
    base = get_number_base()
    if base == 10:
        return int(s)
    elif base == 12:
        return from_base12(s)
    raise ValueError(f"Unsupported base: {base}")

def to_base12(n: int) -> str:
    digits = "0123456789↊↋"  # Unicode: ↊ = 10, ↋ = 11
    if n == 0:
        return "0"
    result = ""
    while n > 0:
        result = digits[n % 12] + result
        n //= 12
    return result

def from_base12(s: str) -> int:
    digits = "0123456789↊↋"
    value = 0
    for char in s:
        value = value * 12 + digits.index(char)
    return value
