import os
import hashlib
import tkinter as tk
from tkinter import filedialog

def file_hash(filename):
    """Generate hash for a file."""
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicates(directory):
    """Find duplicate files in a directory."""
    duplicates = {}
    for root, dirs, files in os.walk(directory):
        for filename in files:
            full_path = os.path.join(root, filename)
            file_hash_value = file_hash(full_path)
            if file_hash_value in duplicates:
                duplicates[file_hash_value].append(full_path)
            else:
                duplicates[file_hash_value] = [full_path]
    return {k: v for k, v in duplicates.items() if len(v) > 1}

def delete_duplicates(duplicates):
    """Delete duplicate files, keeping only one copy."""
    for duplicate_files in duplicates.values():
        original_file = duplicate_files[0]
        for duplicate_file in duplicate_files[1:]:
            print(f"Deleting duplicate file: {duplicate_file}")
            os.remove(duplicate_file)

def select_folder():
    """Prompt the user to select a folder."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory(title="Select Folder")
    return folder_path

if __name__ == "__main__":
    directory = select_folder()
    if directory:
        print(f"Selected folder: {directory}")
        print("Finding duplicate files...")
        duplicates = find_duplicates(directory)
        if duplicates:
            print("Duplicate files found:")
            for hash_value, files in duplicates.items():
                print(f"Hash: {hash_value}")
                for file in files:
                    print(f"  - {file}")
            delete_duplicates(duplicates)
            print("Duplicates removed successfully.")
        else:
            print("No duplicate files found.")
    else:
        print("No folder selected. Exiting program.")
