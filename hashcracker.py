#!/usr/bin/env python3
import subprocess
import os
import shutil

def get_folder_path(prompt):
    """Prompt the user for a folder path and check if the folder exists."""
    while True:
        folder_path = input(prompt)
        if os.path.isdir(folder_path):
            return folder_path
        else:
            print(f"Folder '{folder_path}' does not exist. Please try again.")

def get_file_path(prompt):
    """Prompt the user for a file path and check if the file exists."""
    while True:
        file_path = input(prompt)
        if os.path.isfile(file_path):
            return file_path
        else:
            print('##########################################################')
            print(f"File '{file_path}' does not exist. Please try again.")
            print('##########################################################')

def convert_cap_to_hc22000(cap_file):
    """Convert .cap file to .hc22000 format using hcxpcapngtool."""
    hc22000_file = cap_file.replace('.cap', '.hc22000')
    try:
        convert_command = ['hcxpcapngtool', '-o', hc22000_file, cap_file]
        print(f"Converting {cap_file} to {hc22000_file} using hcxpcapngtool...")
        subprocess.run(convert_command, check=True)
        print("Conversion successful.\n")
        return hc22000_file
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while converting .cap to .hc22000: {e}")
        return None
    except FileNotFoundError:
        print("hcxpcapngtool is not installed or not found in the system PATH.")
        return None

def check_wordlists(wordlists):
    """Check which wordlists exist from the provided list."""
    existing_wordlists = [wordlist for wordlist in wordlists if os.path.isfile(wordlist)]
    if not existing_wordlists:
        print("No valid wordlists found. Please ensure at least one wordlist is available.")
    return existing_wordlists

