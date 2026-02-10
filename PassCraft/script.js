// DOM elements
const userInfoForm = document.getElementById('userInfoForm');
const passwordsContainer = document.getElementById('passwordsContainer');
const copyAllBtn = document.getElementById('copyAllBtn');
const downloadBtn = document.getElementById('downloadBtn');
const passwordCountSlider = document.getElementById('passwordCount');
const countValue = document.getElementById('countValue');

// Update slider value display
passwordCountSlider.addEventListener('input', function() {
    countValue.textContent = this.value;
});

// Form submission handler
userInfoForm.addEventListener('submit', function(e) {
    e.preventDefault();
    generatePasswords();
});

// Copy all passwords button
copyAllBtn.addEventListener('click', copyAllPasswords);

// Download button
downloadBtn.addEventListener('click', downloadPasswordList);

// UTILITY FUNCTIONS
function capitalize(text) {
    if (!text) return '';
    return text.charAt(0).toUpperCase() + text.slice(1);
}

function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

function copyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
}

function calculatePasswordStrength(password) {
    let score = 0;
    
    // Length
    if (password.length >= 12) score += 2;
    else if (password.length >= 8) score += 1;
    
    // Has lowercase
    if (/[a-z]/.test(password)) score += 1;
    
    // Has uppercase
    if (/[A-Z]/.test(password)) score += 1;
    
    // Has numbers
    if (/\d/.test(password)) score += 1;
    
    // Has special characters
    if (/[^A-Za-z0-9]/.test(password)) score += 1;
    
    // Determine strength
    if (score >= 5) return 'strong';
    if (score >= 3) return 'medium';
    return 'weak';
}

// PASSWORD GENERATION FUNCTIONS
function generatePasswords() {
    // Get user input values
    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const birthDate = document.getElementById('birthDate').value;
    const petName = document.getElementById('petName').value.trim();
    const favoriteNumber = document.getElementById('favoriteNumber').value;
    const hobby = document.getElementById('hobby').value.trim();
    const city = document.getElementById('city').value.trim();
    const partnerName = document.getElementById('partnerName').value.trim();
    
    // Get options
    const includeSpecial = document.getElementById('includeSpecial').checked;
    const includeNumbers = document.getElementById('includeNumbers').checked;
    const capitalizeFirst = document.getElementById('capitalizeFirst').checked;
    const passwordCount = parseInt(passwordCountSlider.value);
    
    // Validate required fields
    if (!firstName) {
        alert('Please enter at least your first name');
        return;
    }
    
    // Parse birth date
    let birthYear = '';
    let birthMonth = '';
    let birthDay = '';
    
    if (birthDate) {
        const dateObj = new Date(birthDate);
        birthYear = dateObj.getFullYear().toString();
        birthMonth = (dateObj.getMonth() + 1).toString().padStart(2, '0');
        birthDay = dateObj.getDate().toString().padStart(2, '0');
    }
    
    // Prepare data object for pattern replacement
    const userData = {
        firstName: firstName.toLowerCase(),
        lastName: lastName.toLowerCase(),
        birthYear: birthYear,
        birthMonth: birthMonth,
        birthDay: birthDay,
        petName: petName.toLowerCase(),
        favoriteNumber: favoriteNumber,
        hobby: hobby.toLowerCase(),
        city: city.toLowerCase(),
        partnerName: partnerName.toLowerCase(),
        
        // Capitalized versions
        FirstName: capitalize(firstName),
        LastName: capitalize(lastName),
        PetName: capitalize(petName),
        City: capitalize(city),
        Hobby: capitalize(hobby),
        PartnerName: capitalize(partnerName),
        
        // Leet speak versions
        firstNameLeet: applyLeetSpeak(firstName.toLowerCase()),
        lastNameLeet: applyLeetSpeak(lastName.toLowerCase()),
    };
    
    // Get patterns based on options
    const patterns = getPatterns(includeSpecial, includeNumbers, capitalizeFirst);
    
    // Generate passwords
    const passwords = [];
    const usedPasswords = new Set();
    
    // Shuffle patterns to get variety
    const shuffledPatterns = shuffleArray([...patterns]);
    
    // Generate passwords until we reach the desired count or run out of patterns
    for (let pattern of shuffledPatterns) {
        if (passwords.length >= passwordCount) break;
        
        // Generate multiple variations from the same pattern
        const variations = generatePasswordVariations(pattern, userData, includeSpecial);
        
        for (let password of variations) {
            if (passwords.length >= passwordCount) break;
            
            // Only add if not already added and meets criteria
            if (password && !usedPasswords.has(password) && password.length >= 6) {
                // Check if numbers are required
                if (includeNumbers && !/\d/.test(password)) {
                    // Add a number if needed
                    password += favoriteNumber || Math.floor(Math.random() * 100);
                }
                
                passwords.push(password);
                usedPasswords.add(password);
            }
        }
    }
    
    // If we don't have enough passwords, generate some random ones
    if (passwords.length < passwordCount) {
        const needed = passwordCount - passwords.length;
        const extraPasswords = generateExtraPasswords(userData, needed, includeSpecial, includeNumbers);
        extraPasswords.forEach(pwd => {
            if (!usedPasswords.has(pwd)) {
                passwords.push(pwd);
                usedPasswords.add(pwd);
            }
        });
    }
    
    // Display passwords
    displayPasswords(passwords);
    
    // Store passwords for download
    window.lastGeneratedPasswords = passwords;
    window.lastUserData = userData;
}

