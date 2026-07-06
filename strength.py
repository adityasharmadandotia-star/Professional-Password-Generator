"""
Password Strength Analyzer Module
--------------------------------
Evaluates the security strength of a password using information entropy.
Rather than using arbitrary rules, it determines strength based on the
mathematical probability of guessing the password (bits of entropy).
"""
import math
import string
from typing import Tuple
def calculate_entropy(password: str) -> float:
    """
    Calculates the information entropy of a password in bits.
    Formula: H = L * log2(R)
    where L is the length of the password, and R is the character pool size
    determined by the character types present in the password.
    Args:
        password (str): The password to analyze.
    Returns:
        float: The calculated entropy in bits (rounded to 2 decimal places).
    """
    if not password:
        return 0.0
    length = len(password)
    has_lowercase = False
    has_uppercase = False
    has_digits = False
    has_symbols = False
    # Check which character pools are actually used in the password
    for char in password:
        if char in string.ascii_lowercase:
            has_lowercase = True
        elif char in string.ascii_uppercase:
            has_uppercase = True
        elif char in string.digits:
            has_digits = True
        else:
            # Any punctuation or other characters are treated as symbols
            has_symbols = True
    # Sum the potential range (pool size) of each present category
    pool_size = 0
    if has_lowercase:
        pool_size += 26
    if has_uppercase:
        pool_size += 26
    if has_digits:
        pool_size += 10
    if has_symbols:
        pool_size += 32  # standard punctuation pool size approximation
    # Fallback in case pool size is still 0 (e.g. empty string)
    if pool_size == 0:
        return 0.0
    # H = L * log2(R)
    entropy = length * math.log2(pool_size)
    return round(entropy, 2)
def get_strength_rating(password: str) -> Tuple[float, str]:
    """
    Determines the password strength classification based on its entropy.
    Strength tiers:
    - Weak: < 40 bits (Very easy to brute-force)
    - Medium: 40 to < 60 bits (Moderate security for non-critical accounts)
    - Strong: 60 to < 80 bits (Good security, standard requirements)
    - Very Strong: >= 80 bits (Extremely secure, military-grade protection)
    Args:
        password (str): The password to evaluate.
    Returns:
        Tuple[float, str]: A tuple containing:
            - The calculated entropy (float)
            - The strength label: "Weak", "Medium", "Strong", or "Very Strong"
    """
    entropy = calculate_entropy(password)
    if entropy < 40.0:
        return entropy, "Weak"
    elif entropy < 60.0:
        return entropy, "Medium"
    elif entropy < 80.0:
        return entropy, "Strong"
    else:
        return entropy, "Very Strong"