from SerialServer import main_server
from sys import argv

class main():
    def __init__(self):
        self.start_main_server()

    def start_main_server(self):
        if len(argv) == 2:
            main_server.run(port=int(argv[1]))
        else:
            main_server.run()

if __name__ == '__main__':
    main()