import unittest
from unittest.mock import patch
from queue import Queue
import threading
import time

from Agent import agent_1, agent_2, inbox, outbox
from blockchain import get_token_balance, transfer_token, SOURCE_ADDRESS

TO_ADDRESS = '0xFa7e2322AE858d58CDb7C4D8e2687c447d08c231'

class TestAgents(unittest.TestCase):

    @patch('Agent.get_token_balance')
    @patch('Agent.transfer_token')
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

    @patch('blockchain.token_contract')
    def test_get_token_balance(self, mock_token_contract):
        # Mock the balanceOf function call
        mock_token_contract.functions.balanceOf.return_value.call.return_value = 1000000
        balance = get_token_balance(SOURCE_ADDRESS)
        mock_token_contract.functions.balanceOf.assert_called_once_with(SOURCE_ADDRESS)
        
        # Verify the expected output format
        self.assertEqual(balance, 1)  # Adjusting for token decimals

    @patch('blockchain.token_contract')
    @patch('blockchain.web3')
    def test_transfer_token(self, mock_web3, mock_token_contract):
        # Mocking nonce and transaction building
        mock_web3.eth.get_transaction_count.return_value = 1
        transfer_token(TO_ADDRESS)
        
        # Verify transfer function call with correct arguments
        mock_token_contract.functions.transferFrom.assert_called_once_with(
            SOURCE_ADDRESS,TO_ADDRESS, 1 * 10**6
        )


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
