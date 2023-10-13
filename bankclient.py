import socket
import json
import random
from tabulate import tabulate
from time import sleep


class Client():
    def __init__(self, sock):
        self.sock = sock
        self.person = {}
        self.FILENAME = "client_registry.json"

    def send_function(self, data):  # pragma no cover
        self.sock.sendall(data.encode())

    def receieve(self):  # pragma no cover
        return self.sock.recv(1024).decode()

    def customer_input(self):
        try:  # stores 4 values in self.person dict
            self.person["Bank ID"] = random.randint(1, 200)
            self.person["Name"] = input("Enter Name: ").capitalize()
            self.person["Balance"] = int(input("Deposit money: "))
            self.person["Address"] = input("Enter address: ").capitalize()
            return "\nAccount has been created "
        except ValueError:  # valuerror for balance, unfinished account will be handled after
            return "Only numbers allowed! Register again please."

    def get_accounts(self, data):
        try:
            if "locked" in data:  # check if name is locked
                return data
            else:
                data_as_list = json.loads(data)
                header = data_as_list[0].keys()  # using tabulate for a nicer output
                rows = [x.values() for x in data_as_list]  # list comprehension to loop through list
                tabulate_list = tabulate(rows, header, tablefmt='fancy_grid')
                return tabulate_list  # return fancy grid
        except IndexError:  # If list is returned empty, handle with index error
            return "\nBank accounts registry is empty or account does not exist"

    def write_to_client_json(self):
        with open(self.FILENAME) as f:
            data = json.load(f)
        if len(self.person) != 4:  # Checks if self.person contains a completed account, otherwise deletes it
            return "Unfinished registration detected. Deleting..."
        else:
            data["Accounts"].append(self.person)  # Appends to end of accounts list inside file
            with open(self.FILENAME, "w", encoding="utf-8") as f:  # write back updated file
                f.write(json.dumps(data, indent=4))
            return "Account added to registry"

    def transfer_file(self):
        print("Transfering file..."), sleep(2)
        with open(self.FILENAME) as f:
            file = json.load(f)
        if len(file["Accounts"]) == 0: # if "accounts" list is empty, abort transfer
            return "Transfer aborted"
        else:
            print("Transfer COMPLETED")
            client_file_str = json.dumps(file)  # dumps json file as a str
            return client_file_str  # and return json file as str

    def empty_sent_file(self):
        with open(self.FILENAME) as f:
            file = json.load(f)

        while len(file["Accounts"]) != 0:  # empty all acconunts list after dumping it with json
            file["Accounts"].pop()

        with open(self.FILENAME, "w") as f:  # Write back empty list into file
            f.write(json.dumps(file, indent=4))

        return "Client registry is now emptied."

    def wait_for_user(self):  # pragma no cover
        input("\nPress any key to continue...")


def withdraw_deposit(client):  # pragma no cover
    choice = input("1. Withdraw\n2. Deposit\n")  # function to make while true loop branch shorter
    client.send_function(choice)
    name = input("Name of account: ").capitalize()
    client.send_function(name)
    amount = input("Enter amount: ")
    client.send_function(amount)
    response = client.receieve()
    print("\n", response)
    client.wait_for_user()


def main_menu(client):  # pragma no cover
    while True:  # A while loop to handle all possible options
        print('''\n
1. Register new customer
2. Account registry
3. Search bar
4. Transfer file
5. Lock account
6. Unlock account
7. Make a withdrawal or deposit
8. Exit Bank Server\n
''')
        option = input("Enter choice or send a message: ")
        if not option:
            print("\nEmpty message is Not an option")
        elif option == "1":
            print(client.customer_input())
            print(client.write_to_client_json())
            client.wait_for_user()
        elif option == "2":
            client.send_function("all")
            data = client.receieve()
            print(client.get_accounts(data))
            client.wait_for_user()
        elif option == "3":
            client.send_function("search")
            search = input("Name of the customer you would like to search for: ").capitalize()
            client.send_function(search)
            data = client.receieve()
            print(client.get_accounts(data))
            client.wait_for_user()
        elif option == "4":
            client.send_function("transfer")
            client_file_str = client.transfer_file()
            client.send_function(client_file_str)
            print(client.empty_sent_file())
            client.wait_for_user()
        elif option == "5":
            client.send_function("lock")
            name = input("Name of the Account you would like to lock: ").capitalize()
            client.send_function(name)
            print("\n", client.receieve())
            client.wait_for_user()
        elif option == "6":
            client.send_function("unlock")
            name = input("Name of the Account you would like to unlock: ").capitalize()
            client.send_function(name)
            print("\n", client.receieve())
            client.wait_for_user()
        elif option == "7":
            withdraw_deposit(client)
        elif option == "8":
            client.send_function("disconnect")
            break
        else:
            client.send_function(option)
            print("\n", client.receieve())


def main():  # pragma no cover

    HOST = socket.gethostname()
    PORT = 50006
    sock = socket.socket()
    print(f'\nConnection established to Bank server...')
    sock.connect((HOST, PORT))
    client = Client(sock)  # instantiate class with sock as argument
    main_menu(client)
    sock.close()
    print("Exiting Bank server...\nGoodbye!")


if __name__ == "__main__":  # pragma no cover
    main()  # pragma no cover
