import tkinter as tk

def run_stats_gui():
    root = tk.Tk()
    root.title("Parkplatz Management System - Statistiken")

    root.configure(bg="gray")

    stats_label = tk.Label(root, text="Statistiken", font=("Helvetica", 20, "bold"), fg="white", bg="gray")
    stats_label.pack(pady=20, padx=20, fill=tk.X)

    stats_content = tk.Label(root, text="Hier könnten Statistiken und Diagramme dargestellt werden.", font=("Helvetica", 14), fg="white", bg="gray")
    stats_content.pack(pady=10, padx=20, fill=tk.X)

    root.geometry("800x600")
    root.minsize(400, 300)

    root.mainloop()

if __name__ == "__main__":
    run_stats_gui()
