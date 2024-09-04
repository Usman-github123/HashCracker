# HashCracker
This HashCracker, is designed to automate the process of cracking WiFi passwords Offline using the Hashcat tool. The script supports both dictionary-based attacks and number brute-force attacks, targeting .cap and .hc22000 files.

Features:

    File Handling:
        Converts .cap files to .hc22000 format using hcxpcapngtool.
        Processes single files or all files in a folder.
        Moves processed files to a dedicated HashCracked folder.

    Attack Types:
        WordList Attack:
            Supports brute-force attacks using predefined or user-provided wordlists.
        Number Attack:
            Performs a brute-force attack on 8-digit numbers (with options for 9 and 10 digits planned for future implementation).

    Cracked Password Management:
        Automatically displays cracked passwords and saves any new passwords to a HashCrack-Pass.txt file.

    Error Handling:
        Robust error handling for missing tools (hashcat, hcxpcapngtool), invalid paths, and command execution failures.

Usage:

    git clone https://github.com/Usman-github123/HashCracker.git
    cd HashCracker
    chmod +x hashcracker.py
    python3 hashcracker.py

Requirements:

    Kali Linux
    Python 3.10+

Usage:

Run the script, and it will guide you through the steps to choose the type of attack, select files or folders for processing, and manage wordlists. The script is designed to be user-friendly while offering flexibility for both casual and advanced users.

This script is ideal for cybersecurity professionals and enthusiasts working on WiFi password recovery tasks.
