import tkinter as tk
import random
import threading
import time

def create_binary_window():
    root = tk.Tk()
    root.title("Terminal")
    root.geometry("800x600")
    root.configure(bg='black')

    text = tk.Text(root, bg='black', fg='green', font=('Courier', 12), wrap=tk.WORD)
    text.pack(expand=True, fill=tk.BOTH)

    def scroll_binary():
        while True:
            line = ''.join(random.choice('01') for _ in range(80))
            text.insert(tk.END, line + '\n')
            text.see(tk.END)
            time.sleep(0.1)

    threading.Thread(target=scroll_binary, daemon=True).start()
    root.mainloop()

def create_message_window(message):
    root = tk.Tk()
    root.title("Hacking Status")
    root.geometry("400x200")
    root.configure(bg='black')

    label = tk.Label(root, text=message, bg='black', fg='green', font=('Courier', 24))
    label.pack(expand=True)

    root.mainloop()

if __name__ == "__main__":
    # Create multiple binary windows
    for i in range(10):
        threading.Thread(target=create_binary_window, daemon=True).start()
        time.sleep(0.1)

    # Create message windows
    messages = ['Access Granted', 'Hacking in Progress', 'System Compromised', 'Data Retrieved', 'Firewall Breached']
    for msg in messages:
        threading.Thread(target=lambda m=msg: create_message_window(m), daemon=True).start()
        time.sleep(0.1)