function generatePasswordVariations(pattern, userData, includeSpecial) {
    const variations = [];
    
    // Replace placeholders in the pattern
    let password = pattern;
    
    // Replace data placeholders
    for (const [key, value] of Object.entries(userData)) {
        const placeholder = `{${key}}`;
        if (password.includes(placeholder) && value) {
            password = password.replace(new RegExp(placeholder, 'g'), value);
        }
    }
    
    // Replace special character placeholder
    if (password.includes('{specialChar}') && includeSpecial) {
        const specialChar = specialCharacters[Math.floor(Math.random() * specialCharacters.length)];
        password = password.replace(/{specialChar}/g, specialChar);
    }
    
    // Add the main variation
    if (password !== pattern) {
        variations.push(password);
    }
    
    // Generate additional variations
    if (userData.favoriteNumber) {
        // Variation with number at the beginning
        variations.push(userData.favoriteNumber + password);
        
        // Variation with number at the end (if not already)
        if (!password.endsWith(userData.favoriteNumber)) {
            variations.push(password + userData.favoriteNumber);
        }
    }
    
    // Add special character variations
    if (includeSpecial) {
        const specialChar = specialCharacters[Math.floor(Math.random() * specialCharacters.length)];
        variations.push(password + specialChar);
        variations.push(specialChar + password);
    }
    
    return variations.filter(p => p && p.length > 0);
}

function generateExtraPasswords(userData, count, includeSpecial, includeNumbers) {
    const extraPasswords = [];
    const components = [
        userData.firstName, userData.lastName, userData.petName,
        userData.hobby, userData.city, userData.partnerName,
        userData.birthYear, userData.favoriteNumber
    ].filter(c => c);
    
    if (components.length === 0) return [];
    
    for (let i = 0; i < count; i++) {
        // Shuffle components
        const shuffled = shuffleArray([...components]);
        
        // Take 2-3 components
        const numComponents = 2 + Math.floor(Math.random() * 2);
        let password = shuffled.slice(0, numComponents).join('');
        
        // Possibly capitalize first letter
        if (Math.random() > 0.5) {
            password = capitalize(password);
        }
        
        // Add special character
        if (includeSpecial && Math.random() > 0.3) {
            const specialChar = specialCharacters[Math.floor(Math.random() * specialCharacters.length)];
            if (Math.random() > 0.5) {
                password += specialChar;
            } else {
                password = specialChar + password;
            }
        }
        
        // Add number if needed
        if (includeNumbers && Math.random() > 0.4) {
            password += userData.favoriteNumber || Math.floor(Math.random() * 1000);
        }
        
        extraPasswords.push(password);
    }
    
    return extraPasswords;
}

