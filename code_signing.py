# This script will be used to sign all my files

import os
import gnupg
import getpass
from pathlib import Path
import tqdm


def sign_files_in_folder(folder_path, gpg_key_id, passphrase):
    # Initialize GPG
    gpg = gnupg.GPG()

    # Get list of files in the target folder
    files = [f for f in Path(folder_path).iterdir() if f.is_file()]

    # Progress reporting
    for file in tqdm.tqdm(files, desc="Signing files", unit="file"):
        with open(file, 'rb') as f:
            signed_data = gpg.sign_file(f, keyid=gpg_key_id, passphrase=passphrase, output=str(file) + '.sig', detach=True)
            if not signed_data:
                print(f"Failed to sign {file}")


if __name__ == "__main__":
    # Ask user for the folder path
    folder_path = input("Enter the path to the folder containing files to sign: ").strip()
    if not os.path.isdir(folder_path):
        print("Invalid folder path")
        exit(1)

    # Ask user for the GPG passphrase
    passphrase = getpass.getpass("Enter the GPG key passphrase: ").strip()

    # GPG key ID
    gpg_key_id = "1E04D0A679846BC0"

    # Sign files in the folder
    sign_files_in_folder(folder_path, gpg_key_id, passphrase)
