import tkinter as tk
from tkinter import messagebox
import subprocess
import os

class AutocompletePopup(tk.Toplevel):
    def __init__(self, master, suggestions, callback):
        super().__init__(master)
        self.overrideredirect(True)
        self.suggestions = suggestions
        self.callback = callback
        self.listbox = tk.Listbox(self, height=len(suggestions), selectbackground="lightgray", selectmode=tk.SINGLE, bg="#333", fg="white")
        self.listbox.pack(expand=True, fill=tk.BOTH)
        self.listbox.bind("<ButtonRelease-1>", self.on_click)

    def on_click(self, event):
        selected_item = self.listbox.get(self.listbox.curselection())
        self.callback(selected_item)
        self.destroy()

autocomplete_popup = None
search_var = None
search_entry = None
output_text = None

def run_cmd():
    global search_var, output_text
    command = search_var.get().strip()
    if not command:
        messagebox.showwarning("Warning", "Please enter your query")
        return

    try:
        current_dir = os.getcwd()
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=current_dir)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"{current_dir}> {command}\n")
        output_text.insert(tk.END, f"Exit Code: {result.returncode}\n")
        output_text.insert(tk.END, "\n")
        output_text.insert(tk.END, result.stdout)
        output_text.insert(tk.END, result.stderr)
    except Exception as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Error: {str(e)}")

    search_var.set('')

def on_select(event):
    global search_var, search_entry, all_suggestions
    value = search_var.get().strip()
    suggestions = [item for item in all_suggestions if value.lower() in item.lower()]
    show_autocomplete_suggestions(suggestions)

def show_autocomplete_suggestions(suggestions):
    global autocomplete_popup, search_var, search_entry
    if autocomplete_popup is None:
        autocomplete_popup = AutocompletePopup(window, [], on_autocomplete_select)

    if suggestions:
        x, y, _, _ = search_entry.bbox("insert")
        x += search_entry.winfo_rootx() + 2
        y += search_entry.winfo_rooty() + search_entry.winfo_height() + 2
        autocomplete_popup.geometry(f"{search_entry.winfo_width()}x200+{x}+{y}")
        autocomplete_popup.deiconify()
        autocomplete_popup.lift()
        autocomplete_popup.listbox.delete(0, tk.END)
        for suggestion in suggestions:
            autocomplete_popup.listbox.insert(tk.END, suggestion)
    else:
        hide_autocomplete_suggestions()

def hide_autocomplete_suggestions():
    global autocomplete_popup
    if autocomplete_popup:
        autocomplete_popup.withdraw()
        autocomplete_popup = None

def on_autocomplete_select(selected_item):
    global search_var
    search_var.set(selected_item)
    hide_autocomplete_suggestions()

window = tk.Tk()
window.title("Cmd Interface")
window.geometry("800x600")
window.configure(bg='#333')  # Set background color

label = tk.Label(window, text="Enter cmd command:", bg='#333', fg='white', font=("Arial", 14, 'bold'))
label.pack(pady=10)

all_suggestions = [
    'assoc', 'at', 'attrib', 'break', 'bcdedit', 'cacls', 'call', 'cd', 'chcp',
    'chdir', 'chkdsk', 'chkntfs', 'cls', 'cmd', 'color', 'comp', 'compact', 'convert',
    'copy', 'date', 'del', 'dir', 'diskpart', 'doskey', 'driverquery', 'echo', 'endlocal',
    'erase', 'exit', 'fc', 'find', 'findstr', 'for', 'format', 'fsutil', 'ftype', 'gpupdate',
    'goto', 'gpresult', 'graftabl', 'help', 'icacls', 'if', 'ipconfig', 'label', 'md', 'mkdir',
    'mklink', 'mode', 'more', 'move', 'net', 'netstat', 'notepad', 'nslookup', 'openfiles', 'path',
    'pause', 'popd', 'print', 'prompt', 'pushd', 'rd', 'recover', 'ren', 'rename', 'replace',
    'rmdir', 'robocopy', 'set', 'setlocal', 'setx', 'sfc', 'shutdown', 'sort', 'start', 'subst',
    'systeminfo', 'taskkill', 'tasklist', 'time', 'title', 'tree', 'type', 'ver', 'verify', 'vol',
    'where', 'wmic', 'xcopy'
]


search_var = tk.StringVar()

entry_frame = tk.Frame(window, bg='#333')  
entry_frame.pack(pady=10)

label = tk.Label(entry_frame, text="Enter cmd command:", bg='#333', fg='white', font=("Arial", 12))
label.pack(side=tk.LEFT, padx=10)

search_entry_font = ("Arial", 14)
search_entry = tk.Entry(entry_frame, font=search_entry_font, textvariable=search_var, bg='#444', fg='white')  
search_entry.pack(side=tk.LEFT, padx=10)

run_button = tk.Button(window, text="Run Command", command=run_cmd, bg='#4CAF50', fg='white', font=("Arial", 12, 'bold'))
run_button.pack(pady=10)

output_text = tk.Text(window, height=20, width=70, bg='#444', fg='white')  
output_text.pack(pady=10)

search_entry.bind('<KeyRelease>', on_select)

window.mainloop()
