# master password to access to the text file
# store normal passwords in txt file
# encrypt those stored passwords

from cryptography.fernet import Fernet
import hashlib

def write_key():
    key = Fernet.generate_key()
    with open("key.key", 'wb') as k_file:
        k_file.write(key)

def load_key():
    with open('key.key', 'rb') as file:
        key = file.read()
        return key

def get_fernet_instance(master_pwd):
    key = load_key()
    combined_key = hashlib.sha256(key + master_pwd.encode()).digest()
    return Fernet(combined_key)

master_pwd = input("Enter your master password: ")
write_key()
fer = get_fernet_instance(master_pwd)

def view():
    entered_account_name = input("Enter the name of the account: ")
    with open("store_pwd.txt", "r") as file:
        for line in file:
            line = line.rstrip()  # Remove any trailing whitespace/newline characters
            if '|' in line:
                account_name, encrypted_pwd = line.split("|", 1)  # Split only on the first '|'
                if account_name == entered_account_name:
                    try:
                        decrypted_pwd = fer.decrypt(encrypted_pwd.encode()).decode()
                        print(f"Account name: {account_name}\nPassword: {decrypted_pwd}")
                        return  # Exit after finding and printing the account details
                    except Exception as e:
                        print(f"Error decrypting password: {e}")
                        return
    print("Account not found.")

def add():
    account_name = input("Enter the name of the account: ")
    pwd = input("Enter the password: ")
    with open('store_pwd.txt', 'a') as file:
        file.write(account_name + "|" + str(fer.encrypt(pwd.encode())) + "\n")

while True:
    mode = input("Do you want to add or view a password(add/view)/q to quit: ").lower()
    if mode == "q":
        break
    if mode == "add":
        add()
    elif mode == "view":
        view()
    else:
        print("Invalid input.")
        continue                # To go back to while loop


