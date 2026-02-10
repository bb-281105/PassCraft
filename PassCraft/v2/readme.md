# 🔐 PassCraft
PassCraft is an educational cybersecurity tool that demonstrates how weak passwords can be generated using personal information such as name, date of birth, city, and phone number.

The project highlights why personal data should never be used in passwords and how attackers build targeted password wordlists.

## 📌 Overview

Most real-world password attacks do not rely on random guessing.
Instead, attackers create custom password dictionaries using publicly available or commonly known personal information.

PassCraft simulates this process in a safe and controlled environment by generating hundreds to thousands of realistic password combinations from minimal user input.

## ⚠️ Important Disclaimer

This tool is intended strictly for educational and authorized security testing purposes.

- Do NOT use this tool for illegal or malicious activities
- Only test systems you own or have explicit permission to test
- Use this tool to improve password security awareness
- Always follow ethical hacking guidelines and applicable laws

## ✨ Features

- Smart parsing of personal information
- Generates 800–1500+ realistic password combinations
- Demonstrates common human password patterns
- Optional leetspeak substitutions
- Saves generated passwords to a text file
- Simple and beginner-friendly command-line interface
- Uses only Python standard library

## 📁 Project Structure

passcraft/
├── main.py
├── README.md
├── generated_passwords.txt

### Project Structure Table

| File Name | Description |
|----------|-------------|
| main.py | Core password generation logic |
| requirements.txt | all requirements mentioned |
| README.md | Project documentation |
| generated_passwords.txt | Generated password wordlist |

## 🛠️ Requirements

- Python 3.6 or higher
- No external libraries required

Optional enhancements:
- tqdm (progress bar)
- colorama (colored output)
- pyfiglet (ASCII banners)

## 🚀 Installation

Clone the repository and run the tool:

git clone <repository-url>
cd passcraft
python main.py

## 🎮 Usage

Run the program using:

python main.py

You will be prompted to enter:
- Full name
- Date of birth
- City
- Phone number

## 🧪 Example Input

Full Name: John Smith  
Date of Birth: 1990-05-15  
City: New York  
Phone Number: 123-456-7890

## 📤 Example Output

Generated 1243 unique passwords.

Sample passwords:
john1990
john@1990
smith0515
js1990
newyork123
john7890

All passwords saved to generated_passwords.txt

## 🔧 How It Works

PassCraft generates passwords using common real-world patterns:

- Name + year of birth
- Name + date
- Name + phone digits
- Initials + numbers
- City + numbers
- Special character combinations

## 🛡️ Security Lessons Demonstrated

- Personal information makes passwords predictable
- Attackers prioritize targeted wordlists
- Password reuse increases risk
- Strong passwords should be random and unrelated to personal life

## 💡 Best Practices

DO:
- Use long, random passwords
- Use password managers
- Enable two-factor authentication
- Use unique passwords everywhere

DON'T:
- Use names or birthdates in passwords
- Reuse passwords
- Use short or simple passwords

## 📈 Learning Outcomes

By using PassCraft, you will understand:
- How attackers build password wordlists
- Why personal data-based passwords fail
- How to improve password hygiene
- Basic principles of password security

## ⚠️ Final Disclaimer

Unauthorized access to computer systems is illegal.

This project is intended strictly for educational purposes.
The author assumes no responsibility for misuse.

Hack ethically. Learn responsibly.

