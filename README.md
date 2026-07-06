# 🔑 Secure Password Suite

A modular, professional, and cryptographically secure Command Line Interface (CLI) Password Generator and Strength Analyzer written in Python.
This project implements modular programming best practices, computes strength using mathematical information entropy, manages local logging (safely ignored from version control), and provides seamless clipboard integration.

---

## 🚀 Features

- **Cryptographically Secure**: Utilizes Python's native `secrets` module (which retrieves entropy from the operating system) instead of the pseudo-random `random` module.
- **Strict Category Constraints**: Guarantees that at least one character from each selected category (Uppercase, Lowercase, Digits, Symbols) is present in the generated password.
- **Entropy-Based Strength Evaluator**: Measures password safety using mathematical information entropy ($H = L \log_2(R)$) rather than naive length rules.
- **Attractive Visual Terminal UI**: Interactive design employing ANSI colors and Unicode icons, optimized to render correctly on Windows CMD, PowerShell, and Git Bash.
- **Automated Clipboard Copying**: Automatically copies generated passwords to the clipboard using `pyperclip` for a frictionless user experience.
- **Local Persistence Logging**: Appends history logs containing timestamps, passwords, and strength metadata to a local `password_history.txt` file (automatically excluded in Git).
- **Interactive Loops**: Generate multiple passwords, check logs, or clear history without restarting the application.
- **Input Validation & Exception Handling**: Resilient to invalid menu items, lengths outside range, or empty character set selections.

---

## 📂 Folder Structure

```text
├── .gitignore               # Excludes Python bytecode, virtual environments, and history logs
├── README.md                # Extensive project and portfolio documentation
├── generator.py             # Cryptographically secure random password generation logic
├── history.py               # File I/O for saving, reading, and wiping password logs
├── main.py                  # Entrypoint: terminal UI, main loops, and clipboard handling
├── requirements.txt         # External package list (pyperclip)
└── strength.py              # Math modules for password entropy rating
```

---

## 📊 How Strength Analysis Works (Information Entropy)

Unlike standard checkers that verify simple pattern matches (e.g., "contains a number"), this application measures the **Information Entropy** (bits of uncertainty) using:
$$H = L \log_2(R)$$
Where:

- $L$ is the length of the password.
- $R$ is the size of the character pool based on the categories present in the password.

### Pool Sizes ($R$):

- **Lowercase alphabet**: 26 characters
- **Uppercase alphabet**: 26 characters
- **Digits (0-9)**: 10 characters
- **Symbols (Punctuation)**: 32 characters

### Strength Tiers:

- **Weak** ($H < 40$ bits): Vulnerable to basic brute force.
- **Medium** ($40 \le H < 60$ bits): Adequate for non-critical personal accounts.
- **Strong** ($60 \le H < 80$ bits): Recommended for general web applications.
- **Very Strong** ($H \ge 80$ bits): Cryptographically secure; immune to modern brute force attempts.

---

## 🔧 Installation

### 1. Download or clone this repository

Copy the project files into a folder (e.g., `project password`).

### 2. Set up a virtual environment (Recommended)

```bash
python -m venv .venv
```

Activate the environment:

- **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
- **Windows (CMD):** `.venv\Scripts\activate.bat`
- **macOS / Linux:** `source .venv/bin/activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## _(Note: `pyperclip` is the only external package. On Linux, pyperclip might require `xclip` or `xsel` utilities installed via your package manager)._

## 💻 Usage

Launch the generator from your console:

```bash
python main.py
```

### Menu Interface Preview

When started, you are greeted with the interactive dashboard:

```text
=================================================================
      🔑  🛡️   S E C U R E   P A S S W O R D   S U I T E   🛡️  🔑
=================================================================
Main Menu:
  [1] ⚙️  Generate New Password
  [2] 📜  View Password History
  [3] ❌  Clear Password History
  [4] 🚪  Exit Program
👉 Select an option (1-4):
```

---

## 📸 Screenshots Section

Below is a demonstration of how the application looks during execution:

### 1. Dashboard View

Displays the application header, menu actions, and user selection.

### 2. Generator Results

Displays the password in high-contrast cyan, alongside colorized strength indicators:

- **Weak** in `Red`
- **Medium** in `Yellow`
- **Strong** in `Green`
- **Very Strong** in `Bold Green`

---

## 🛠️ Future Improvements

- **Local Log Encryption**: Encrypt the plaintext `password_history.txt` with AES-256 using a master password (via `cryptography`).
- **Ambiguous Character Filter**: Exclude similar-looking characters (e.g., `0`, `O`, `l`, `1`, `I`) to prevent manual transcription errors.
- **Multiple Output Formats**: Allow users to export historical logs in CSV or JSON.
- **GUI Desktop App**: Wrap the modular engine in a GUI using Tkinter, CustomTkinter, or PyQt.

---

## 📄 License

## This project is open-source and licensed under the **MIT License**.

## 👤 Author

Developed by **Pragy** – _Python Developer & Portfolio Designer_.
