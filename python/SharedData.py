# SharedData.py
import threading

# Shared variables encapsulated in a dictionary
shared_data = {
    'parking_spot_amount': 2,
    'free': 0,
    'next_parking_spot': 'Hellow'
}

dataBaseChanges = []

# Lock for thread-safe access to shared data
data_lock = threading.Lock()
