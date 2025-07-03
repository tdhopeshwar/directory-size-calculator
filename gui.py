import tkinter as tk
from tkinter import messagebox, Listbox, END
from main import Directory, File, root  # Import your existing file system

current_dir = root

# ---------------- GUI Setup ----------------

window = tk.Tk()
window.title("📁 Directory Size Calculator")
window.geometry("500x400")

label = tk.Label(window, text="📂 Current Directory: root", font=("Times New Roman", 20))
label.pack(pady=10)

listbox = Listbox(window, width=80, height=25)
listbox.pack()

# ---------- Functions ------------

def update_display():
    listbox.delete(0, END)
    label.config(text=f"📂 Current Directory: {current_dir.name}")
    
    for subdir in current_dir.subdirectories.values():
        listbox.insert(END, f"[DIR] {subdir.name}/")
    
    for file in current_dir.files:
        listbox.insert(END, f"{file.name} ({file.size} KB)")

def show_size():
    total = current_dir.get_size()
    messagebox.showinfo("Directory Size", f"Total size of '{current_dir.name}' is {total} KB")

def go_back():
    global current_dir
    if current_dir.parent:
        current_dir = current_dir.parent
        update_display()

def on_item_double_click(event):
    global current_dir
    selection = listbox.get(listbox.curselection())
    
    if selection.startswith("[DIR]"):
        folder_name = selection.replace("[DIR] ", "").replace("/", "")
        current_dir = current_dir.subdirectories[folder_name]
        update_display()

# ---------- Buttons ------------

button_frame = tk.Frame(window)
button_frame.pack(pady=10)

size_btn = tk.Button(button_frame, text="📏 Show Size", command=show_size)
size_btn.grid(row=0, column=0, padx=5)

back_btn = tk.Button(button_frame, text="🔙 Go Back", command=go_back)
back_btn.grid(row=0, column=1, padx=5)

# Double-click folder to open
listbox.bind("<Double-Button-1>", on_item_double_click)

# Initial load
update_display()
window.mainloop()
