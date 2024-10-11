# Gui.py
import tkinter as tk
import threading
from SharedData import shared_data, data_lock  # Import shared data and lock
from Programm import programm  # Import the programm function

def run_gui():
    global root, welcome_entry, next_parking_label, occupied_label, free_label

    root = tk.Tk()
    root.title("Parkplatz Management System")

    # Hintergrundfarbe des Hauptfensters ändern
    root.configure(bg="gray")

    # Frame für die Willkommensnachricht Eingabe
    input_frame = tk.Frame(root, bg="gray")
    input_frame.pack(pady=10, padx=20, fill=tk.X)

    # Willkommensnachricht Eingabe
    welcome_label = tk.Label(input_frame, text="Willkommensnachricht eingeben:", font=("Helvetica", 14), fg="white", bg="gray")
    welcome_label.pack(side=tk.LEFT)

    welcome_entry = tk.Entry(input_frame, width=50)
    welcome_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

    # Start- und Beenden-Knöpfe
    button_frame = tk.Frame(root, bg="gray")
    button_frame.pack(pady=10, fill=tk.X)

    start_button = tk.Button(button_frame, text="Start", command=show_parking_info)
    start_button.pack(side=tk.LEFT, padx=10)

    quit_button = tk.Button(button_frame, text="Beenden", command=root.quit)
    quit_button.pack(side=tk.LEFT, padx=10)

    # Fenster anpassen
    root.geometry("800x600")
    root.minsize(400, 300)  # Mindestgröße des Fensters

    # Start the main loop of the GUI
    root.mainloop()

# Funktion zum Öffnen eines neuen Fensters mit den Parkplatzdaten
def show_parking_info():
    welcome_message = welcome_entry.get()

    # Neues Fenster erstellen
    parking_info_window = tk.Toplevel(root)
    parking_info_window.title("Parkplatz Informationen")

    # Hintergrundfarbe ändern
    parking_info_window.configure(bg="gray")

    # Eingabetext (Willkommensnachricht)
    welcome_label = tk.Label(parking_info_window, text=welcome_message, font=("Helvetica", 24, "bold"), fg="white", bg="gray")
    welcome_label.pack(pady=20, padx=20, fill=tk.X)

    # Create parking information labels (initially empty)
    global next_parking_label, occupied_label, free_label

    next_parking_label = tk.Label(parking_info_window, text="", font=("Helvetica", 24, "bold"), fg="white", bg="gray")
    next_parking_label.pack(pady=20, padx=20, fill=tk.X)

    occupied_label = tk.Label(parking_info_window, text="", font=("Helvetica", 20, "bold"), fg="white", bg="gray")
    occupied_label.pack(pady=10, padx=20, fill=tk.X)

    free_label = tk.Label(parking_info_window, text="", font=("Helvetica", 20, "bold"), fg="white", bg="gray")
    free_label.pack(pady=10, padx=20, fill=tk.X)

    # Start polling to update the labels based on shared data
    poll_for_updates(parking_info_window)

    # Dynamische Anpassung der Fenstergröße
    parking_info_window.geometry("800x600")
    parking_info_window.minsize(400, 300)  # Mindestgröße des Fensters

def poll_for_updates(parking_info_window):
    # This function will be called every 500ms to check for updates
    with data_lock:
        # Update the parking info from shared data
        next_parking_label.config(text=f"Nächster freier Parkplatz: {shared_data['next_parking_spot']}")
        occupied_label.config(text=f"Besetzte Parkplätze: {shared_data['occupied']}")
        free_label.config(text=f"Freie Parkplätze: {shared_data['free']}")

    # Continue polling every 500ms
    parking_info_window.after(500, poll_for_updates, parking_info_window)

def main():
    # Run the programm logic in a separate thread
    programm_thread = threading.Thread(target=programm)
    programm_thread.start()

    # Start the GUI in the main thread
    run_gui()

if __name__ == "__main__":
    main()
