import os
from dotenv import load_dotenv

load_dotenv()

hostname = os.getenv("HOSTNAME")
port = os.getenv("PORT")
username = os.getenv("BEUTZERNAME")
password = os.getenv("PASSWORT")

print(hostname + port + username + password)