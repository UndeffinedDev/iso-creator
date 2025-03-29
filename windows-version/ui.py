import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os
import sys

def get_iso_creator_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, "iso-creator.exe")
    return os.path.join(os.path.dirname(__file__), "iso-creator.exe")

def select_files():
    files = filedialog.askopenfilenames(title="Select files or folders")
    for file in files:
        file_listbox.insert(tk.END, file)

def select_folders():
    folder = filedialog.askdirectory(title="Select folder")
    if folder:
        file_listbox.insert(tk.END, folder)

def clear_list():
    file_listbox.delete(0, tk.END)

def generate_command():
    iso_creator_path = get_iso_creator_path()

    if not os.path.exists(iso_creator_path):
        messagebox.showerror("Error", f"Could not find iso-creator.exe at {iso_creator_path}")
        return ""

    label = label_entry.get().strip()
    extract_zip = "-z" if extract_var.get() else ""
    files = " ".join(f'"{file_listbox.get(i)}"' for i in range(file_listbox.size()))
    output_iso = output_entry.get().strip()

    if not files:
        messagebox.showerror("Error", "You must select at least one file or folder.")
        return ""

    if not output_iso.lower().endswith(".iso"):
        output_iso += ".iso"
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_iso)

    return f'"{iso_creator_path}" -l "{label}" {extract_zip} {files} "{output_iso}"'

def run_command():
    command = generate_command()
    if not command:
        return
    
    root.title("ISO Creator UI - Converting...")

    thread = threading.Thread(target=execute_command, args=(command,))
    thread.start()

def execute_command(command):
    set_output_state("normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Running: {command}\n\n")
    set_output_state("disabled")
    
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def read_output(stream, tag=""):
        for line in stream:
            set_output_state("normal")
            output_text.insert(tk.END, line, tag)
            output_text.update()
            set_output_state("disabled")

    stdout_thread = threading.Thread(target=read_output, args=(process.stdout,))
    stderr_thread = threading.Thread(target=read_output, args=(process.stderr, "error"))

    stdout_thread.start()
    stderr_thread.start()

    process.wait()
    stdout_thread.join()
    stderr_thread.join()

    root.title("ISO Creator UI")
    
    messagebox.showinfo("Process Completed", "ISO created successfully" if process.returncode == 0 else "An error occurred while creating the ISO")

def set_output_state(state):
    output_text.config(state=state)

# Main window configuration
root = tk.Tk()
root.title("ISO Creator UI")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=5)

file_listbox = tk.Listbox(frame, width=80, height=10)
file_listbox.pack(side=tk.LEFT)
scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=file_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
file_listbox.config(yscrollcommand=scrollbar.set)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Add Files", command=select_files).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Add Folders", command=select_folders).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Clear List", command=clear_list).pack(side=tk.LEFT, padx=5)

options_frame = tk.Frame(root)
options_frame.pack(pady=5)

extract_var = tk.BooleanVar()
tk.Checkbutton(options_frame, text="Extract ZIPs", variable=extract_var).pack(side=tk.LEFT, padx=5)

tk.Label(options_frame, text="Label:").pack(side=tk.LEFT, padx=5)
label_entry = tk.Entry(options_frame, width=15)
label_entry.pack(side=tk.LEFT, padx=5)
label_entry.insert(0, "ISO_CREATION")

output_frame = tk.Frame(root)
output_frame.pack(pady=5)

tk.Label(output_frame, text="ISO File:").pack(side=tk.LEFT, padx=5)
output_entry = tk.Entry(output_frame, width=30)
output_entry.pack(side=tk.LEFT, padx=5)
output_entry.insert(0, "output.iso")

run_button = tk.Button(root, text="Create ISO", command=run_command)
run_button.pack(pady=10)

output_text = tk.Text(root, height=10, width=70, state="disabled")
output_text.pack(pady=5)
output_text.tag_config("error", foreground="red")

tk.mainloop()
