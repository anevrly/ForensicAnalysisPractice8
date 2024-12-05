import requests
import itertools
import time

def generate_combinations(characters, length):
    """Generate all combinations of a given length using the specified characters."""
    return itertools.product(characters, repeat=length)

def start_bruteforce(server_url, complexity):
    """
    Perform the brute-force attack on the given server URL using the selected password complexity.
    """
    # Set characters and password length based on complexity
    if complexity == 0:
        characters = "0123456789"  # 4 digits
        password_length = 4
    elif complexity == 1:
        characters = "0123456789"  # 5 digits
        password_length = 5
    elif complexity == 2:
        characters = "abcdefghijklmnopqrstuvwxyz"  # 4 letters
        password_length = 4
    elif complexity == 3:
        characters = "abcdefghijklmnopqrstuvwxyz0123456789"  # 4 letters + numbers
        password_length = 4
    elif complexity == 4:
        characters = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"  # letters + numbers + special characters
        password_length = 4
    else:
        print("Invalid complexity level")
        return

    # Generate all combinations for the selected complexity
    combinations = generate_combinations(characters, password_length)
    start_time = time.time()
    attempts = 0
    found = False

    for combo in combinations:
        password = ''.join(combo)
        attempts += 1
        print(f"Attempting password: {password} (Attempt {attempts})")

        # Send the password attempt to the server
        response = requests.post(
            f"{server_url}/check_password",
            data={
                "password": password,
                "complexity": complexity
            }
        )
        
        result = response.json()

        if result.get('result') == "OK":
            found = True
            print(f"Password found: {password}")
            print(f"Total attempts: {attempts}")
            print(f"Time taken: {time.time() - start_time} seconds")
            break

    if not found:
        print(f"Brute-force failed. Total attempts: {attempts}")
        print(f"Time taken: {time.time() - start_time} seconds")

def main():
    # Input the server URL and complexity level
    server_url = input("Enter the server URL (e.g., http://127.0.0.1:8000): ").strip()
    complexity = int(input("Enter the complexity level (0-4): ").strip())

    start_bruteforce(server_url, complexity)

if __name__ == "__main__":
    main()
