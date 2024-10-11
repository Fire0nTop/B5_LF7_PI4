import tkinter as tk
from tkinter import PhotoImage


# Funktion zum Öffnen eines neuen Fensters mit den Parkplatzdaten
def show_parking_info():
    welcome_message = welcome_entry.get()

    # Neues Fenster erstellen
    parking_info_window = tk.Toplevel(root)
    parking_info_window.title("Parkplatz Informationen")

    # Hintergrundbild
    bg_label = tk.Label(parking_info_window, image=background_image)
    bg_label.place(relwidth=1, relheight=1)

    # Eingabetext (Willkommensnachricht)
    welcome_label = tk.Label(parking_info_window, text=f"{welcome_message}", font=("Helvetica", 24, "bold"), fg="black",
                             bg="#add8e6")
    welcome_label.pack(pady=20)

    # Nächster Parkplatz
    next_parking_label = tk.Label(parking_info_window, text="Nächster freier Parkplatz: P1",
                                  font=("Helvetica", 24, "bold"), fg="black", bg="#add8e6")
    next_parking_label.pack(pady=20)

    # Parkplatzinformationen in einzelnen Abteilen
    occupied_label = tk.Label(parking_info_window, text="Besetzte Parkplätze: 25", font=("Helvetica", 20, "bold"),
                              fg="black", bg="#add8e6")
    occupied_label.pack(pady=10)

    free_label = tk.Label(parking_info_window, text="Freie Parkplätze: 15", font=("Helvetica", 20, "bold"), fg="black",
                          bg="#add8e6")
    free_label.pack(pady=10)

    # Dynamische Anpassung der Fenstergröße
    parking_info_window.geometry("800x600")


# Funktion zum Beenden des Programms
def quit_program():
    root.quit()


# Hauptfenster
root = tk.Tk()
root.title("Parkplatz Management System")

# Hintergrundbild laden
background_image = PhotoImage(file="gradient.png")

# Hintergrund im Hauptfenster
bg_label = tk.Label(root, image=background_image)
bg_label.place(relwidth=1, relheight=1)

# Willkommensnachricht Eingabe
welcome_label = tk.Label(root, text="Willkommensnachricht eingeben:", font=("Helvetica", 14), fg="black", bg="white")
welcome_label.pack(pady=10)

welcome_entry = tk.Entry(root)
welcome_entry.pack(pady=10)

# Start- und Beenden-Knöpfe
start_button = tk.Button(root, text="Start", command=show_parking_info)
start_button.pack(pady=10)

quit_button = tk.Button(root, text="Beenden", command=quit_program)
quit_button.pack(pady=10)

root.mainloop()
