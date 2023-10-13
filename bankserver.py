import socket
import threading
import json
from time import sleep


class Server(threading.Thread):
    def __init__(self, conn, address):
        super(Server, self).__init__()
        self.conn = conn
        self.address = address
        self.FILENAME = "server_registry.json"
        self.running = True

    def run(self):  # pragma no cover
        print(f"Thread {threading.active_count() - 1} activated by Bank '{self.address[1]}'")
        try:
            while self.running:
                data = self.receieve()
                file = self.read_json_file()

                if data == "disconnect":
                    self.stop()

                elif data == "all":
                    all_accounts = self.send_registry(file)
                    self.send_function(all_accounts)

                elif data == "transfer":
                    client_file = self.receieve()
                    print(f"Receiving file from bank {self.address[1]}..."), sleep(2)
                    if "aborted" in client_file:
                        print("An empty file received...")
                    else:
                        client_file_dict = json.loads(client_file)
                        updated_file = self.handle_file_transfer(file, client_file_dict)
                        self.write_json_file(updated_file)

                elif data == "search":
                    name = self.receieve()
                    if self.check_locked_acc(file, name) is True:  # Check if acc is locked, if True, return access denied
                        self.send_function("Access denied! This account is locked")
                    else:
                        acc_search = self.search_registry(file, name)
                        self.send_function(acc_search)

                elif data == "lock":
                    name = self.receieve()
                    if self.check_locked_acc(file, name) is True:  # prevents locking already locked account
                        self.send_function("This account is already locked and cannot be accessed.")
                    elif self.check_accounts(file, name) is False:
                        self.send_function("There is no account by that name in the register.")
                    else:
                        updated_file = self.lock_accounts(file, name)
                        self.write_json_file(updated_file)
                        self.send_function(f"Account {name} is now locked")

                elif data == "unlock":
                    name = self.receieve()
                    if self.check_accounts(file, name) is True:  # Prevents unlocking already unlocked accounts
                        self.send_function("This account is already unlocked and is available for change")
                    elif self.check_locked_acc(file, name) is False:
                        self.send_function("There is no account by that name in the register.")
                    else:
                        updated_file = self.unlock_accounts(file, name)
                        self.write_json_file(updated_file)
                        self.send_function(f"Account {name} is now unlocked")

                elif data == "1":
                    name = self.receieve()
                    amount = self.receieve()
                    if self.check_locked_acc(file, name) is True:
                        self.send_function("Access denied! This account is locked")
                    elif self.check_accounts(file, name) is False:
                        self.send_function("There is no account by that name in the register.")
                    else:
                        message = self.withdraw(file, name, int(amount))
                        self.send_function(message)

                elif data == "2":
                    name = self.receieve()
                    amount = self.receieve()
                    if self.check_locked_acc(file, name) is True:
                        self.send_function("Access denied! This account is locked")
                    elif self.check_accounts(file, name) is False:
                        self.send_function("There is no account by that name in the register.")
                    else:
                        message = self.deposit(file, name, int(amount))
                        self.send_function(message)
                else:
                    self.send_function(f"SERVER: Message receieved, but no action applied")
                    print(f"Message from Bank {self.address[1]}: '{data}'")

        except (ConnectionAbortedError, ConnectionResetError, OSError):  # Handles CTRL C exits from clients
            print(f"Bank {self.address[1]} has disconnected. shutting down thread...")

    def receieve(self):  # pragma no cover # function handles all receving messages
        return self.conn.recv(1024).decode()

    def send_function(self, data):  # pragma no cover
        self.conn.sendall(data.encode())  # function handles all sent data

    def send_registry(self, file):
        print(f"Account registry sent back to Bank {self.address[1]}")
        return json.dumps(file["Accounts"])

    def search_registry(self, file, name):
        acc_search = []
        for value in file["Accounts"]:
            if value["Name"] == name:
                acc_search.append(value)
        return json.dumps(acc_search)

    def handle_file_transfer(self, file, client_file_dict):
        for account in client_file_dict["Accounts"]:
            file["Accounts"].append(account)
            print("Downloading data..."), sleep(1)
        sleep(1), print("Download COMPLETED.")
        return file

    def lock_accounts(self, file, name):
        for i, value in enumerate(file["Accounts"]):  # Enumerate to get index and value at same time
            if value["Name"] == name:  # If name matches name inside value
                file["locked"].append(value)  # append locked list
                file["Accounts"].pop(i)  # pop from Accounts list
        return file

    def unlock_accounts(self, file, name):
        for i, value in enumerate(file["locked"]):
            if value["Name"] == name:
                file["Accounts"].append(value)
                file["locked"].pop(i)
        return file

    def check_locked_acc(self, file, name):
        for value in file["locked"]:
            if value["Name"] == name:  # if name of account is in there, return True
                return True
        return False

    def check_accounts(self, file, name):
        for value in file["Accounts"]:
            if value["Name"] == name:  # if name of account is in there, return True
                return True
        return False

    def withdraw(self, file, name, amount):
        for i, value in enumerate(file["Accounts"]):  # using enumerate to get the index and value at same time
            if value["Name"] == name:
                current_balance = file["Accounts"][i]["Balance"]  # converting for readability
                if amount > current_balance:
                    return "Not enough balance!"
                else:
                    file["Accounts"][i]["Balance"] = current_balance - amount
        self.write_json_file(file)
        print(f"Bank {self.address[1]} has made a withdrawal from account {name}")
        return f"You have withdrawn {amount} sek."

    def deposit(self, file, name, amount):
        for i, value in enumerate(file["Accounts"]):
            if value["Name"] == name:
                current_balance = file["Accounts"][i]["Balance"]
                file["Accounts"][i]["Balance"] = current_balance + int(amount)
        self.write_json_file(file)
        print(f"Bank {self.address[1]} has made a deposit to account {name}.")
        return f"You have deposited {amount} sek."

    def read_json_file(self):
        with open(self.FILENAME) as f:
            file = json.load(f)
        return file

    def write_json_file(self, file):
        with open(self.FILENAME, "w") as f:
            f.write(json.dumps(file, indent=4))

    def stop(self):  # pragma no cover
        self.conn.close()


def main():  # pragma no cover
    HOST = socket.gethostname()
    PORT = 50006
    with socket.socket() as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        print("Bank server is up and running...")
        while True:
            conn, address = sock.accept()
            print(f"Connection established from bank {address[1]}...")
            Server(conn, address).start()


if __name__ == "__main__":  # pragma no cover
    main()
