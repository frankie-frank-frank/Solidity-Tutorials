from solcx import compile_standard, install_solc
install_solc('0.8.13')
import json
from web3 import Web3

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*":["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.8.13",
)

with open("compiled_code.json","w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#connect to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0xa02F701Afa3d4875808e57CAAE073f3b59e4F8C6"
private_key = "f8f78dd9b5edb82a5677647c860a995d03bdae868d906fc23b139798b3e58e3f"

#create contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

#get latest transaction count
nonce = w3.eth.getTransactionCount(my_address)

#build a transaction
transaction = SimpleStorage.constructor().buildTransaction({"chainId": chain_id, "from": my_address, "nonce": nonce})
print(transaction)