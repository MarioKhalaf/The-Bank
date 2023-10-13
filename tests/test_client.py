from bankclient import Client
from unittest import mock
import json

client = Client(sock=" ")


def test_customer_input(monkeypatch):
    test = iter(["Thomas", 5000, "Odenplan"])
    monkeypatch.setattr("builtins.input", lambda _: next(test))
    assert client.customer_input() == "\nAccount has been created "


@mock.patch("builtins.input", return_value="Thomas, 5000, Odenplan")
def test_customer_input2(mocked_input, capfd):  # monkeypatch cant diff between integers and strings
    client.customer_input()  # could not raise valuerror without this as above
    out, err = capfd.readouterr()
    assert out == ""


def test_write_to_client():
    assert client.write_to_client_json() == "Account added to registry"


def test_get_accounts():
    data = "Access denied! This account is locked"
    assert client.get_accounts(data) == data


def test_get_accounts2():
    lista = [{"Bank ID": 127, "Name": "Noel", "Balance": 600, "Address": "Norsborg"}]
    list_str = json.dumps(lista)
    tabulated_list = '╒═══════════╤════════╤═══════════╤═══════════╕\n│   Bank ID │ Name   │   Balance │ Address   │\n╞═══════════╪════════╪═══════════╪═══════════╡\n│       127 │ Noel   │       600 │ Norsborg  │\n╘═══════════╧════════╧═══════════╧═══════════╛'
    assert client.get_accounts(list_str) == tabulated_list


def test_get_accounts3():
    empty_list = []
    empty_list = json.dumps(empty_list)
    assert client.get_accounts(empty_list) == "\nBank accounts registry is empty or account does not exist"

def test_transfer_file():
    client_file_str = client.transfer_file()
    assert client.transfer_file() == client_file_str

def test_empty_sent_file():
    assert client.empty_sent_file() == "Client registry is now emptied."