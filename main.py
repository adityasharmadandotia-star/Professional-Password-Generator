"""
Secure Password Generator CLI Application
-----------------------------------------
Main entry point. Coordinates terminal styling, menu flow, user inputs, and
integrates password generation, strength analysis, clipboard actions, and
history logging.
"""
import os
import sys
# Attempt to import pyperclip and warn the user if it is missing
try:
    import pyperclip
except ImportError:
    print("\n❌ Error: The 'pyperclip' library is required to run this application.")
    print("👉 Please install dependencies using: pip install -r requirements.txt\n")
    sys.exit(1)
# Import local modules
from generator import generate_password
from history import HISTORY_FILE, clear_history, get_history, save_password
from strength import get_strength_rating
# ANSI Escape Sequences for terminal styling
RESET: str = "\033[0m"
BOLD: str = "\033[1m"
DIM: str = "\033[2m"
# Foreground colors
RED: str = "\033[91m"
GREEN: str = "\033[92m"
YELLOW: str = "\033[93m"
CYAN: str = "\033[96m"
WHITE: str = "\033[97m"
# Strength-to-color mapping for visually-rich output
STRENGTH_COLORS: dict = {
    "Weak": RED,
    "Medium": YELLOW,
    "Strong": GREEN,
    "Very Strong": BOLD + GREEN
}
def init_terminal() -> None:
    """
    Enables ANSI escape sequence support in Windows Command Prompt and PowerShell.
    On non-Windows systems, this is a no-op.
    """
    if os.name == 'nt':
        os.system('color')
def print_header(title: str) -> None:
    """
    Prints a formatted, bordered header in BOLD CYAN to create a premium UI feel.
    Args:
        title (str): The header text.
    """
    print(f"\n{BOLD}{CYAN}{'='*65}{RESET}")
    print(f"{BOLD}{CYAN}{title.center(65)}{RESET}")
    print(f"{BOLD}{CYAN}{'='*65}{RESET}\n")
def get_bool_input(prompt: str, default: bool = True) -> bool:
    """
    Prompts the user for a Yes/No question and validates the input.
    Args:
        prompt (str): Prompt text to display.
        default (bool): Default return value if user presses Enter directly.
    Returns:
        bool: True for Yes, False for No.
    """
    default_str = "Y/n" if default else "y/N"
    full_prompt = f"{prompt} ({default_str}): "
    while True:
        try:
            choice = input(full_prompt).strip().lower()
            if not choice:
                return default
            if choice in ("y", "yes"):
                return True
            if choice in ("n", "no"):
                return False
            print(f"{YELLOW}⚠️  Invalid input. Please enter 'y' or 'n'.{RESET}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n👋 Operation cancelled.")
            sys.exit(0)
def get_int_input(prompt: str, min_val: int, max_val: int, default: int) -> int:
    """
    Prompts the user for an integer within a range and validates the input.
    Args:
        prompt (str): Prompt text to display.
        min_val (int): Minimum allowed value.
        max_val (int): Maximum allowed value.
        default (int): Default return value if user presses Enter directly.
    Returns:
        int: The validated integer.
    """
    full_prompt = f"{prompt} [{min_val}-{max_val}] (default: {default}): "
    while True:
        try:
            user_input = input(full_prompt).strip()
            if not user_input:
                return default
            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            print(f"{YELLOW}⚠️  Value must be between {min_val} and {max_val}.{RESET}")
        except ValueError:
            print(f"{YELLOW}⚠️  Invalid input. Please enter a valid number.{RESET}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n👋 Operation cancelled.")
            sys.exit(0)
