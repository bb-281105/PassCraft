// Special characters to use in passwords
const specialCharacters = ['!', '@', '#', '$', '%', '&', '*', '_', '-', '.', '+', '=', '?'];

// Leet speak substitutions
const leetSubstitutions = {
    'a': '4', 'A': '4',
    'e': '3', 'E': '3',
    'i': '1', 'I': '1',
    'o': '0', 'O': '0',
    's': '5', 'S': '5',
    't': '7', 'T': '7',
    'b': '8', 'B': '8',
    'g': '9', 'G': '9'
};

// Function to apply leet speak to a string
function applyLeetSpeak(text) {
    if (!text) return '';
    let result = '';
    for (let char of text) {
        result += leetSubstitutions[char] || char;
    }
    return result;
}

// Password generation patterns and rules
const passwordPatterns = {
    // Basic combinations
    basic: [
        "{firstName}{birthYear}",
        "{firstName}{favoriteNumber}",
        "{firstName}{petName}",
        "{firstName}{city}",
        "{lastName}{birthYear}",
        "{lastName}{favoriteNumber}",
        "{petName}{birthYear}",
        "{city}{birthYear}",
        "{hobby}{birthYear}",
        "{hobby}{favoriteNumber}",
        "{partnerName}{birthYear}",
        "{partnerName}{favoriteNumber}",
    ],
    
    // With special characters
    withSpecialChars: [
        "{firstName}@{birthYear}",
        "{firstName}#{favoriteNumber}",
        "{firstName}_{petName}",
        "{firstName}.{lastName}{birthYear}",
        "{petName}!{birthYear}",
        "{city}@{favoriteNumber}",
        "{hobby}_{birthYear}",
        "{firstName}{specialChar}{favoriteNumber}",
        "{lastName}{specialChar}{birthYear}",
        "{petName}{specialChar}{city}",
        "{partnerName}{specialChar}{birthYear}",
        "{firstName}{specialChar}{petName}",
    ],
    
    // With capitalization variations
    withCaps: [
        "{FirstName}{birthYear}",
        "{FirstName}{PetName}",
        "{FirstName}{City}{favoriteNumber}",
        "{LastName}{BirthYear}",
        "{City}{BirthYear}",
        "{Hobby}{birthYear}",
        "{FirstName}{LastName}{birthYear}",
        "{PetName}{City}{favoriteNumber}",
        "{PartnerName}{BirthYear}",
        "{FirstName}{Hobby}{favoriteNumber}",
    ],
    
    // Complex combinations
    complex: [
        "{firstName}{birthDay}{birthMonth}",
        "{lastName}{birthMonth}{birthYear}",
        "{petName}{partnerName}{favoriteNumber}",
        "{city}{hobby}{birthYear}",
        "{firstName}{lastName}{city}{favoriteNumber}",
        "{petName}{birthYear}{city}",
        "{hobby}{partnerName}{birthYear}",
        "{firstName}{specialChar}{petName}{favoriteNumber}",
        "{lastName}{specialChar}{city}{birthYear}",
        "{firstName}{lastName}{birthYear}{city}",
    ],
    
    // Number substitutions (leet speak)
    leetSpeak: [
        "{firstName}1337",
        "{firstNameLeet}{birthYear}",
        "{lastNameLeet}{favoriteNumber}",
        "ILove{partnerName}{birthYear}",
        "{hobby}4Life{birthYear}",
        "{city}Dude{favoriteNumber}",
        "{petName}Lover{birthYear}",
        "{firstName}007{favoriteNumber}",
    ]
};

// Function to get all possible password patterns based on options
function getPatterns(includeSpecial, includeNumbers, capitalizeFirst) {
    let patterns = [];
    
    // Always include basic patterns
    patterns = patterns.concat(passwordPatterns.basic);
    
    // Include patterns with special characters if selected
    if (includeSpecial) {
        patterns = patterns.concat(passwordPatterns.withSpecialChars);
    }
    
    // Include patterns with capitalization if selected
    if (capitalizeFirst) {
        patterns = patterns.concat(passwordPatterns.withCaps);
    }
    
    // Always include complex patterns (they're more secure)
    patterns = patterns.concat(passwordPatterns.complex);
    
    // Include leet speak patterns if numbers are included
    if (includeNumbers) {
        patterns = patterns.concat(passwordPatterns.leetSpeak);
    }
    
    return patterns;
}