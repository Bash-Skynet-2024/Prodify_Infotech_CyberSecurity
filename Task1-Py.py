def caesar_encrypt_all(text, shift):
    encrypted = ""
    for char in text:
        encrypted += chr((ord(char) + shift) % 256)  # Shift within byte range
    return encrypted

def caesar_decrypt_all(text, shift):
    decrypted = ""
    for char in text:
        decrypted += chr((ord(char) - shift) % 256)
    return decrypted

def main():
    print("=== Caesar Cipher - Full Character Support ===")
    choice = input("Do you want to (E)ncrypt or (D)ecrypt? ").strip().lower()

    if choice not in ['e', 'd']:
        print("Invalid choice. Use 'E' for encryption or 'D' for decryption.")
        return

    message = input("Enter your message: ")
    try:
        shift = int(input("Enter shift value (0-255): "))
        shift = shift % 256
    except ValueError:
        print("Shift must be a valid integer.")
        return

    if choice == 'e':
        result = caesar_encrypt_all(message, shift)
        print("Encrypted message:")
        print(result)
    else:
        result = caesar_decrypt_all(message, shift)
        print("Decrypted message:")
        print(result)

if __name__ == "__main__":
    main()

