import tkinter as tk

def run_settings_gui():
    root = tk.Tk()
    root.title("Parkplatz Management System - Einstellungen")

    root.configure(bg="gray")

    settings_label = tk.Label(root, text="Einstellungen", font=("Helvetica", 20, "bold"), fg="white", bg="gray")
    settings_label.pack(pady=20, padx=20, fill=tk.X)

    settings_content = tk.Label(root, text="Hier könnten verschiedene Einstellungen vorgenommen werden.", font=("Helvetica", 14), fg="white", bg="gray")
    settings_content.pack(pady=10, padx=20, fill=tk.X)

    root.geometry("800x600")
    root.minsize(400, 300)

    root.mainloop()

if __name__ == "__main__":
    run_settings_gui()