// DISPLAY FUNCTIONS
function displayPasswords(passwords) {
    // Clear container
    passwordsContainer.innerHTML = '';
    
    // If no passwords, show empty state
    if (passwords.length === 0) {
        passwordsContainer.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-circle"></i>
                <p>No passwords could be generated with the provided information.</p>
                <p class="small">Try adding more information or adjusting the options.</p>
            </div>
        `;
        updatePasswordStats([]);
        return;
    }
    
    // Add each password
    passwords.forEach((password, index) => {
        const passwordElement = createPasswordElement(password, index);
        passwordsContainer.appendChild(passwordElement);
    });
    
    // Update stats
    updatePasswordStats(passwords);
    
    // Add event listeners to copy buttons
    addCopyEventListeners();
}

function createPasswordElement(password, index) {
    const strength = calculatePasswordStrength(password);
    const strengthClass = `strength-${strength}`;
    const strengthText = strength.charAt(0).toUpperCase() + strength.slice(1);
    
    const div = document.createElement('div');
    div.className = 'password-item';
    div.innerHTML = `
        <div class="password-index">${index + 1}.</div>
        <div class="password-text">${password}</div>
        <div class="password-actions">
            <span class="strength-badge ${strengthClass}">${strengthText}</span>
            <button class="copy-password-btn" data-password="${password}">
                <i class="far fa-copy"></i> Copy
            </button>
        </div>
    `;
    
    return div;
}

function updatePasswordStats(passwords) {
    let strong = 0, medium = 0, weak = 0;
    
    passwords.forEach(password => {
        const strength = calculatePasswordStrength(password);
        if (strength === 'strong') strong++;
        else if (strength === 'medium') medium++;
        else weak++;
    });
    
    document.getElementById('totalCount').textContent = passwords.length;
    document.getElementById('strongCount').textContent = strong;
    document.getElementById('mediumCount').textContent = medium;
    document.getElementById('weakCount').textContent = weak;
}

function addCopyEventListeners() {
    document.querySelectorAll('.copy-password-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const password = this.getAttribute('data-password');
            copyToClipboard(password);
            
            // Visual feedback
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-check"></i> Copied!';
            this.style.backgroundColor = '#27ae60';
            
            setTimeout(() => {
                this.innerHTML = originalText;
                this.style.backgroundColor = '';
            }, 1500);
        });
    });
}

// COPY ALL PASSWORDS FUNCTION
function copyAllPasswords() {
    const passwordElements = document.querySelectorAll('.password-text');
    if (passwordElements.length === 0) {
        alert('No passwords to copy!');
        return;
    }
    
    const allPasswords = Array.from(passwordElements).map(el => el.textContent).join('\n');
    copyToClipboard(allPasswords);
    
    // Visual feedback
    const originalText = copyAllBtn.innerHTML;
    copyAllBtn.innerHTML = '<i class="fas fa-check"></i> All Copied!';
    copyAllBtn.style.backgroundColor = '#27ae60';
    
    setTimeout(() => {
        copyAllBtn.innerHTML = originalText;
        copyAllBtn.style.backgroundColor = '';
    }, 2000);
}

// DOWNLOAD FUNCTION
function downloadPasswordList() {
    if (!window.lastGeneratedPasswords || window.lastGeneratedPasswords.length === 0) {
        alert('No passwords to download! Generate passwords first.');
        return;
    }
    
    const passwords = window.lastGeneratedPasswords;
    const userData = window.lastUserData || {};
    
    // Create text content
    const date = new Date();
    const formattedDate = date.toLocaleDateString('en-IN');
    const formattedTime = date.toLocaleTimeString('en-IN');
    
    let textContent = "===========================================\n";
    textContent += "PASSWORD CRAFTING APP - GENERATED PASSWORDS\n";
    textContent += "===========================================\n\n";
    
    // User information
    textContent += "USER INFORMATION:\n";
    textContent += "-----------------\n";
    if (userData.FirstName) textContent += `First Name: ${userData.FirstName}\n`;
    if (userData.LastName) textContent += `Last Name: ${userData.LastName}\n`;
    if (userData.birthYear) textContent += `Birth Year: ${userData.birthYear}\n`;
    if (userData.PetName) textContent += `Pet Name: ${userData.PetName}\n`;
    if (userData.favoriteNumber) textContent += `Favorite Number: ${userData.favoriteNumber}\n`;
    if (userData.Hobby) textContent += `Hobby: ${userData.Hobby}\n`;
    if (userData.City) textContent += `City: ${userData.City}\n`;
    if (userData.PartnerName) textContent += `Partner: ${userData.PartnerName}\n`;
    textContent += "\n";
    
    // Generation details
    textContent += "GENERATION DETAILS:\n";
    textContent += "-------------------\n";
    textContent += `Date: ${formattedDate}\n`;
    textContent += `Time: ${formattedTime}\n`;
    textContent += `Total Passwords: ${passwords.length}\n\n`;
    
    // Passwords list
    textContent += "GENERATED PASSWORDS:\n";
    textContent += "--------------------\n";
    
    passwords.forEach((pwd, index) => {
        const strength = calculatePasswordStrength(pwd);
        textContent += `${index + 1}. ${pwd} [${strength.toUpperCase()}]\n`;
    });
    
    // Security warning
    textContent += "\n===========================================\n";
    textContent += "SECURITY WARNING:\n";
    textContent += "===========================================\n";
    textContent += "These passwords are generated from personal information\n";
    textContent += "and are easily guessable. DO NOT use them for actual accounts!\n";
    textContent += "This tool is for educational purposes only.\n";
    textContent += "===========================================\n";
    
    // Create download link
    const blob = new Blob([textContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    
    // Create filename
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    const firstName = userData.firstName || 'user';
    a.download = `passwords_${firstName}_${timestamp}.txt`;
    
    // Trigger download
    document.body.appendChild(a);
    a.click();
    
    // Cleanup
    setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }, 100);
    
    // Show confirmation
    showDownloadConfirmation();
}

function showDownloadConfirmation() {
    const confirmation = document.createElement('div');
    confirmation.className = 'download-confirmation';
    confirmation.innerHTML = `
        <i class="fas fa-check-circle"></i>
        <span>Passwords downloaded successfully!</span>
    `;
    
    document.body.appendChild(confirmation);
    
    // Remove after 3 seconds
    setTimeout(() => {
        confirmation.classList.add('fade-out');
        setTimeout(() => {
            if (confirmation.parentNode) {
                document.body.removeChild(confirmation);
            }
        }, 500);
    }, 3000);
}