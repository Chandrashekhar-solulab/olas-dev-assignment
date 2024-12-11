import os
import unittest
from unittest.mock import patch
import threading
import time

from agent.agent import agent_1, agent_2, inbox, outbox
from blockchain.blockchain import get_token_balance, transfer_token
SOURCE_ADDRESS = os.getenv("FROM_ADDRESS")


TO_ADDRESS = '0xFa7e2322AE858d58CDb7C4D8e2687c447d08c231'

class TestAgents(unittest.TestCase):

    @patch('agent.agent.get_token_balance')
    @patch('agent.agent.transfer_token')
    def test_agent_1_process_message(self, mock_transfer_token, mock_get_token_balance):
        stop_event = threading.Event()
        
        # Populate inbox with a message
        inbox.put("hello world")
        inbox.put("crypto message")
        
        # Run agent_1 for a short duration and then stop
        thread = threading.Thread(target=agent_1, args=(stop_event,))
        thread.start()
        time.sleep(1)  # Give some time to process messages

        # Verify correct processing of messages
        self.assertFalse(inbox.empty())
        self.assertEqual(outbox.get(), "hello world")
        mock_get_token_balance.assert_called_once_with(SOURCE_ADDRESS)
        
        self.assertEqual(outbox.get(), "crypto message")
        mock_transfer_token.assert_called_once()
        
        # Stop the agent
        stop_event.set()
        thread.join()
    def test_agent_2_generate_messages(self):
        stop_event = threading.Event()
        
        # Run agent_2 for a short duration and then stop
        thread = threading.Thread(target=agent_2, args=(stop_event,))
        thread.start()
        time.sleep(3)  # Adjusted sleep time to ensure processing
    
        # Logging to confirm if messages exist
        print("Queue size after agent_2 runs:", inbox.qsize())

        # Check if messages were generated
        self.assertFalse(inbox.empty())
        
        # Stop the agent
        stop_event.set()
        thread.join()

    @patch('blockchain.blockchain.token_contract')
    def test_get_token_balance(self, mock_token_contract):
      
        mock_token_contract.functions.balanceOf.return_value.call.return_value = 10000000
        balance = get_token_balance(SOURCE_ADDRESS)
        mock_token_contract.functions.balanceOf.assert_called_once_with(SOURCE_ADDRESS)
        
     
        self.assertEqual(balance, 10) 
    
    @patch('blockchain.blockchain.web3')  
    @patch('blockchain.blockchain.token_contract') 
    def test_transfer_token(self, mock_token_contract, mock_web3):
        # Mock the decimals method on the token contract
        mock_token_contract.functions.decimals.return_value.call.return_value = 6  # Example decimal value

        # Retrieve the decimal dynamically
        DECIMAL = mock_token_contract.functions.decimals().call()
        amount = 1 * (10 ** DECIMAL)  # Correct calculation for token amount

        # Mock transaction count and gas price
        mock_web3.eth.get_transaction_count.return_value = 1  
        mock_web3.to_wei.return_value = 2000000000  

        # Mock signing the transaction
        mock_signed_txn = unittest.mock.Mock()
        mock_signed_txn.raw_transaction = b'signed_txn_data'
        mock_web3.eth.account.sign_transaction.return_value = mock_signed_txn

        # Mock sending the raw transaction
        mock_web3.eth.send_raw_transaction.return_value = b'mock_tx_hash'

        # Mock token contract transfer function
        mock_transfer_func = unittest.mock.Mock()
        mock_transfer_func.build_transaction.return_value = {
            "from": SOURCE_ADDRESS,
            "nonce": 1,
            "gas": 200000,
            "gasPrice": 2000000000,
        }
        mock_token_contract.functions.transfer.return_value = mock_transfer_func

        # Call the function under test
        transfer_token(TO_ADDRESS, amount)

        # Assertions for contract call
        mock_token_contract.functions.transfer.assert_called_once_with(TO_ADDRESS, amount)
        mock_transfer_func.build_transaction.assert_called_once_with({
            "from": SOURCE_ADDRESS,
            "nonce": 1,
            "gas": 200000,
            "gasPrice": 2000000000,
        })

        # Assertions for signing and sending the transaction
        mock_web3.eth.account.sign_transaction.assert_called_once()
        mock_web3.eth.send_raw_transaction.assert_called_once_with(b'signed_txn_data')
        
    def test_integration_agents_message_flow(self):
        stop_event = threading.Event()
        
        # Start both agents
        thread_1 = threading.Thread(target=agent_1, args=(stop_event,))
        thread_2 = threading.Thread(target=agent_2, args=(stop_event,))
        
        thread_1.start()
        thread_2.start()
        
        time.sleep(5)  # Allow time for message generation and processing
        
        # Check that messages have moved from inbox to outbox
        self.assertFalse(inbox.empty())
        
        # Stop the agents
        stop_event.set()
        thread_1.join(timeout=3)
        thread_2.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
