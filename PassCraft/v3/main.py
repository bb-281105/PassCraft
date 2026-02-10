"""
Personal Information Password Generator - GUI Version
Generates password combinations from user's personal information
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import itertools
import re
from datetime import datetime
from typing import List, Set
import threading
import os

class PasswordGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Personal Information Password Generator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Configure style
        self.setup_styles()
        
        # Create main container
        self.main_container = ttk.Frame(root, padding="20")
        self.main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_container.columnconfigure(1, weight=1)
        
        # Initialize variables
        self.generated_passwords = []
        self.setup_variables()
        
        # Build UI
        self.create_widgets()
        
        # Center window
        self.center_window()
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.bg_color = "#f0f0f0"
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.success_color = "#27ae60"
        self.warning_color = "#e74c3c"
        
        # Configure styles
        style.configure('Title.TLabel', 
                       font=('Arial', 16, 'bold'), 
                       foreground=self.primary_color)
        
        style.configure('Header.TLabel',
                       font=('Arial', 12, 'bold'),
                       foreground=self.secondary_color)
        
        style.configure('Generate.TButton',
                       font=('Arial', 10, 'bold'),
                       padding=10)
        
        style.configure('Save.TButton',
                       font=('Arial', 10),
                       padding=5)
        
        style.map('Generate.TButton',
                 background=[('active', self.secondary_color)])
        
    def setup_variables(self):
        """Setup tkinter variables"""
        self.name_var = tk.StringVar()
        self.dob_var = tk.StringVar()
        self.city_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.filename_var = tk.StringVar(value="generated_passwords.txt")
        self.status_var = tk.StringVar(value="Ready")
        self.password_count_var = tk.StringVar(value="0 passwords generated")
        self.progress_var = tk.IntVar(value=0)
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title
        title_label = ttk.Label(self.main_container, 
                               text="🔐 Personal Information Password Generator",
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Warning label
        warning_text = "⚠️ WARNING: This tool demonstrates how attackers can generate passwords\n" \
                      "from personal information. Use only for educational/security testing purposes."
        warning_label = ttk.Label(self.main_container, 
                                 text=warning_text,
                                 font=('Arial', 9),
                                 foreground=self.warning_color,
                                 justify=tk.CENTER)
        warning_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Input Frame
        self.create_input_frame()
        
        # Progress Bar
        self.create_progress_section()
        
        # Results Frame
        self.create_results_frame()
        
        # Status Bar
        self.create_status_bar()
        
    def create_input_frame(self):
        """Create input form frame"""
        input_frame = ttk.LabelFrame(self.main_container, 
                                    text="📝 Enter Personal Information",
                                    padding="15")
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(1, weight=1)
        
        # Name
        ttk.Label(input_frame, text="Full Name:", font=('Arial', 10)).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(input_frame, textvariable=self.name_var, 
                              font=('Arial', 10), width=40)
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        name_entry.insert(0, "John Smith")
        
        # Date of Birth
        ttk.Label(input_frame, text="Date of Birth:", font=('Arial', 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        dob_frame = ttk.Frame(input_frame)
        dob_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        dob_entry = ttk.Entry(dob_frame, textvariable=self.dob_var, 
                             font=('Arial', 10), width=20)
        dob_entry.pack(side=tk.LEFT)
        dob_entry.insert(0, "1990-05-15")
        
        ttk.Label(dob_frame, text=" (YYYY-MM-DD or DD-MM-YYYY)", 
                 font=('Arial', 9), foreground="gray").pack(side=tk.LEFT, padx=(10, 0))
        
        # City
        ttk.Label(input_frame, text="City:", font=('Arial', 10)).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        city_entry = ttk.Entry(input_frame, textvariable=self.city_var, 
                              font=('Arial', 10), width=40)
        city_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        city_entry.insert(0, "New York")
        
        # Phone Number
        ttk.Label(input_frame, text="Phone Number:", font=('Arial', 10)).grid(
            row=3, column=0, sticky=tk.W, pady=5)
        phone_entry = ttk.Entry(input_frame, textvariable=self.phone_var, 
                               font=('Arial', 10), width=40)
        phone_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        phone_entry.insert(0, "123-456-7890")
        
        # Button Frame
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(15, 0))
        
        # Generate Button
        generate_btn = ttk.Button(button_frame, 
                                 text="🚀 GENERATE PASSWORDS",
                                 style='Generate.TButton',
                                 command=self.start_generation)
        generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear Button
        clear_btn = ttk.Button(button_frame,
                              text="Clear All",
                              command=self.clear_fields)
        clear_btn.pack(side=tk.LEFT)
        
        # Load Example Button
        example_btn = ttk.Button(button_frame,
                                text="Load Example",
                                command=self.load_example)
        example_btn.pack(side=tk.LEFT, padx=(10, 0))
        
    def create_progress_section(self):
        """Create progress bar section"""
        progress_frame = ttk.Frame(self.main_container)
        progress_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Progress Label
        self.progress_label = ttk.Label(progress_frame, 
                                       text="Progress:",
                                       font=('Arial', 10))
        self.progress_label.pack(side=tk.LEFT)
        
        # Progress Bar
        self.progress_bar = ttk.Progressbar(progress_frame, 
                                          variable=self.progress_var,
                                          maximum=100,
                                          length=400,
                                          mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, padx=(10, 10), fill=tk.X, expand=True)
        
        # Password Count Label
        self.count_label = ttk.Label(progress_frame,
                                    textvariable=self.password_count_var,
                                    font=('Arial', 10, 'bold'),
                                    foreground=self.secondary_color)
        self.count_label.pack(side=tk.LEFT)
        
    def create_results_frame(self):
        """Create results display frame"""
        results_frame = ttk.LabelFrame(self.main_container,
                                      text="📋 Generated Passwords",
                                      padding="10")
        results_frame.grid(row=4, column=0, columnspan=3, 
                          sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Create Text Widget with Scrollbar
        text_frame = ttk.Frame(results_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Text Widget
        self.results_text = tk.Text(text_frame,
                                   wrap=tk.WORD,
                                   yscrollcommand=scrollbar.set,
                                   font=('Courier', 10),
                                   height=15,
                                   bg='white',
                                   relief=tk.SUNKEN,
                                   borderwidth=1)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar.config(command=self.results_text.yview)
        
        # Save Button Frame
        save_frame = ttk.Frame(results_frame)
        save_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Filename Entry
        ttk.Label(save_frame, text="Save as:").pack(side=tk.LEFT)
        filename_entry = ttk.Entry(save_frame, 
                                  textvariable=self.filename_var,
                                  width=30)
        filename_entry.pack(side=tk.LEFT, padx=(5, 5))
        
        # Browse Button
        browse_btn = ttk.Button(save_frame,
                               text="Browse...",
                               command=self.browse_file)
        browse_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Save Button
        self.save_btn = ttk.Button(save_frame,
                                  text="💾 Save to File",
                                  style='Save.TButton',
                                  command=self.save_to_file,
                                  state='disabled')
        self.save_btn.pack(side=tk.LEFT)
        
        # Copy Button
        copy_btn = ttk.Button(save_frame,
                             text="📋 Copy to Clipboard",
                             command=self.copy_to_clipboard)
        copy_btn.pack(side=tk.LEFT, padx=(10, 0))
        
    def create_status_bar(self):
        """Create status bar at bottom"""
        status_frame = ttk.Frame(self.main_container, relief=tk.SUNKEN)
        status_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        status_label = ttk.Label(status_frame,
                                textvariable=self.status_var,
                                relief=tk.SUNKEN,
                                anchor=tk.W)
        status_label.pack(fill=tk.X)
        
    # ===== Password Generation Methods =====
    
    def clean_input(self, text: str) -> str:
        """Clean and normalize input text"""
        if not text:
            return ""
        return text.strip().lower()
    
    def extract_parts(self, name: str) -> dict:
        """Extract different parts from name"""
        name = self.clean_input(name)
        parts = {}
        
        name_parts = name.split()
        parts['first'] = name_parts[0] if len(name_parts) > 0 else ""
        parts['last'] = name_parts[-1] if len(name_parts) > 1 else ""
        parts['middle'] = name_parts[1] if len(name_parts) > 2 else ""
        
        parts['first_initial'] = parts['first'][0] if parts['first'] else ""
        parts['last_initial'] = parts['last'][0] if parts['last'] else ""
        
        parts['first_capital'] = parts['first'].capitalize() if parts['first'] else ""
        parts['last_capital'] = parts['last'].capitalize() if parts['last'] else ""
        
        return parts
    
    def parse_dob(self, dob: str) -> dict:
        """Parse date of birth into different formats"""
        dob = self.clean_input(dob)
        parts = {}
        
        try:
            for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d']:
                try:
                    date_obj = datetime.strptime(dob, fmt)
                    parts['year'] = str(date_obj.year)
                    parts['year_short'] = parts['year'][2:]
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
            numbers = re.findall(r'\d+', dob)
            if numbers:
                parts['numbers'] = numbers
                
        return parts
    
    def parse_phone(self, phone: str) -> dict:
        """Extract different parts from phone number"""
        phone = self.clean_input(phone)
        parts = {}
        
        digits = re.sub(r'\D', '', phone)
        
        if digits:
            parts['full'] = digits
            parts['last4'] = digits[-4:] if len(digits) >= 4 else digits
            parts['last3'] = digits[-3:] if len(digits) >= 3 else digits
            parts['area_code'] = digits[:3] if len(digits) >= 3 else digits
            
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
            
            abbrev_map = {
                'new york': 'ny',
                'los angeles': 'la',
                'san francisco': 'sf',
                'chicago': 'chi',
                'london': 'ldn',
                'mumbai': 'mum',
                'delhi': 'dlh',
                'tokyo': 'tky',
                'paris': 'prs',
                'berlin': 'ber'
            }
            
            parts['abbrev'] = abbrev_map.get(city, city[:3])
            
        return parts
    
    def generate_passwords(self, name: str, dob: str, city: str, phone: str) -> List[str]:
        """Generate passwords from information"""
        # Parse all information
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
        
        # Generate passwords
        passwords = set()
        
        # Basic components
        components = []
        
        # Name components
        if name_data['first']:
            components.append(name_data['first'])
            components.append(name_data['first_capital'])
        if name_data['last']:
            components.append(name_data['last'])
            components.append(name_data['last_capital'])
        if name_data['first_initial'] and name_data['last_initial']:
            components.append(name_data['first_initial'] + name_data['last_initial'])
            components.append(name_data['first_initial'].upper() + name_data['last_initial'].upper())
        
        # Number components
        numbers = []
        if dob_data:
            if 'year' in dob_data:
                numbers.extend([dob_data['year'], dob_data['year_short']])
            if 'month' in dob_data:
                numbers.extend([dob_data['month'], dob_data['month_short']])
            if 'day' in dob_data:
                numbers.extend([dob_data['day'], dob_data['day_short']])
        
        if phone_data:
            if 'last4' in phone_data:
                numbers.append(phone_data['last4'])
            if 'area_code' in phone_data:
                numbers.append(phone_data['area_code'])
            if 'full' in phone_data:
                numbers.append(phone_data['full'])
        
        # City components
        cities = []
        if city_data.get('full'):
            cities.extend([city_data['full'], city_data['capital'], city_data['abbrev']])
        
        # Common suffixes
        suffixes = ["", "123", "!", "@123", "123!", "2024", "2025", "007", "111", "999"]
        separators = ["", ".", "_", "-", "@", "#"]
        
        # Generate combinations
        for comp in components:
            # Simple combinations
            passwords.add(comp)
            
            # With numbers
            for num in numbers[:10]:  # Limit to first 10 numbers
                passwords.add(comp + num)
                for sep in separators[:3]:
                    passwords.add(comp + sep + num)
                    for suffix in suffixes[:5]:
                        passwords.add(comp + sep + num + suffix)
            
            # With cities
            for city in cities:
                passwords.add(comp + city)
                passwords.add(city + comp)
                for sep in separators[:2]:
                    passwords.add(comp + sep + city)
                    for suffix in suffixes[:3]:
                        passwords.add(comp + sep + city + suffix)
        
        # Number-only combinations
        for num in numbers[:5]:
            passwords.add(num)
            for suffix in suffixes:
                passwords.add(num + suffix)
        
        # City + number combinations
        for city in cities:
            for num in numbers[:5]:
                passwords.add(city + num)
                passwords.add(num + city)
        
        # Special patterns
        if name_data['first'] and dob_data.get('year_short'):
            passwords.add(name_data['first'] + dob_data['year_short'])
            passwords.add(name_data['first_capital'] + dob_data['year_short'])
            passwords.add(name_data['first'] + name_data['last_initial'].upper() + dob_data['year_short'])
        
        if name_data['last'] and dob_data.get('year_short'):
            passwords.add(name_data['last'] + dob_data['year_short'])
            passwords.add(name_data['last_capital'] + dob_data['year_short'])
        
        # Leetspeak variations
        leet_passwords = set()
        for pwd in list(passwords)[:200]:  # Limit leetspeak to first 200
            leet = (pwd.replace('a', '@').replace('A', '@')
                       .replace('e', '3').replace('E', '3')
                       .replace('i', '1').replace('I', '1')
                       .replace('o', '0').replace('O', '0')
                       .replace('s', '$').replace('S', '$'))
            if leet != pwd:
                leet_passwords.add(leet)
        
        passwords.update(leet_passwords)
        
        # Convert to sorted list
        password_list = sorted(list(passwords))
        return password_list
    
    # ===== GUI Event Handlers =====
    
    def start_generation(self):
        """Start password generation in a separate thread"""
        # Validate inputs
        if not all([self.name_var.get(), self.dob_var.get(), 
                   self.city_var.get(), self.phone_var.get()]):
            messagebox.showwarning("Missing Information", 
                                 "Please fill in all fields.")
            return
        
        # Disable generate button and enable save button
        self.save_btn.config(state='disabled')
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.password_count_var.set("Generating...")
        self.status_var.set("Generating passwords...")
        self.progress_var.set(0)
        
        # Start generation in separate thread
        thread = threading.Thread(target=self.generate_passwords_thread)
        thread.daemon = True
        thread.start()
    
    def generate_passwords_thread(self):
        """Thread function for password generation"""
        try:
            # Get inputs
            name = self.name_var.get()
            dob = self.dob_var.get()
            city = self.city_var.get()
            phone = self.phone_var.get()
            
            # Update progress
            self.root.after(0, lambda: self.progress_var.set(25))
            self.root.after(0, lambda: self.status_var.set("Parsing information..."))
            
            # Generate passwords
            passwords = self.generate_passwords(name, dob, city, phone)
            
            # Update progress
            self.root.after(0, lambda: self.progress_var.set(75))
            self.root.after(0, lambda: self.status_var.set("Formatting results..."))
            
            # Store passwords
            self.generated_passwords = passwords
            
            # Update UI in main thread
            self.root.after(0, self.update_results_ui, passwords)
            
        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)))
    
    def update_results_ui(self, passwords):
        """Update UI with generated passwords"""
        # Clear text widget
        self.results_text.delete(1.0, tk.END)
        
        # Insert passwords
        for i, pwd in enumerate(passwords, 1):
            self.results_text.insert(tk.END, f"{i:4}. {pwd}\n")
        
        # Update counters
        count = len(passwords)
        self.password_count_var.set(f"{count} passwords generated")
        
        # Update progress and status
        self.progress_var.set(100)
        self.status_var.set(f"Generated {count} passwords successfully!")
        
        # Enable save button
        self.save_btn.config(state='normal')
        
        # Show success message
        if count > 0:
            messagebox.showinfo("Success", 
                              f"Successfully generated {count} passwords!")
    
    def save_to_file(self):
        """Save generated passwords to file"""
        if not self.generated_passwords:
            messagebox.showwarning("No Passwords", 
                                 "No passwords to save. Generate passwords first.")
            return
        
        filename = self.filename_var.get().strip()
        if not filename:
            filename = "generated_passwords.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# Password Dictionary Generated from Personal Information\n")
                f.write(f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Total Passwords: {len(self.generated_passwords)}\n")
                f.write("#" * 60 + "\n\n")
                
                for pwd in self.generated_passwords:
                    f.write(f"{pwd}\n")
            
            self.status_var.set(f"Saved {len(self.generated_passwords)} passwords to {filename}")
            messagebox.showinfo("Success", 
                              f"Passwords saved to:\n{os.path.abspath(filename)}")
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving file: {e}")
    
    def browse_file(self):
        """Open file dialog to choose save location"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=self.filename_var.get()
        )
        if filename:
            self.filename_var.set(filename)
    
    def copy_to_clipboard(self):
        """Copy generated passwords to clipboard"""
        if not self.generated_passwords:
            messagebox.showwarning("No Passwords", 
                                 "No passwords to copy. Generate passwords first.")
            return
        
        # Get first 100 passwords for clipboard
        passwords_to_copy = "\n".join(self.generated_passwords[:100])
        
        self.root.clipboard_clear()
        self.root.clipboard_append(passwords_to_copy)
        
        self.status_var.set("Copied first 100 passwords to clipboard")
        messagebox.showinfo("Copied", "First 100 passwords copied to clipboard!")
    
    def clear_fields(self):
        """Clear all input fields"""
        self.name_var.set("")
        self.dob_var.set("")
        self.city_var.set("")
        self.phone_var.set("")
        self.filename_var.set("generated_passwords.txt")
        self.results_text.delete(1.0, tk.END)
        self.password_count_var.set("0 passwords generated")
        self.progress_var.set(0)
        self.status_var.set("Ready")
        self.save_btn.config(state='disabled')
    
    def load_example(self):
        """Load example data"""
        self.name_var.set("John Smith")
        self.dob_var.set("1990-05-15")
        self.city_var.set("New York")
        self.phone_var.set("123-456-7890")
        self.filename_var.set("john_smith_passwords.txt")
    
    def show_error(self, error_msg):
        """Show error message"""
        self.status_var.set(f"Error: {error_msg}")
        self.progress_var.set(0)
        self.password_count_var.set("Generation failed")
        messagebox.showerror("Error", f"Error generating passwords:\n{error_msg}")

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()