"""
Password History Management Module
----------------------------------
Handles file I/O operations for saving, retrieving, and clearing
generated passwords. The history is saved in `password_history.txt`.
"""
import os
from datetime import datetime
from typing import List
HISTORY_FILE: str = "password_history.txt"
# Security warning written at the top of a newly created history file
FILE_HEADER: str = (
    "===============================================================================\n"
    "🔒 PASSWORD GENERATOR HISTORY LOG\n"
    "⚠️  WARNING: Keep this file secure! It contains generated passwords in plaintext.\n"
    "===============================================================================\n\n"
)
def save_password(password: str, strength_label: str, entropy: float) -> None:
    """
    Saves a generated password, its strength classification, its entropy,
    and the current timestamp to the history file.
    If the file does not exist, it is created with a security warning header.
    Args:
        password (str): The generated password to log.
        strength_label (str): The strength rating (e.g., "Strong").
        entropy (float): The entropy of the password in bits.
    """
    file_exists = os.path.exists(HISTORY_FILE)
    # Prepare log entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Password: {password} | Strength: {strength_label} ({entropy} bits)\n"
    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            if not file_exists:
                f.write(FILE_HEADER)
            f.write(log_entry)
    except IOError as e:
        print(f"\n⚠️  Error writing to history file: {e}")
def get_history() -> List[str]:
    """
    Reads all log entries from the history file, skipping the header.
    Returns:
        List[str]: A list of log entry strings.
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # Filter out the header lines (starting with '=', '🔒', '⚠️', or empty lines)
        log_entries = []
        for line in lines:
            stripped = line.strip()
            if stripped and not any(stripped.startswith(x) for x in ["===", "🔒", "⚠️"]):
                log_entries.append(stripped)
        return log_entries
    except IOError as e:
        print(f"\n⚠️  Error reading history file: {e}")
        return []
def clear_history() -> None:
    """
    Deletes the history file if it exists, effectively clearing all saved entries.
    """
    if os.path.exists(HISTORY_FILE):
        try:
            os.remove(HISTORY_FILE)
        except OSError as e:
            print(f"\n⚠️  Error deleting history file: {e}")
