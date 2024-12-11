import os
import random
import time
from queue import Queue
from threading import Event
from blockchain.blockchain import FROM_ADDRESS, get_token_balance, transfer_token
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TARGET_ADDRESS = os.getenv("TARGET_ADDRESS")
WORD_LIST = os.getenv("WORD_LIST", "hello,sun,world,space,moon,crypto,sky,ocean,universe,human").split(",")
BALANCE_CHECK_TIME = int(os.getenv("BALANCE_CHECK_TIME", 10))
MESSAGE_GENERATE_TIME = int(os.getenv("MESSAGE_GENERATE_TIME", 2))
MESSAGE_WORD = os.getenv("MESSAGE_WORD", "hello")
CRYPTO_WORD = os.getenv("CRYPTO_WORD", "crypto")

# Queues for communication between agents
inbox = Queue()
outbox = Queue()

# Agent 1: Processes messages in the inbox every 10 seconds
def agent_1(stop_event):
    while not stop_event.is_set():
        time.sleep(BALANCE_CHECK_TIME)
        # Check the token balance
        get_token_balance(FROM_ADDRESS)

        # Process inbox messages
        while not inbox.empty():
            message = inbox.get()

            if MESSAGE_WORD in message:
                print(f"Message with '{MESSAGE_WORD}' moved to outbox:", message)
            elif CRYPTO_WORD in message:
                print(f"Triggering token transfer for message containing '{CRYPTO_WORD}'")
                transfer_token(TARGET_ADDRESS,1*1**6)

            outbox.put(message)

            # Check the stop event after processing each message
            if stop_event.is_set():
                break

# Agent 2: Generates messages every 2 seconds and puts them in Agent 1's inbox
def agent_2(stop_event):
    while not stop_event.is_set():
        time.sleep(MESSAGE_GENERATE_TIME)
        
        # Generate a random message
        message = f"{random.choice(WORD_LIST)} {random.choice(WORD_LIST)}"
        inbox.put(message)
        print("Generated inbox message:", message)
