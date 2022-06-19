from sys import argv
import SerialServer.main_server as main_server

class main():
    def __init__(self):
        self.start_main_server()

    def start_main_server(self):
        if len(argv) == 2:
            main_server.run(pHWport=argv[1])
        elif len(argv) == 3:
            main_server.run(pHWport=argv[1], pHWbautrate=int(argv[2]))
        elif len(argv) == 4:
            main_server.run(pHWport=argv[1], pHWbautrate=int(argv[2]), pSrvPort=int(argv[3]))
        else:
            #main_server.run(pHWport='COM25', pHWbautrate=38400, pSrvPort=8080)
            main_server.run(pHWport='/dev/ttyUSB0', pHWbautrate=38400, pSrvPort=8080)

if __name__ == '__main__':
    main()