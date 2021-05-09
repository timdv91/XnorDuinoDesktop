import serial, time, string, random

def main():
    ser = serial.Serial('COM19', 19200, timeout=2)

    time.sleep(5)

    counter = 0
    while(True):
        # printing lowercase
        letters = string.ascii_lowercase
        sendData = (''.join(random.choice(letters) for i in range(10))).encode('ascii')

        ser.write(sendData)
        retData = ser.read(len(sendData))

        if(sendData != retData):
            print("ERROR: Successcount: ", counter)
            quit(1)

        counter += 1

        if(counter%1000 == 0):
            print(retData, "| count: ", counter)


main()