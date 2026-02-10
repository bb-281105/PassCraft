"""
Personal Information Password Generator
Generates password combinations from user's personal information
"""

import itertools
import re
from datetime import datetime
from typing import List, Set
import json

class PasswordGenerator:
    def __init__(self):
        self.passwords = set()  # Use set to avoid duplicates
        
    def clean_input(self, text: str) -> str:
        """Clean and normalize input text"""
        if not text:
            return ""
        # Remove extra spaces and convert to lowercase
        return text.strip().lower()
    
    def extract_parts(self, name: str) -> dict:
        """Extract different parts from name"""
        name = self.clean_input(name)
        parts = {}
        
        # Full name parts
        name_parts = name.split()
        parts['first'] = name_parts[0] if len(name_parts) > 0 else ""
        parts['last'] = name_parts[-1] if len(name_parts) > 1 else ""
        parts['middle'] = name_parts[1] if len(name_parts) > 2 else ""
        
        # Initials
        parts['first_initial'] = parts['first'][0] if parts['first'] else ""
        parts['last_initial'] = parts['last'][0] if parts['last'] else ""
        
        # Variations
        parts['first_capital'] = parts['first'].capitalize() if parts['first'] else ""
        parts['last_capital'] = parts['last'].capitalize() if parts['last'] else ""
        
        return parts
    
    def parse_dob(self, dob: str) -> dict:
        """Parse date of birth into different formats"""
        dob = self.clean_input(dob)
        parts = {}
        
        try:
            # Try different date formats
            for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']:
                try:
                    date_obj = datetime.strptime(dob, fmt)
                    parts['year'] = str(date_obj.year)
                    parts['year_short'] = parts['year'][2:]  # Last 2 digits
                    parts['month'] = f"{date_obj.month:02d}"
                    parts['month_short'] = str(date_obj.month)
                    parts['day'] = f"{date_obj.day:02d}"
                    parts['day_short'] = str(date_obj.day)
                    parts['full'] = date_obj.strftime('%Y%m%d')
                    parts['reversed'] = date_obj.strftime('%d%m%Y')
                    parts['us'] = date_obj.strftime('%m%d%Y')
                    break
                except ValueError:
                    continue
        except:
            # If parsing fails, try to extract numbers
            numbers = re.findall(r'\d+', dob)
            if numbers:
                parts['numbers'] = numbers
                
        return parts
    
    def parse_phone(self, phone: str) -> dict:
        """Extract different parts from phone number"""
        phone = self.clean_input(phone)
        parts = {}
        
        # Extract only digits
        digits = re.sub(r'\D', '', phone)
        
        if digits:
            parts['full'] = digits
            parts['last4'] = digits[-4:] if len(digits) >= 4 else digits
            parts['last3'] = digits[-3:] if len(digits) >= 3 else digits
            parts['area_code'] = digits[:3] if len(digits) >= 3 else digits
            
            # Split into parts if it's a standard format
            if len(digits) == 10:
                parts['first3'] = digits[:3]
                parts['middle3'] = digits[3:6]
                parts['last4'] = digits[6:]
        
        return parts
    
    def parse_city(self, city: str) -> dict:
        """Extract city variations"""
        city = self.clean_input(city)
        parts = {}
        
        if city:
            parts['full'] = city
            parts['capital'] = city.capitalize()
            parts['upper'] = city.upper()
            
            # Common abbreviations
            abbrev_map = {
                'new york': 'ny',
                'los angeles': 'la',
                'san francisco': 'sf',
                'chicago': 'chi',
                'london': 'ldn',
                'mumbai': 'mum',
                'delhi': 'dlh'
            }
            
            parts['abbrev'] = abbrev_map.get(city, city[:3])
            
        return parts
    
    def generate_simple_combinations(self, data: dict) -> List[str]:
        """Generate simple password combinations"""
        passwords = []
        
        name_parts = data['name']
        dob_parts = data['dob']
        phone_parts = data['phone']
        city_parts = data['city']
        
        # Basic name variations
        if name_parts['first']:
            passwords.extend([
                name_parts['first'],
                name_parts['first_capital'],
                name_parts['first'] + "123",
                name_parts['first'] + "!",
                name_parts['first'] + "@123",
            ])
        
        if name_parts['last']:
            passwords.extend([
                name_parts['last'],
                name_parts['last_capital'],
                name_parts['last'] + "123",
            ])
        
        # Name + numbers
        if name_parts['first'] and dob_parts:
            if 'year' in dob_parts:
                passwords.extend([
                    name_parts['first'] + dob_parts['year'],
                    name_parts['first_capital'] + dob_parts['year'],
                    name_parts['first'] + dob_parts['year_short'],
                    name_parts['last'] + dob_parts['year'],
                    name_parts['first'] + dob_parts['day'],
                    name_parts['first'] + dob_parts['month'] + dob_parts['day'],
                ])
        
        # DOB combinations
        if dob_parts:
            if 'full' in dob_parts:
                passwords.extend([
                    dob_parts['full'],
                    dob_parts['reversed'],
                    dob_parts['us'],
                ])
            
            if 'day' in dob_parts and 'month' in dob_parts and 'year_short' in dob_parts:
                passwords.extend([
                    dob_parts['day'] + dob_parts['month'] + dob_parts['year_short'],
                    dob_parts['month'] + dob_parts['day'] + dob_parts['year_short'],
                ])
        
        # Phone combinations
        if phone_parts:
            if 'full' in phone_parts:
                passwords.append(phone_parts['full'])
            
            if 'last4' in phone_parts:
                passwords.extend([
                    phone_parts['last4'],
                    "123" + phone_parts['last4'],
                    phone_parts['last4'] + "!",
                ])
        
        # City combinations
        if city_parts.get('full'):
            passwords.extend([
                city_parts['full'],
                city_parts['capital'],
                city_parts['abbrev'],
                city_parts['full'] + "123",
            ])
        
        return passwords
    
    def generate_advanced_combinations(self, data: dict) -> List[str]:
        """Generate more complex password combinations"""
        passwords = []
        
        name_parts = data['name']
        dob_parts = data['dob']
        phone_parts = data['phone']
        city_parts = data['city']
        
        # Initialize components
        name_components = []
        number_components = []
        special_components = []
        
        # Collect name components
        if name_parts['first']:
            name_components.extend([name_parts['first'], name_parts['first_capital']])
        if name_parts['last']:
            name_components.extend([name_parts['last'], name_parts['last_capital']])
        if name_parts['first_initial'] and name_parts['last_initial']:
            name_components.append(name_parts['first_initial'] + name_parts['last_initial'])
            name_components.append(name_parts['first_initial'].upper() + name_parts['last_initial'].upper())
        
        # Collect number components from DOB
        if dob_parts:
            if 'year' in dob_parts:
                number_components.extend([dob_parts['year'], dob_parts['year_short']])
            if 'month' in dob_parts:
                number_components.extend([dob_parts['month'], dob_parts['month_short']])
            if 'day' in dob_parts:
                number_components.extend([dob_parts['day'], dob_parts['day_short']])
        
        # Collect phone components
        if phone_parts:
            if 'last4' in phone_parts:
                number_components.append(phone_parts['last4'])
            if 'area_code' in phone_parts:
                number_components.append(phone_parts['area_code'])
        
        # Collect city components
        if city_parts.get('full'):
            special_components.extend([city_parts['full'], city_parts['capital'], city_parts['abbrev']])
        
        # Common suffixes/prefixes
        suffixes = ["", "123", "!", "@123", "123!", "2024", "2025", "007", "111", "999"]
        separators = ["", ".", "_", "-", "@", "#"]
        
        # Generate combinations
        for name in name_components:
            for num in number_components:
                for sep in separators[:3]:  # Use fewer separators for basic combos
                    passwords.append(f"{name}{sep}{num}")
                    
                    # Add suffixes
                    for suffix in suffixes[:5]:
                        passwords.append(f"{name}{sep}{num}{suffix}")
        
        # City + number combinations
        if special_components:
            for city in special_components:
                for num in number_components[:3]:  # Use top 3 number components
                    passwords.extend([
                        f"{city}{num}",
                        f"{city}{num}123",
                        f"{city.upper()}{num}",
                    ])
        
        # Reverse combinations
        for name in name_components:
            for num in number_components:
                if len(num) >= 2:  # Only reverse if number has at least 2 digits
                    passwords.append(f"{num}{name}")
        
        # Special patterns
        if name_parts['first'] and dob_parts.get('year_short'):
            passwords.extend([
                f"{name_parts['first']}{dob_parts['year_short']}{name_parts['last_initial'].upper()}",
                f"{name_parts['first_initial'].upper()}{dob_parts['year_short']}{name_parts['last']}",
                f"{name_parts['first']}.{dob_parts['year_short']}",
                f"{name_parts['first']}_{dob_parts['day']}_{dob_parts['month']}",
            ])
        
        return passwords
    
    def generate_all_combinations(self, data: dict) -> Set[str]:
        """Generate all possible password combinations"""
        all_passwords = set()
        
        # Generate simple combinations
        simple = self.generate_simple_combinations(data)
        all_passwords.update(simple)
        
        # Generate advanced combinations
        advanced = self.generate_advanced_combinations(data)
        all_passwords.update(advanced)
        
        # Add common variations
        variations = self.add_variations(list(all_passwords))
        all_passwords.update(variations)
        
        return all_passwords
    
    def add_variations(self, passwords: List[str]) -> List[str]:
        """Add common variations to passwords"""
        variations = []
        
        for pwd in passwords:
            # Leetspeak substitutions
            leet = pwd
            leet = leet.replace('a', '@').replace('A', '@')
            leet = leet.replace('e', '3').replace('E', '3')
            leet = leet.replace('i', '1').replace('I', '1')
            leet = leet.replace('o', '0').replace('O', '0')
            leet = leet.replace('s', '$').replace('S', '$')
            
            if leet != pwd:
                variations.append(leet)
            
            # Case variations for short passwords
            if len(pwd) <= 8:
                variations.append(pwd.upper())
                variations.append(pwd.capitalize())
            
            # Add special characters
            variations.append(pwd + "!")
            variations.append(pwd + "@")
            variations.append(pwd + "#")
            variations.append(pwd + "123")
            variations.append(pwd + "!")
        
        return variations
    
    def generate_from_info(self, name: str, dob: str, city: str, phone: str) -> List[str]:
        """Main method to generate passwords from user information"""
        print("\n" + "="*60)
        print("PERSONAL INFORMATION PASSWORD GENERATOR")
        print("="*60)
        
        # Parse all information
        print("\n📊 Parsing information...")
        
        name_data = self.extract_parts(name)
        dob_data = self.parse_dob(dob)
        city_data = self.parse_city(city)
        phone_data = self.parse_phone(phone)
        
        data = {
            'name': name_data,
            'dob': dob_data,
            'city': city_data,
            'phone': phone_data
        }
        
        # Display parsed data
        print(f"\n✅ Parsed Data:")
        print(f"   Name: {name_data.get('first', '')} {name_data.get('last', '')}")
        if dob_data.get('year'):
            print(f"   DOB: {dob_data.get('day')}/{dob_data.get('month')}/{dob_data.get('year')}")
        if city_data.get('full'):
            print(f"   City: {city_data.get('full').title()}")
        if phone_data.get('full'):
            print(f"   Phone: {phone_data.get('full')}")
        
        # Generate passwords
        print("\n🔐 Generating password combinations...")
        all_passwords = self.generate_all_combinations(data)
        
        # Convert to list and sort
        password_list = list(all_passwords)
        password_list.sort()
        
        print(f"\n✅ Generated {len(password_list)} unique passwords")
        
        return password_list
    
    def save_to_file(self, passwords: List[str], filename: str = "generated_passwords.txt"):
        """Save generated passwords to a file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Password Dictionary Generated from Personal Information\n")
            f.write(f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Total Passwords: {len(passwords)}\n")
            f.write("#" * 60 + "\n\n")
            
            for i, pwd in enumerate(passwords, 1):
                f.write(f"{pwd}\n")
        
        print(f"💾 Passwords saved to: {filename}")
        return filename

def main():
    """Main program interface"""
    print("\n" + "="*60)
    print("🔐 PERSONAL INFORMATION PASSWORD GENERATOR")
    print("="*60)
    print("\n⚠️  WARNING: This tool demonstrates how attackers can")
    print("   generate passwords from personal information.")
    print("   Use only for educational/security testing purposes.")
    print("="*60)
    
    generator = PasswordGenerator()
    
    while True:
        print("\n📝 Enter personal information (or 'q' to quit):")
        
        name = input("Full Name: ").strip()
        if name.lower() == 'q':
            break
        
        dob = input("Date of Birth (YYYY-MM-DD or DD-MM-YYYY): ").strip()
        if dob.lower() == 'q':
            break
        
        city = input("City: ").strip()
        if city.lower() == 'q':
            break
        
        phone = input("Phone Number: ").strip()
        if phone.lower() == 'q':
            break
        
        # Validate input
        if not all([name, dob, city, phone]):
            print("\n❌ Error: All fields are required!")
            continue
        
        print("\n⏳ Processing...")
        
        try:
            # Generate passwords
            passwords = generator.generate_from_info(name, dob, city, phone)
            
            if not passwords:
                print("\n❌ No passwords generated. Check your input format.")
                continue
            
            # Ask for output filename
            filename = input(f"\n💾 Save to filename (default: 'generated_passwords.txt'): ").strip()
            if not filename:
                filename = "generated_passwords.txt"
            
            # Save to file
            saved_file = generator.save_to_file(passwords, filename)
            
            # Show sample
            print("\n📋 Sample of generated passwords:")
            print("-" * 40)
            for i, pwd in enumerate(passwords[:20], 1):
                print(f"{i:3}. {pwd}")
            
            if len(passwords) > 20:
                print(f"... and {len(passwords) - 20} more")
            
            print(f"\n✅ Successfully generated {len(passwords)} passwords!")
            print(f"📁 Saved to: {saved_file}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        # Ask to continue
        print("\n" + "="*60)
        again = input("\nGenerate more passwords? (y/n): ").strip().lower()
        if again != 'y':
            break
    
    print("\n👋 Goodbye! Remember to use strong, unique passwords!")

if __name__ == "__main__":
    main()