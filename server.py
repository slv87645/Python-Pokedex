from socket import *
import random


def random_number_gen(max_num):
    randNum = random.randint(1, max_num)
    return randNum


def run_server():
    """Runs a server that generates a random number and sends it to the client."""
    clientPort = 9344
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('localhost', clientPort))
    serverSocket.listen(1)
    print("Waiting for connection...")
    while True:
        connection, addr = serverSocket.accept()
        print("Connection made.")
        randNum = random_number_gen(1010)
        connection.send(str(randNum).encode())
        print("Random number " + str(randNum) + " sent.")


if __name__ == "__main__":
    run_server()