def show_cracked_passwords(file_path):
    """Run hashcat with the --show option to display cracked passwords."""
    try:
        show_command = ['hashcat', '--show', '-m', '22000', file_path]
        result = subprocess.run(show_command, capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print('----------------------------------------################------------------------------------------------------')
            print("\nCracked Passwords:\n")
            print(result.stdout)
            print('----------------------------------------################------------------------------------------------------')
            # Read existing cracked passwords from file
            existing_passwords = set()
            if os.path.exists('HashCrack-Pass.txt'):
                with open('HashCrack-Pass.txt', 'r') as output_file:
                    existing_passwords = set(line.strip() for line in output_file)

            # Append only new cracked passwords to the file
            new_passwords = [line for line in result.stdout.splitlines() if line not in existing_passwords]
            
            if new_passwords:
                with open('HashCrack-Pass.txt', 'a') as output_file:
                    for password in new_passwords:
                        output_file.write(password + '\n')
                print("\nNew passwords were saved in HashCrack-Pass.txt.")
            else:
                print("No new passwords found to save.")

            return True
        else:
            print("No passwords have been cracked yet.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running hashcat --show: {e}")
        return False
    except FileNotFoundError:
        print("Hashcat is not installed or not found in the system PATH.")
        return False

def run_hashcat(file_path, wordlists):
    """Run the hashcat command with the specified parameters."""
    base_command = [
        'hashcat', '-a', '0', '-m', '22000', '-d', '1,2,3',
        '--opencl-device-types', '1,2', '-o', 'HashCrack-Pass.txt', '--quiet', file_path
    ]
    base_command.extend(wordlists)

    try:
        print(f"Running command: {' '.join(base_command)}\n")
        subprocess.run(base_command, check=True)
        print("Hashcat command executed successfully.\n")
        
        if show_cracked_passwords(file_path):
            move_file_to_hashcracked(file_path)
        
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running hashcat: {e}")
    except FileNotFoundError:
        print("Hashcat is not installed or not found in the system PATH.")

def move_file_to_hashcracked(file_path):
    """Move the file to the HashCracked folder."""
    hashcracked_folder = 'HashCracked'
    if not os.path.exists(hashcracked_folder):
        os.makedirs(hashcracked_folder)
    
    try:
        shutil.move(file_path, os.path.join(hashcracked_folder, os.path.basename(file_path)))
        print(f"Moved {file_path} to {hashcracked_folder}.")
    except Exception as e:
        print(f"Error occurred while moving the file: {e}")

def process_single_cap_file(cap_file_path, wordlists):
    """Process a single .cap file."""
    print(f"Processing file: {cap_file_path}")
    
    # Convert .cap to .hc22000
    hc22000_file_path = convert_cap_to_hc22000(cap_file_path)
    if not hc22000_file_path:
        return  # Exit if conversion fails
    
    # Show any cracked passwords before attempting to crack
    if not show_cracked_passwords(hc22000_file_path):
        run_hashcat(hc22000_file_path, wordlists)

def process_cap_files(folder_path, wordlists):
    """Process all .cap files in the folder."""
    for filename in os.listdir(folder_path):
        if filename.endswith('.cap'):
            cap_file_path = os.path.join(folder_path, filename)
            process_single_cap_file(cap_file_path, wordlists)

def process_hc22000_files(folder_path, wordlists):
    """Process all .hc22000 files in the folder."""
    for filename in os.listdir(folder_path):
        if filename.endswith('.hc22000'):
            hc22000_file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {hc22000_file_path}")
            
            # Show any cracked passwords before attempting to crack
            if not show_cracked_passwords(hc22000_file_path):
                run_hashcat(hc22000_file_path, wordlists)

def number_attack(file_path):
    """Run a number attack with hashcat for an 8-digit number."""
    try:
        command = [
            'hashcat', '-m', '22000', file_path, '-a', '3',
            '--increment', '--increment-min', '8', '--increment-max', '8',
            '?d?d?d?d?d?d?d?d', '-d', '1,2,3', '--opencl-device-types', '1,2',
            '--session=HashCrackNum', '--quiet'
        ]
        print(f"Running command: {' '.join(command)}\n")
        subprocess.run(command, check=True)
        print("Number attack command executed successfully.\n")
        if show_cracked_passwords(file_path):
            move_file_to_hashcracked(file_path)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running number attack: {e}")
    except FileNotFoundError:
        print("Hashcat is not installed or not found in the system PATH.")
        

def Brute_Select_File(file_type):
    if file_type == '1':
        print("\nSelect the file format:")
        print("1. .cap")
        print("2. .hc22000")
        print('----------------------------------------------------------')
        single_type = input("Enter the number for your choice: ").strip()
        print('----------------------------------------------------------')
        if single_type == '1':
            print('#################################################################')
            cap_file_path = get_file_path("Enter the path to the .cap file: ")
            print('#################################################################')
            process_single_cap_file(cap_file_path, existing_wordlists)
        elif single_type == '2':
            hc22000_file_path = get_file_path("Enter the path to the .hc22000 file: ")
            if not show_cracked_passwords(hc22000_file_path):
                run_hashcat(hc22000_file_path, existing_wordlists)
        else:
            print("Invalid input. Please enter '1' for .cap or '2' for .hc22000.")
            return
    elif file_type == '2':
        print("\nSelect the file format:")
        print("1. .cap")
        print("2. .hc22000")
        print('----------------------------------------------------------')
        folder_type = input("Enter the number for your choice: ").strip()
        print('----------------------------------------------------------')
        if folder_type == '1':
            folder_path = get_folder_path("\nEnter the path to the folder containing .cap files: ")
            process_cap_files(folder_path, existing_wordlists)
        elif folder_type == '2':
            folder_path = get_folder_path("\nEnter the path to the folder containing .hc22000 files: ")
            process_hc22000_files(folder_path, existing_wordlists)
        else:
            print("\nInvalid input. Please enter '1' for .cap or '2' for .hc22000.")
            return
    else:
        print("Invalid input. Please enter '1' for Single File or '2' for Folder.")
        return

def main():
    print("############ HashCracker #############")
    print("Select the type of Attack:")
    print("1. WordList Attack")
    print("2. Number Attack")
    print("3. Restore Attacks")
    print('----------------------------------------------------------')
    file_type = input("Enter the number for your choice: ").strip()
    print('----------------------------------------------------------')
    if file_type == '1':
        wordlists = [
            '/usr/share/wordlists/rockyou.txt',
            '/usr/share/wordlists/indian-passwords-length8-20-sorted',
            '/usr/share/wordlists/wifite.txt',
            '/usr/share/wordlists/SecLists/Passwords/WiFi-WPA/probable-v2-wpa-top4800.txt',
            '/usr/share/wordlists/SecLists/Passwords/darkweb2017-top10000.txt',
            '/usr/share/wordlists/SecLists/Passwords/xato-net-10-million-passwords-1000000.txt',
            '/usr/share/wordlists/Airtel_wordlist.txt'
        ]
            
        # Ask user to enter the path of a wordlist
        askword = input("Do you want to add custom wordlist 'y' or 'n': ").strip().lower()
        print('----------------------------------------------------------')
        if askword in ['y', 'yes']:
            user_input = input("Enter the paths of the wordlists you want to add (separated by commas): ")
            new_wordlists = user_input.split(',')
            new_wordlists = [wordlist.strip() for wordlist in new_wordlists]
            # Strip any leading/trailing whitespace from each path
            new_wordlists = [wordlist.strip() for wordlist in new_wordlists]
            wordlists = new_wordlists + wordlists
            # Output the updated wordlists array
            print('--------------------------------------------------------------------------------------------')
            print("Updated wordlists:\n")
            for wordlist in wordlists:
                print(wordlist)
            print('--------------------------------------------------------------------------------------------')
            global existing_wordlists
            existing_wordlists = check_wordlists(wordlists)
            if not existing_wordlists:
                return
        elif askword in ['n', 'no']:
            pass
        print("\nSelect the type of WordList Attack:")
        print("1. Single File BruteForce")
        print("2. Folder BruteForce")
        print('----------------------------------------------------------')
        file_type = input("Enter the number for your choice: ").strip()
        print('----------------------------------------------------------')
        Brute_Select_File(file_type)
    elif file_type == '2':
        print("\nSelect the type of Number Attack:")
        print("1. 8 Digit Number")
        print("2. 9 Digit Number")
        print("3. 10 Digit Number")
        print('----------------------------------------------------------')
        number_attack_type = input("Enter the number for your choice: ").strip()
        print('----------------------------------------------------------')
        if number_attack_type == '1':
            file_path = get_file_path("Enter the path to the .hc22000 file: ")
            number_attack(file_path)
        elif number_attack_type in ('2', '3'):
            print("Number attack for 9 or 10 digits is not yet implemented.")
        else:
            print("\nInvalid input. Please select a valid option.")
    else:
        print("\nInvalid input. Please select an option.")

if __name__ == "__main__":
    main()

