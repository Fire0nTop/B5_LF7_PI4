
from Arduino import Arduino


arduino = Arduino(Arduino.selectArduinoPort())

while True:
    command = input("cmd: ")

    match command:
        case "exit":
            quit(0)
        case "special":
            status = arduino.getStatus(0)
            _, _, _, special = status
            print("special: " + str(arduino.setSpecial(0, not special)))
        case"reserved":
            status = arduino.getStatus(0)
            _, _, reserved, _ = status
            print("reserved: " + str(arduino.setReserved(0, not reserved)))
        case _:
            print(arduino.sendCommand(command))

