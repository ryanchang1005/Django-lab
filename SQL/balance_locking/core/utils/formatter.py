from core.utils.my_math import floor


def format_to_decimal(value, n=0):
    return ('{:,.' + str(n) + 'f}').format(floor(value, n))
