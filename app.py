#!/usr/bin/env python3

import re
import getpass
import sys

def check_password_strength(password):
    """
    Assess the strength of a password based on various criteria.
    Returns a dictionary containing the assessment results.
    """
    assessment = {
        'length': len(password),
        'has_uppercase': bool(re.search(r'[A-Z]', password)),
        'has_lowercase': bool(re.search(r'[a-z]', password)),
        'has_numbers': bool(re.search(r'\d', password)),
        'has_special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
        'score': 0,
        'feedback': []
    }

    # Score calculation (out of 100)
    if assessment['length'] >= 12:
        assessment['score'] += 40
    elif assessment['length'] >= 8:
        assessment['score'] += 25
    elif assessment['length'] >= 6:
        assessment['score'] += 10

    if assessment['has_uppercase']: assessment['score'] += 15
    if assessment['has_lowercase']: assessment['score'] += 15
    if assessment['has_numbers']: assessment['score'] += 15
    if assessment['has_special']: assessment['score'] += 15

    # Generate feedback
    if assessment['length'] < 8:
        assessment['feedback'].append("Password is too short. Use at least 8 characters.")
    if not assessment['has_uppercase']:
        assessment['feedback'].append("Add uppercase letters (A-Z).")
    if not assessment['has_lowercase']:
        assessment['feedback'].append("Add lowercase letters (a-z).")
    if not assessment['has_numbers']:
        assessment['feedback'].append("Add numbers (0-9).")
    if not assessment['has_special']:
        assessment['feedback'].append("Add special characters (!@#$%^&*(),.?\":{}|<>).")

    # Overall strength assessment
    if assessment['score'] >= 90:
        assessment['strength'] = 'Very Strong'
        assessment['color'] = '\033[92m'  # Green
    elif assessment['score'] >= 70:
        assessment['strength'] = 'Strong'
        assessment['color'] = '\033[94m'  # Blue
    elif assessment['score'] >= 50:
        assessment['strength'] = 'Moderate'
        assessment['color'] = '\033[93m'  # Yellow
    else:
        assessment['strength'] = 'Weak'
        assessment['color'] = '\033[91m'  # Red

    return assessment

def print_password_analysis(assessment):
    """Print a detailed analysis of the password strength."""
    reset_color = '\033[0m'
    color = assessment['color']
    
    print("\n" + "="*50)
    print(f"{color}Password Strength Analysis{reset_color}")
    print("="*50)
    
    print(f"\nStrength: {color}{assessment['strength']}{reset_color}")
    print(f"Score: {color}{assessment['score']}/100{reset_color}")
    
    print("\nCriteria Check:")
    print(f"✓ Length: {assessment['length']} characters")
    print(f"✓ Uppercase letters: {'Yes' if assessment['has_uppercase'] else 'No'}")
    print(f"✓ Lowercase letters: {'Yes' if assessment['has_lowercase'] else 'No'}")
    print(f"✓ Numbers: {'Yes' if assessment['has_numbers'] else 'No'}")
    print(f"✓ Special characters: {'Yes' if assessment['has_special'] else 'No'}")
    
    if assessment['feedback']:
        print(f"\n{color}Suggestions for improvement:{reset_color}")
        for suggestion in assessment['feedback']:
            print(f"• {suggestion}")
    else:
        print(f"\n{color}Great job! Your password meets all criteria!{reset_color}")
    
    print("\n" + "="*50)

def main():
    """Main function to run the password strength checker."""
    print("\nWelcome to the Password Strength Checker!")
    print("Enter 'q' to quit at any time.")
    
    while True:
        try:
            password = getpass.getpass("\nEnter a password to check: ")
            
            if password.lower() == 'q':
                print("\nThank you for using the Password Strength Checker!")
                sys.exit(0)
            
            if not password:
                print("Please enter a password.")
                continue
            
            assessment = check_password_strength(password)
            print_password_analysis(assessment)
            
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    main() 