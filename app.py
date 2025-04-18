from PIL import Image
import random
import os

# Define a key for XOR operation (it should be consistent for encryption and decryption)
KEY = 123  # Random key, you can change this for stronger encryption
RANDOM_SEED = 42  # Used for deterministic shuffling (same shuffle for both encryption and decryption)

def xor_pixel(pixel, key):
    """Perform XOR operation on the RGB values of a pixel."""
    return (
        pixel[0] ^ key,  # XOR the red channel
        pixel[1] ^ key,  # XOR the green channel
        pixel[2] ^ key   # XOR the blue channel
    )

def encrypt_image(image_path, output_path):
    """Encrypt an image by XORing each pixel and shuffling pixels."""
    img = Image.open(image_path)
    pixels = img.load()

    # Set a random seed for pixel shuffling (same seed for encryption and decryption)
    random.seed(RANDOM_SEED)
    pixel_list = []

    # Store all pixels with their positions
    for i in range(img.width):
        for j in range(img.height):
            pixel_list.append((i, j, pixels[i, j]))

    # Shuffle pixel list to randomly reorder the pixels
    random.shuffle(pixel_list)

    # Apply XOR encryption and shuffled pixel positions
    for idx, (i, j, pixel) in enumerate(pixel_list):
        pixels[i, j] = xor_pixel(pixel, KEY)

    img.save(output_path)
    print(f"Image encrypted and saved as {output_path}")

    # Save the shuffled pixel indices for later decryption
    with open(output_path + '.map', 'w') as f:
        for idx, (i, j, _) in enumerate(pixel_list):
            f.write(f"{i},{j},{idx}\n")

def decrypt_image(image_path, output_path):
    """Decrypt an image by XORing each pixel and reversing pixel shuffle."""
    img = Image.open(image_path)
    pixels = img.load()

    # Read the shuffled pixel positions map
    map_file = image_path + '.map'
    if not os.path.exists(map_file):
        print("Map file not found. Cannot decrypt.")
        return

    # Create a position lookup dictionary
    position_lookup = {}
    with open(map_file, 'r') as f:
        for line in f:
            i, j, idx = map(int, line.strip().split(','))
            position_lookup[(i, j)] = idx

    # Store original pixels and their positions
    pixel_list = []
    for i in range(img.width):
        for j in range(img.height):
            pixel_list.append((i, j, pixels[i, j]))

    # Sort based on the original position index
    sorted_pixel_list = sorted(pixel_list, key=lambda x: position_lookup[(x[0], x[1])])

    # Apply XOR decryption and restore original pixel positions
    for idx, (i, j, pixel) in enumerate(sorted_pixel_list):
        pixels[i, j] = xor_pixel(pixel, KEY)

    img.save(output_path)
    print(f"Image decrypted and saved as {output_path}")

def main():
    print("Enhanced Image Encryption Tool with XOR + Pixel Shuffling")
    print("1. Encrypt an Image")
    print("2. Decrypt an Image")
    choice = input("Enter your choice (1/2): ")

    if choice not in ['1', '2']:
        print("Invalid choice.")
        return

    image_path = input("Enter path to image file: ")

    if not os.path.exists(image_path):
        print("Image file does not exist.")
        return

    output_path = input("Enter output file name (with extension): ")

    if choice == '1':
        encrypt_image(image_path, output_path)
    else:
        decrypt_image(image_path, output_path)

if __name__ == "__main__":
    main()
