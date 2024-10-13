import tkinter as tk
from tkinter import ttk
import threading
from Manager import Manager
from SharedData import shared_data, data_lock


def run_main_gui(dummy_data=False):
    global root, welcome_entry, next_parking_label, free_label, welcome_label_display, input_frame, button_frame, current_font_size
    current_font_size = 14  # Standard-Schriftgröße

    root = tk.Tk()
    root.title("Parkplatz Management System - Hauptseite")
    root.configure(bg="black")

    input_frame = tk.Frame(root, bg="black")
    input_frame.pack(pady=10, padx=20, fill=tk.X)

    welcome_label = tk.Label(input_frame, text="Willkommensnachricht eingeben:", font=("Helvetica", current_font_size),
                             fg="white", bg="black")
    welcome_label.pack(side=tk.LEFT)

    welcome_entry = tk.Entry(input_frame, width=50, font=("Helvetica", current_font_size), bg="black", fg="white")
    welcome_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

    button_frame = tk.Frame(root, bg="black")
    button_frame.pack(pady=10, fill=tk.X)

    style = ttk.Style()
    style.configure('TButton', font=("Helvetica", current_font_size), background="black", foreground="white")

    start_button = ttk.Button(button_frame, text="Start", command=lambda: show_parking_info(dummy_data),
                              style="TButton")
    start_button.pack(side=tk.LEFT, padx=10)

    quit_button = ttk.Button(button_frame, text="Beenden", command=root.quit, style="TButton")
    quit_button.pack(side=tk.LEFT, padx=10)

    # Initialisiere Labels ohne Text
    welcome_label_display = tk.Label(root, text="", font=("Helvetica", 24, "bold"), fg="white", bg="black")
    welcome_label_display.pack(pady=20, padx=20, fill=tk.X)

    free_label = tk.Label(root, text="", font=("Helvetica", 20, "bold"), fg="white", bg="black")
    free_label.pack(pady=10, padx=20, fill=tk.X)

    next_parking_label = tk.Label(root, text="", font=("Helvetica", 24, "bold"), fg="white", bg="black")
    next_parking_label.pack(pady=10, padx=20, fill=tk.X)

    root.geometry("800x600")
    root.minsize(400, 300)

    # Scrollen mit dem Mausrad
    root.bind("<MouseWheel>", zoom)

    root.mainloop()


def zoom(event):
    global current_font_size

    if event.delta > 0:
        current_font_size += 2
    else:
        current_font_size -= 2

    # Grenze der Schriftgröße festlegen
    current_font_size = max(8, current_font_size)

    for widget in root.winfo_children():
        update_font_size(widget, current_font_size)


def update_font_size(widget, size):
    if isinstance(widget, (tk.Label, tk.Button, ttk.Button)):
        widget.config(font=("Helvetica", size))

    for child in widget.winfo_children():
        update_font_size(child, size)


def show_parking_info(dummy_data):
    global welcome_label_display, free_label, next_parking_label

    welcome_message = welcome_entry.get()  # Get the welcome message before destroying the widgets
    input_frame.destroy()
    button_frame.destroy()

    welcome_label_display.config(text=welcome_message)

    if dummy_data:
        shared_data['next_parking_spot'] = 'D1'
        shared_data['free'] = 10
        shared_data['parking_spot_amount'] = 50

    free_label.config(text=f"Freie Parkplätze: {shared_data['free']}/{shared_data['parking_spot_amount']}")
    next_parking_label.config(text=f"Nächster freier Parkplatz: {shared_data['next_parking_spot']}")

    poll_for_updates(dummy_data)


def poll_for_updates(dummy_data):
    with data_lock:
        if not dummy_data:
            free_label.config(text=f"Freie Parkplätze: {shared_data['free']}/{shared_data['parking_spot_amount']}")
            next_parking_label.config(text=f"Nächster freier Parkplatz: {shared_data['next_parking_spot']}")

    root.after(500, lambda: poll_for_updates(dummy_data))


if __name__ == "__main__":
    def choose_mode():
        mode_window = tk.Tk()
        mode_window.title("Wählen Sie den Modus")
        mode_window.geometry("300x200")
        mode_window.configure(bg="black")

        label = tk.Label(mode_window, text="Wählen Sie den Modus aus:", font=("Helvetica", 14), fg="white", bg="black")
        label.pack(pady=20)

        normal_button = ttk.Button(mode_window, text="Normal",
                                   command=lambda: [mode_window.destroy(), start_manager_and_gui(False)],
                                   style="TButton")
        normal_button.pack(pady=10)

        dummy_button = ttk.Button(mode_window, text="Dummy-Daten",
                                  command=lambda: [mode_window.destroy(), start_manager_and_gui(True)], style="TButton")
        dummy_button.pack(pady=10)

        mode_window.mainloop()


    def start_manager_and_gui(dummy_data):
        if not dummy_data:
            manager = Manager()
            manager_thread = threading.Thread(target=manager.run)
            manager_thread.daemon = True
            manager_thread.start()
        run_main_gui(dummy_data)


    choose_mode()
