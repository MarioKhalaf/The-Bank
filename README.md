# Bank server and Client
# Creator: Mario Khalaf
# Setup
The way to setup the program is simple:
* Folder must contain all four files:


        Bankserver.py
        Bankclient.py
        Server_registry.json
        Client_registry.json


* Run bankserver.py and start connecting multiple clients with bankclient.py


# Banksystem
* Register new accounts and client_registry.json will be used to store all new registered accounts.
* Once you're done, you can transfer the client_registry.json over to the server through the sockets and the accounts will be stored in the server file and the client file will be emptied.
* You can choose to ask the server for all accounts registered in the server. Make sure to transfer the client_registry.json if you wish to see the new accounts. This file wont be printed out.
* You can choose to search for specific Accounts by name.
* You can lock from further changes and even unlock them.
* You can withdraw and deposit money into the each account.
* The program has a lot of error handling such as locking and unlocking same customer over and over.
* You cannot withdraw more money than you what is in the account.
* Locked accounts cannot be accessed and therefore search, withdraw or deposit will not work on them.

* Pytest and tox have been used to test each function with 18 passed test and 100% coverage on server and 95% on client. No socket related function have been tested.



