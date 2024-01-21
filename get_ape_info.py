from web3 import Web3
from web3.providers.rpc import HTTPProvider
import requests
import json

# You will need the ABI to connect to the contract
# The file 'abi.json' has the ABI for the bored ape contract
# In general, you can get contract ABIs from etherscan
# https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
#with open('/home/codio/workspace/abi.json', 'r') as f:
    #abi = json.load(f)

contract_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
abi_endpoint = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}"

try:
    response = requests.get(abi_endpoint, timeout=20)
    abi_response = response.json()

    if abi_response['status'] == '1':
        abi = json.loads(abi_response['result'])
        with open('/home/codio/workspace/abi.json', 'w') as f:
            json.dump(abi, f)
        print("ABI successfully obtained and saved.")
    else:
        print(f"Failed to get ABI: {abi_response['message']}")

except Exception as e:
    print(f"Failed to get ABI from Etherscan: {e}")

with open('/home/codio/workspace/abi.json', 'r') as f:
    abi_l = json.load(f)


# Connect to an Ethereum node
api_url = "https://eth-mainnet.alchemyapi.io/v2/7R8FD0Z9VuycQYgASfO5xsfAPsK21DJW"
provider = HTTPProvider(api_url)
web3 = Web3(provider)

def get_ape_info(apeID):
    assert isinstance(apeID, int), f"{apeID} is not an int"
    assert 1 <= apeID, f"{apeID} must be at least 1"

    contract = web3.eth.contract(address=contract_address, abi=abi_l)

    # Get the owner of the ape
    owner = contract.functions.ownerOf(apeID).call()

    # Get the token URI from IPFS
    token_uri = f'https://gateway.pinata.cloud/ipfs/QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/{apeID}'
    response = requests.get(token_uri)
    token_data = response.json()

    # Extract image and eyes data from token data
    image = token_data.get('image', '')
    eyes = token_data.get('eyes', '')

    data = {'owner': owner, 'image': image, 'eyes': eyes}

    print(data)

    assert isinstance(data, dict), f'get_ape_info{apeID} should return a dict'
    assert all([a in data.keys() for a in ['owner', 'image', 'eyes']]), \
        f"return value should include the keys 'owner', 'image' and 'eyes'"
    return data

# Main function to test get_ape_info()
def main():
    # Test cases
    ape_ids = [1, 5000, 10000]

    for ape_id in ape_ids:
        ape_info = get_ape_info(ape_id)
        print(f"Ape ID: {ape_id}, Info: {ape_info}")

if __name__ == "__main__":
    main()