def run_generator_flow() -> None:
    """
    Executes the interactive password generation workflow.
    Prompts the user for configuration, generates the password using cryptographically
    secure random numbers, evaluates security strength (entropy), copies it to
    the clipboard, and logs details to the history file.
    """
    while True:
        print_header("⚙️   PASSWORD GENERATION SETTINGS")
        # Get inputs
        length = get_int_input("📏 Password Length", 8, 100, 16)
        print(f"\n{BOLD}Select Character Categories to Include:{RESET}")
        use_upper = get_bool_input("🔠 Include Uppercase Letters (A-Z)", default=True)
        use_lower = get_bool_input("🔡 Include Lowercase Letters (a-z)", default=True)
        use_digits = get_bool_input("🔢 Include Numbers (0-9)", default=True)
        use_symbols = get_bool_input("🔣 Include Symbols (!@#$)", default=True)
        if not (use_upper or use_lower or use_digits or use_symbols):
            print(f"\n{RED}❌ Error: You must select at least one character category.{RESET}")
            input("\nPress Enter to try again...")
            continue
        # Generate Password
        try:
            password = generate_password(
                length=length,
                use_uppercase=use_upper,
                use_lowercase=use_lower,
                use_digits=use_digits,
                use_symbols=use_symbols
            )
        except ValueError as e:
            print(f"\n{RED}❌ Generation failed: {e}{RESET}")
            input("\nPress Enter to try again...")
            continue
        # Estimate Strength
        entropy, strength_label = get_strength_rating(password)
        color = STRENGTH_COLORS.get(strength_label, WHITE)
        # Output UI
        print(f"\n{BOLD}{GREEN}🎉 Password generated successfully!{RESET}")
        print(f"\n{BOLD}🔑 PASSWORD: {CYAN}{password}{RESET}\n")
        print(f"📊 {BOLD}Strength Report:{RESET}")
        print(f"   ├─ Classification: {color}{BOLD}{strength_label}{RESET}")
        print(f"   └─ Information Entropy: {CYAN}{entropy} bits{RESET}")
        # Clipboard Copy
        try:
            pyperclip.copy(password)
            print(f"\n📋 {GREEN}Password copied to clipboard automatically!{RESET}")
        except Exception as e:
            print(f"\n⚠️  Could not copy to clipboard: {e}")
        # Save Entry
        save_password(password, strength_label, entropy)
        print(f"💾 Saved to {HISTORY_FILE}.")
        # Ask to repeat
        if not get_bool_input("\n🔄 Generate another password?", default=True):
            break
def run_view_history_flow() -> None:
    """
    Reads and displays all history records from the history log.
    Dynamically colorizes strength values in the history list for easier scanning.
    """
    print_header("📜  PASSWORD GENERATION HISTORY")
    logs = get_history()
    if not logs:
        print(f"📜 {YELLOW}No password history logs found.{RESET}")
        print("   Generate a password to start recording history.")
    else:
        print(f"{DIM}Note: History is stored in {HISTORY_FILE}. Keep this file secure!{RESET}\n")
        for log in logs:
            formatted_log = log
            # Find and colorize strength keywords in the text
            for strength_name, color in STRENGTH_COLORS.items():
                target_str = f"Strength: {strength_name}"
                if target_str in formatted_log:
                    formatted_log = formatted_log.replace(
                        target_str,
                        f"Strength: {color}{BOLD}{strength_name}{RESET}"
                    )
            print(f"  {formatted_log}")
        print(f"\n📊 Total entries: {len(logs)}")
    input("\nPress Enter to return to Main Menu...")
def run_clear_history_flow() -> None:
    """
    Deletes the history file after receiving confirmation from the user.
    """
    print_header("❌  CLEAR PASSWORD HISTORY")
    if not os.path.exists(HISTORY_FILE):
        print(f"📜 {YELLOW}No history file exists to clear.{RESET}")
        input("\nPress Enter to return to Main Menu...")
        return
    print(f"{RED}{BOLD}⚠️  WARNING: This will permanently delete all saved history entries.{RESET}")
    confirm = get_bool_input("Are you absolutely sure you want to clear history?", default=False)
    if confirm:
        clear_history()
        print(f"\n❌ {GREEN}Password history cleared successfully!{RESET}")
    else:
        print(f"\n🔄 {YELLOW}Operation cancelled.{RESET}")
    input("\nPress Enter to return to Main Menu...")
def main() -> None:
    """
    Main execution loop. Displays the dashboard menu and handles option selections.
    """
    init_terminal()
    while True:
        print_header("🔑  🛡️   S E C U R E   P A S S W O R D   S U I T E   🛡️  🔑")
        print(f"{BOLD}Main Menu:{RESET}")
        print("  [1] ⚙️  Generate New Password")
        print("  [2] 📜  View Password History")
        print("  [3] ❌  Clear Password History")
        print("  [4] 🚪  Exit Program\n")
        try:
            choice = input("👉 Select an option (1-4): ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{GREEN}👋 Goodbye! Keep your accounts safe! 🛡️{RESET}\n")
            sys.exit(0)
        if choice == "1":
            run_generator_flow()
        elif choice == "2":
            run_view_history_flow()
        elif choice == "3":
            run_clear_history_flow()
        elif choice == "4":
            print(f"\n{GREEN}👋 Thank you for using Secure Password Suite. Keep your accounts safe! 🛡️{RESET}\n")
            sys.exit(0)
        else:
            print(f"\n{RED}⚠️  Invalid selection. Please choose an option between 1 and 4.{RESET}")
            input("\nPress Enter to continue...")
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n\n{GREEN}👋 Program interrupted. Keep your accounts safe! 🛡️{RESET}\n")
        sys.exit(0)
