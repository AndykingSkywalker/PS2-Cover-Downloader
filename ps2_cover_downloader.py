import os
import requests
import re
import pandas as pd
import urllib3
import tkinter as tk
from tkinter import filedialog, messagebox
from ttkbootstrap import Style
from tkinter import ttk  # Import ttk for the progress bar

# Suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_game_title(filename):
    game_title = os.path.splitext(filename)[0]
    game_title = re.sub(r'\s*\(.*?\)', '', game_title).strip()
    return game_title

def fetch_serial_numbers(game_title, csv_path):
    df = pd.read_csv(csv_path, on_bad_lines='warn')
    matching_rows = df[df['Title'].str.contains(game_title, case=False, na=False)]
    serial_numbers = matching_rows['Serial'].tolist()
    return serial_numbers

def download_cover_art(game_title, save_dir='covers', processed_titles=None):
    if processed_titles is None:
        processed_titles = set()
    if game_title in processed_titles:
        return False

    base_url = "https://raw.githubusercontent.com/xlenore/ps2-covers/main/covers/default"
    csv_path = os.path.join("games_table.csv")  # Updated path to local CSV file
    serial_numbers = fetch_serial_numbers(game_title, csv_path)

    if not serial_numbers:
        messagebox.showerror("Error", f"Serial number for {game_title} not found in the CSV.")
        return False

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    downloaded = False
    for serial in serial_numbers:
        img_url = f"{base_url}/{serial}.jpg?raw=true"  # Use raw URL format
        img_name = f"{serial}.jpg"
        img_path = os.path.join(save_dir, img_name)

        if os.path.exists(img_path):
            continue  # Skip without showing an error message

        try:
            img_response = requests.get(img_url, verify=False)
            if img_response.status_code == 200:
                with open(img_path, 'wb') as f:
                    f.write(img_response.content)
                downloaded = True
                processed_titles.add(game_title)
                break  # Stop after downloading the first valid cover
            else:
                messagebox.showerror("Error", f"Failed to download image from {img_url} (Status code: {img_response.status_code})")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request Error: {e}")

    return downloaded

def scan_directory_for_games(directory):
    game_titles = []
    for filename in os.listdir(directory):
        if filename.endswith((".iso", ".bin", ".img", ".nrg", ".mdf")):
            game_title = extract_game_title(filename)
            game_titles.append(game_title)
    return game_titles

def get_matching_serials(directory, csv_path):
    game_titles = scan_directory_for_games(directory)
    all_serial_numbers = {}
    for game_title in game_titles:
        serial_numbers = fetch_serial_numbers(game_title, csv_path)
        if serial_numbers:
            all_serial_numbers[game_title] = serial_numbers
    return all_serial_numbers

def start_download():
    game_directory = game_dir_entry.get()
    save_directory = save_dir_entry.get()

    if not os.path.isdir(game_directory):
        messagebox.showerror("Error", "The provided game directory does not exist.")
        return
    if not os.path.isdir(save_directory):
        messagebox.showerror("Error", "The provided save directory does not exist.")
        return

    game_titles = scan_directory_for_games(game_directory)

    if not game_titles:
        messagebox.showinfo("Info", "No PS2 game files found in the directory.")
        return

    downloaded_count = 0
    processed_titles = set()
    progress_bar['maximum'] = len(game_titles)  # Set the maximum value of the progress bar

    for i, game_title in enumerate(game_titles):
        if download_cover_art(game_title, save_directory, processed_titles):
            downloaded_count += 1
        progress_bar['value'] = i + 1  # Update the progress bar
        root.update_idletasks()  # Force the GUI to update

    messagebox.showinfo("Completed", f"Downloaded {downloaded_count} covers.")

def browse_game_dir():
    directory = filedialog.askdirectory()
    if directory:
        game_dir_entry.delete(0, tk.END)
        game_dir_entry.insert(0, directory)

def browse_save_dir():
    directory = filedialog.askdirectory()
    if directory:
        save_dir_entry.delete(0, tk.END)
        save_dir_entry.insert(0, directory)

# Create the main window
root = tk.Tk()
root.title("PS2 Cover Downloader")

# Apply the ttkbootstrap style
style = Style(theme="darkly")

# Create and place the labels and entries for directories
tk.Label(root, text="Game Directory:").grid(row=0, column=0, padx=10, pady=5)
game_dir_entry = tk.Entry(root, width=50)
game_dir_entry.grid(row=0, column=1, padx=10, pady=5)
game_dir_browse_button = tk.Button(root, text="Browse", command=browse_game_dir)
game_dir_browse_button.grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Covers Output Directory:").grid(row=1, column=0, padx=10, pady=5)
save_dir_entry = tk.Entry(root, width=50)
save_dir_entry.grid(row=1, column=1, padx=10, pady=5)
save_dir_browse_button = tk.Button(root, text="Browse", command=browse_save_dir)
save_dir_browse_button.grid(row=1, column=2, padx=10, pady=5)

# Create and place the Start button
start_button = tk.Button(root, text="Start", command=start_download)
start_button.grid(row=2, column=0, columnspan=3, pady=10)

# Create and place the progress bar
progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
progress_bar.grid(row=3, column=0, columnspan=3, pady=10)

# Run the Tkinter event loop
root.mainloop()