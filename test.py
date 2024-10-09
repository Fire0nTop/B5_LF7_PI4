from contextlib import nullcontext
from time import sleep

import serial.tools.list_ports

def selectArduino():
    ports = serial.tools.list_ports.comports()
    choices = []
    print('PORT\tDEVICE\t\t\tMANUFACTURER')
    for index, value in enumerate(sorted(ports)):
        if value.hwid != 'n/a':
            choices.append(index)
            print(index, '\t', value.name, '\t', value.manufacturer)

    choice = -1
    while choice not in choices:
        answer = input("➜ Select your port: ")
        if answer.isnumeric() and int(answer) <= int(max(choices)):
            choice = int(answer)
    print('selecting: ', ports[choice].device)
    return ports[choice].device

serialInst = serial.Serial()
use = selectArduino()

serialInst.baudrate = 9600
serialInst.port = use
serialInst.open()

while True:
    command = input("cmd: ")

    match command:
        case "exit":
            quit(0)
        case "read":
            print("RES: " + serialInst.readline().decode('utf-8'))
        case _:
            print("default")
            serialInst.write(command.encode('utf-8'))
            sleep(0.05)
            print("RES: " + serialInst.readline().decode('utf-8'))

