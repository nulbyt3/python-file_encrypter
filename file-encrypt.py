from cryptography.fernet import Fernet
import os
import sys
import argparse

# Set colors for better outputs
SUCCESS = '\033[92m'
FAIL = '\033[91m'
TEXT = '\033[96m'
RESET = '\033[0m' # Resets color

def generate_key(key_file = 'secret.key'):
    ''' ===== Generate and save a Fernet key ===== '''
    # Generate a key
    generated_key = Fernet.generate_key()
    # Generate and save the key in specified file
    with open(key_file, 'wb') as key_file:
        key_file.write(generated_key)
        print(f'{SUCCESS}[SUCCESS]{RESET} Key has been generated and saved to: {TEXT}{key_file.name}{RESET}')

def load_key(key_file='secret.key'):
    ''' ===== Load the Fernet key from file ===== '''
    try:
        return open(key_file, 'rb').read()
    except FileNotFoundError:
        print(f'{FAIL}[ERROR]{RESET}: Key file {TEXT}"{key_file}"{RESET} not found. Generate a key first.')
        sys.exit(1)

def encrypt_file(filename, key_file='secret.key'): # "filename" is the file that gonna be encrypted
    ''' ===== Encrypt a file using Fernet ===== '''
    # Check if the file we wanna encrypt is exists
    if not os.path.exists(filename):
        print(f'{FAIL}[ERROR]{RESET}: {TEXT}"{filename}"{RESET} does not exists.')
        return
    
    # Load the generated key, if not it will throw an ERROR
    key = load_key(key_file)
    fernet = Fernet(key) # Its gonna create a base64 encoded key
    
    '''
    ===========================================================
        Example for: fernet = Fernet(key)
        
        key = b'Bq0URI7k8eXRTw6JYK8Hlq0YFLra7JYD0vUfQZ5W0z8='
        fernet = Fernet(key)


        encrypted = fernet.encrypt(b"Secret message")
    ===========================================================
    '''
    
    # Read the file that you want to encrypt
    with open(filename, 'rb') as file:
        original_file = file.read()
        
    encyprted_content = fernet.encrypt(original_file)
    
    # Create a new file adding ".encrypted"
    encrypt_filename = filename + '.enc'
    with open(encrypt_filename, 'wb') as encrypted:
        encrypted.write(encyprted_content)
        
    print(f'{SUCCESS}[SUCCESS]{RESET}: File encrypted successfully. Encrypted file: {TEXT}{encrypt_filename}{RESET}.')

def decrypt_file(filename, key_file='secret.key'):
    ''' ===== Decrypt the encrypted file using generated key ( ! new key is not gonna work for decryption ) ===== '''
    # Check if the file we wanna decrypt is exists
    if not os.path.exists(filename):
        print(f'{FAIL}[ERROR]{RESET}: {TEXT}"{filename}{RESET} does not exists."')
        return
    
    # Check if the encrypted file has ".enc" extension
    if not filename.endswith('.enc'):
        print(f'{FAIL}[ERROR]{RESET}: File to decrypt should have {TEXT}".enc"{RESET} extension.')
        return
    
    # Load the generated key, if not it will throw an ERROR
    key = load_key(key_file)
    fernet = Fernet(key)
    
    with open(filename, 'rb') as file:
        encrypted = file.read()
    
    # Try to decrypt the encrypted file
    try:
        decrypted = fernet.decrypt(encrypted)
    except:
        print(f'{FAIL}[FAILED]{RESET}: Decryption failder. Invalid key or corrupted file.')
        return
    
    decrypted_filename = filename[:-4] # Remove ".enc" extension
    with open(decrypted_filename, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
        
    print(f'{SUCCESS}[SUCCESS]{RESET}: File decrypted successfully. Decrypted file: {TEXT}{decrypted_filename}{RESET}.')
    
def main():
    # Initialize the argument parser with a custom description and epilog (footer) text
    parser = argparse.ArgumentParser(
        # Brief description shown at the top of help message
        description='File encryption/decryption tool using Fernet cryptography',
        # Detailed usage examples shown at the bottom of help message
        epilog='Example usage:\n'
               '    Generate key: python3 fernet_tool.py -g\n'
               '    Encrypt file: python3 fernet_tool.py -e file.txt\n'
               '    Decrypt file: python3 fernet_tool.py -d file.txt.enc\n',
        # Preserves formatting (newlines) in the epilog text
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Create a mutually exclusive group for the main operations
    # (user must choose exactly one of these options)    
    group = parser.add_mutually_exclusive_group(required=True)
    # Add argument for key generation (-g or --generate-key)
    # action='store_true' means no additional value needed - just a flag    
    group.add_argument('-g', '--generate-key', action='store_true', help='Generate a new encryption key')
    # Add argument for file encryption (-e or --encrypt)
    # metavar='FILE' shows what to expect after -e in help text    
    group.add_argument('-e', '--encrypt', metavar='FILE', help='Encrypt the specified file')
    # Add argument for file decryption (-d or --decrypt)
    group.add_argument('-d', '--decrypt', metavar='FILE', help='Decrypt the specified file')
    # Add optional argument for custom key file (-k or --key-file)
    # default='secret.key' means this argument is optional    
    parser.add_argument('-k', '--key-file', default='secret.key',
                        help='Specify key file (default: secret.key)'
    )
    
    # Parse the command-line arguments and store them in 'args' object
    args = parser.parse_args()
    
    # Execute the appropriate function based on user input
        
    # If -g/--generate-key was specified    
    if args.generate_key:
        # Call function to generate new key file
        generate_key(args.key_file)
    # If -e/--encrypt was specified with a filename
    elif args.encrypt:
        # Call function to encrypt the specified file
        encrypt_file(args.encrypt, args.key_file)
    # If -d/--decrypt was specified with a filename
    elif args.decrypt:
        # Call function to decrypt the specified file
        decrypt_file(args.decrypt, args.key_file)
    
if __name__ == '__main__':
    main()