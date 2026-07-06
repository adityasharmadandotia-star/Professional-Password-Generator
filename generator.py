"""
Password Generator Module
-------------------------
Provides core logic for generating cryptographically secure random passwords
using the built-in `secrets` module.
"""
import string
import secrets
from typing import List
# Define character sets for each category
UPPERCASE_POOL: str = string.ascii_uppercase
LOWERCASE_POOL: str = string.ascii_lowercase
DIGITS_POOL: str = string.digits
SYMBOLS_POOL: str = string.punctuation
def generate_password(
    length: int,
    use_uppercase: bool,
    use_lowercase: bool,
    use_digits: bool,
    use_symbols: bool
) -> str:
    """
    Generates a cryptographically secure random password based on chosen options.
    Ensures that at least one character from each selected category is included
    to prevent weak choices.
    Args:
        length (int): Desired length of the password (must be between 8 and 100).
        use_uppercase (bool): Include uppercase letters (A-Z).
        use_lowercase (bool): Include lowercase letters (a-z).
        use_digits (bool): Include digits (0-9).
        use_symbols (bool): Include punctuation symbols.
    Returns:
        str: The generated password.
    Raises:
        ValueError: If length is out of bounds or no categories are selected.
    """
    if not (8 <= length <= 100):
        raise ValueError("Password length must be between 8 and 100 characters.")
    # List of selected pools
    selected_pools: List[str] = []
    if use_uppercase:
        selected_pools.append(UPPERCASE_POOL)
    if use_lowercase:
        selected_pools.append(LOWERCASE_POOL)
    if use_digits:
        selected_pools.append(DIGITS_POOL)
    if use_symbols:
        selected_pools.append(SYMBOLS_POOL)
    if not selected_pools:
        raise ValueError("At least one character category must be selected.")
    password_chars: List[str] = []
    # Step 1: Ensure at least one character from each selected category is present
    for pool in selected_pools:
        password_chars.append(secrets.choice(pool))
    # Step 2: Combine all selected pools to draw the remaining characters
    combined_pool: str = "".join(selected_pools)
    remaining_length: int = length - len(password_chars)
    for _ in range(remaining_length):
        password_chars.append(secrets.choice(combined_pool))
    # Step 3: Shuffle securely using secrets.SystemRandom() so positions are unpredictable
    secure_random = secrets.SystemRandom()
    secure_random.shuffle(password_chars)
    return "".join(password_chars)