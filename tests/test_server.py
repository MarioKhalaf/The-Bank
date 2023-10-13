
from bankserver import Server
import json

server = Server(conn="", address=("ip address", "51245"))
with open("server_registry.json") as f:
    file = json.load(f)


def test_read_json_file():
    assert server.read_json_file() == file


def test_send_registry():
    assert server.send_registry(file) == json.dumps(file["Accounts"])


def test_search_registry():
    account_filter = '[{"Bank ID": 55, "Name": "Mario", "Balance": 2645, "Address": "Stockholm"}]'
    assert server.search_registry(file, "Mario") == account_filter


def test_check_locked_acc():
    assert server.check_locked_acc(file, "Robert") is True
    assert server.check_locked_acc(file, "Tony") is False


def test_withdraw():
    assert server.withdraw(file, name="Noel", amount=2000) == "Not enough balance!"
    assert server.withdraw(file, name="Gabbe", amount=500) == "You have withdrawn 500 sek."


def test_deposit():
    assert server.deposit(file, name="Lucas", amount=500) == "You have deposited 500 sek."


def test_lock_accounts():
    assert server.lock_accounts(file, "Nicklas") == file


def test_unlock_accounts():
    assert server.unlock_accounts(file, "Peter") == file


def test_check_accounts():
    assert server.check_accounts(file, "Robert")  is False
    assert server.check_accounts(file, "Mario") is True


def test_handle_file_transfer():
    client_file_dict = {"Accounts": [{"Bank ID": 76, "Name": "Ove"}, {"Bank ID": 149, "Name": "Hello", "Balance": 54334, "Address": "Stockholm"}]}
    assert server.handle_file_transfer(file, client_file_dict) == file