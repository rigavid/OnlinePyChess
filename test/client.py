from multiprocessing.connection import Client

def main():
    address = "192.168.1.125"
    client = Client((address, 1234))
    while True:
        try:
            print(client.recv())
            client.send(input())
        except: break

    client.close()

if __name__ == "__main__":
    main()