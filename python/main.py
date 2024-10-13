import threading
import subprocess

def start_main_gui():
    subprocess.run(["python3", "main_gui.py"])

def start_stats_gui():
    subprocess.run(["python3", "stats_gui.py"])

def start_settings_gui():
    subprocess.run(["python3", "settings_gui.py"])

if __name__ == "__main__":
    threading.Thread(target=start_main_gui).start()
    threading.Thread(target=start_stats_gui).start()
    threading.Thread(target=start_settings_gui).start()
