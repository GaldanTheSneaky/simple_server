from server import Server


def main():
    server = Server(64, 5050)
    server.run()



if __name__ == '__main__':
    main()