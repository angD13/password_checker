import pandas as pd
import string

# Load common passwords from CSV
df = pd.read_csv("common_passwords.csv")
COMMON_PASSWORDS = set(df['password'].str.lower())

def estimate_crack_time(password, adjusted_charset_size):
    length = len(password)
    if adjusted_charset_size == 0:
        return "less than a second"
    combinations = adjusted_charset_size ** length
    guesses_per_second = 1_000_000_000  # 1 billion guesses per second
    seconds = combinations / guesses_per_second
    return format_time(seconds)

def format_time(seconds):
    if seconds < 1:
        return "less than a second"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds // 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hours"
    elif seconds < 31_536_000:
        return f"{int(seconds // 86400)} days"
    elif seconds < 3.15e9:
        return f"{int(seconds // 31_536_000)} years"
    else:
        return "millennia"

def check_password(password):
    if password.lower() in COMMON_PASSWORDS:
        return {
            "strength": "Very Weak",
            "crack_time": "Instantly",
            "common": True,
            "warnings": ["This is one of the most common passwords."]
        }

    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    unique_chars = len(set(password))

    charset = 0
    if has_lower:
        charset += 26
    if has_upper:
        charset += 26
    if has_digit:
        charset += 10
    if has_special:
        charset += len(string.punctuation)

    # Score password
    score = 0
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if has_lower:
        score += 1
    if has_upper:
        score += 1
    if has_digit:
        score += 1
    if has_special:
        score += 1
    if unique_chars >= 6:
        score += 1
    if unique_chars >= 10:
        score += 1
    if unique_chars <= 4:
        score -= 2

    if score <= 2:
        strength = "Very Weak"
    elif score <= 4:
        strength = "Weak"
    elif score <= 6:
        strength = "Medium"
    elif score <= 7:
        strength = "Strong"
    else:
        strength = "Very Strong"

    raw_crack_time = estimate_crack_time(password, charset)

    # Adjust strength based on crack time
    def parse_crack_seconds(time_str):
        if "less than a second" in time_str:
            return 0
        if time_str == "millennia":
            return 31_536_000_000 # approx 1,000 years
        units = {
            "seconds": 1,
            "minutes": 60,
            "hours": 3600,
            "days": 86400,
            "years": 31_536_000,
        }
        for unit, multiplier in units.items():
            if unit in time_str:
                try:
                    number = int(time_str.split()[0])
                    return number * multiplier
                except ValueError:
                    return 0
        return 0

    crack_seconds = parse_crack_seconds(raw_crack_time)
    downgrade_thresholds = [
        (60, "Very Weak"),
        (3600, "Weak"),
        (86400, "Medium"),
        (31_536_000, "Strong")
    ]

    strength_levels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
    score_index = strength_levels.index(strength)

    for threshold, min_label in downgrade_thresholds:
        min_index = strength_levels.index(min_label)
        if crack_seconds < threshold and score_index > min_index:
            strength = min_label
            break

    warnings = []
    if length < 8:
        warnings.append("Too short – use at least 8 characters.")
    if unique_chars <= 4:
        warnings.append("Try using more unique characters.")
    if not has_digit:
        warnings.append("Add a number to strengthen your password.")
    if not has_special:
        warnings.append("Add a special character (e.g., !, @, #).")
    if not has_upper:
        warnings.append("Include uppercase letters.")
    if not has_lower:
        warnings.append("Include lowercase letters.")

    return {
        "strength": strength,
        "crack_time": raw_crack_time,
        "common": False,
        "warnings": warnings
    }

# Run in terminal
if __name__ == "__main__":
    pw = input("Enter a password to check: ")
    result = check_password(pw)
    print(result)
    print(f"Password Strength: {result['strength']}")