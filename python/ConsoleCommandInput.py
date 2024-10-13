from time import sleep

from SharedData import data_lock, shared_data


class ConsoleCommandInput():
    def __init__(self, manager):
        self.manager = manager
        return

    def run(self):
        while True:
            command = input("cmd: ")
            with data_lock:
                shared_data['parking_spot_amount'] = 10
                shared_data['free'] -= 1
            sleep(1)
            # print(shared_data['free'])
            match command:
                case "exit":
                    print("Exiting program...")
                    break  # Exit the loop to end the programm
                case _:
                    self.manager.parkplatz_arduino.sendCommand(command)

        print("Programm has ended.")
