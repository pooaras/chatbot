
import tkinter as tk
import subprocess
from tkinter import messagebox
from tkinter import ttk
def run_cmd():
    command = search_entry.get("1.0", tk.END).strip()
    if not command:
        messagebox.showwarning("Warning", "Please enter your query")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output_text.delete(1.0, tk.END)  # Clear previous output
        output_text.insert(tk.END, result.stdout)
        output_text.insert(tk.END, result.stderr)
    except Exception as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Error: {str(e)}")
def on_select(event):
    value = search_entry.get("1.0", tk.END).strip()
    # Filter suggestions based on the typed text
    suggestions = [item for item in all_suggestions if value.lower() in item.lower()]
    # Update the autocomplete list
    autocomplete_listbox.delete(0, tk.END)
    for suggestion in suggestions:
        autocomplete_listbox.insert(tk.END, suggestion)
    if suggestions:
        autocomplete_listbox.place(x=550,y=50)
    else:
        autocomplete_listbox.place_forget()

def on_click(event):
    # Get the selected suggestion from the autocomplete list
    selected_item = autocomplete_listbox.get(autocomplete_listbox.curselection())
    # Set the selected suggestion in the search bar
    search_entry.delete("1.0", tk.END)
    search_entry.insert("1.0",selected_item)
    # Clear the autocomplete list
    autocomplete_listbox.delete(0, tk.END)
    autocomplete_listbox.place_forget()
# Create the main window
window = tk.Tk()
window.title("Cmd Interface")
window.geometry("700x600")
# Create and place widgets in the window
label = tk.Label(window, text="Enter cmd command:")
label.pack(pady=10)

all_suggestions = [
    'dir', 'cd', 'cls', 'copy', 'del', 'erase', 'ren', 'rename', 'move',
    'mkdir', 'rmdir', 'rd', 'attrib', 'type', 'echo',
    'systeminfo', 'ipconfig', 'ping', 'tracert', 'pathping',
    'net user', 'net localgroup', 'net group', 'net share',
    'tasklist', 'taskkill', 'shutdown',
    'chkdsk', 'format', 'defrag',
    'netstat', 'nslookup', 'arp',
    'mstsc', 'qwinsta', 'logoff',
    'assoc', 'call', 'color', 'date', 'time'
]

# Create and place widgets in the window
search_var = tk.StringVar()

entry_height=40
search_entry_font = ("Arial", 12)
search_entry = tk.Text(window,font=search_entry_font, width=entry_height,height=10)
search_entry.pack(pady=10)
search_entry.bind('<KeyRelease>', on_select)  # Bind the on_select function to the KeyRelease event

autocomplete_listbox = tk.Listbox(window, height=12,width=15)
autocomplete_listbox.place_forget() 
autocomplete_listbox.bind('<ButtonRelease-1>', on_click) 

run_button = tk.Button(window, text="Run Command", command=run_cmd)
run_button.pack(pady=10)
run_button.place(x=70,y=50)
output_text = tk.Text(window, height=20, width=70)
output_text.pack(pady=10)

window.mainloop()

