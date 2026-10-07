"""Safe exact numeric parsing: never evaluate student input as code."""
from fractions import Fraction
import re

def number(value):
    text = str(value).strip().replace('−', '-')
    if len(text) > 80:
        raise ValueError('Answer too long')
    percent = text.endswith('%')
    if percent:
        text = text[:-1].strip()
    # Accept thousands separators only when correctly grouped.
    if ',' in text:
        if not re.fullmatch(r'[+-]?\d{1,3}(,\d{3})+(\.\d+)?', text):
            raise ValueError('Invalid comma grouping')
        text = text.replace(',', '')
    mixed = re.fullmatch(r'([+-]?\d+)\s+(\d+)/(\d+)', text)
    if mixed:
        whole, numerator, denominator = mixed.groups()
        result = abs(Fraction(whole)) + Fraction(int(numerator), int(denominator))
        if whole.startswith('-'):
            result = -result
    elif re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:/\d+)?', text):
        result = Fraction(text)
    else:
        raise ValueError('Use a number, fraction, mixed number or percentage')
    return result / 100 if percent else result

def check_answer(value, expected):
    try:
        return number(value) == number(expected)
    except (ValueError, ZeroDivisionError, TypeError):
        return False
