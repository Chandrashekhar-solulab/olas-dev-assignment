import time
import os
from web3 import Web3
from dotenv import load_dotenv
from blockchain.tokenAbi import token_abi

# Load environment variables
load_dotenv()

# Configuration
ETH_NODE_URL = os.getenv("ETH_NODE_URL")  # Tenderly node URL
TOKEN_CONTRACT_ADDRESS = os.getenv("TOKEN_CONTRACT_ADDRESS")
FROM_ADDRESS = os.getenv("FROM_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
GAS = int(os.getenv("GAS", 200000))
GAS_PRICE = os.getenv("GAS_PRICE", "5")
DECIMAL = int(os.getenv("DECIMAL", 6))

# Initialize Web3 and contract instance
web3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))
token_contract = web3.eth.contract(address=TOKEN_CONTRACT_ADDRESS, abi=token_abi)

# Helper function to log messages with timestamp
def log_message(message):
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))
    print(f"[{current_time}] {message}")

# Get token balance of a specific address
def get_token_balance(address):
    try:
        raw_balance = token_contract.functions.balanceOf(address).call()
        adjusted_balance = raw_balance / 10**DECIMAL
        log_message(f"Token balance of {address}: {adjusted_balance}")
        return adjusted_balance
    except Exception as e:
        log_message(f"Error getting balance for {address}: {e}")
        return None

# Transfer tokens to a specific address
def transfer_token(target_address):
    try:
        tokens_to_transfer = 1 * 10**DECIMAL
        rawTransaction = token_contract.functions.transfer(target_address, tokens_to_transfer).build_transaction({
            "from": FROM_ADDRESS,
            "nonce": web3.eth.get_transaction_count(FROM_ADDRESS),
            "gas": GAS,
            "gasPrice": web3.to_wei(GAS_PRICE, "gwei"),
        })

        signed_txn = web3.eth.account.sign_transaction(rawTransaction, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        log_message(f"Simulating transfer of {tokens_to_transfer / 10**DECIMAL} token(s) from {FROM_ADDRESS} to {target_address}")
        log_message(f"Transaction Hash: {web3.to_hex(tx_hash)}")
    except Exception as e:
        log_message(f"Error transferring tokens from {FROM_ADDRESS} to {target_address}: {e}")
