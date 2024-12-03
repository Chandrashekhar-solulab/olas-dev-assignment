# Autonomous Agents Implementation

This repository contains an implementation of autonomous agents in Python, designed to process and generate messages asynchronously, as per the assignment requirements.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)

## Overview

The project consists of two agents that communicate via message queues. The agents are capable of generating messages, processing incoming messages, checking token balances on Ethereum, and transferring tokens based on specified conditions.

### Agent Features

- **Agent 1**: Processes messages every 10 seconds, checks token balance, and transfers tokens if the message contains "crypto."
- **Agent 2**: Generates random two-word messages every 2 seconds and places them into Agent 1's inbox. It generates messages from a predefined list of words.

## Project Structure

```
├── Agent.py                   # Contains the implementation of Agent 1 and Agent 2
├── blockchain.py              # Interacts with the Ethereum blockchain
├── main.py                    # Main execution file to run the agents
├── tests.py                   # Unit tests for agent functionality
├── .env.example               # Example environment file for configuration
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. Set up a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on the `.env.example`:

   ```bash
   cp .env.example .env
   ```

   Then, open the `.env` file and fill in the values accordingly:

   ```plaintext
   ETH_NODE_URL=https://rpc.tenderly.co/YOUR_TENDERLY_PROJECT_URL   # Tenderly node URL
   FROM_ADDRESS=0xYourFromAddress                               # Address initiating the transactions and  Address holding token funds (e.g., USDC)
   TARGET_ADDRESS=0xYourTargetAddress                           # Address to send  funds
   TOKEN_CONTRACT_ADDRESS=0xYourTokenContractAddress            # USDC or other ERC20 token contract address
   PRIVATE_KEY=YourPrivateKeyHere                                   # Private key of FROM_ADDRESS (keep secure)
   ```

5. Fill in the `.env` file with your Ethereum node URL, source address, and token contract address.

## Usage

Fund the virtual tenderly ETH to perform the transaction

```bash
curl "https://virtual.mainnet.rpc.tenderly.co/1ddbd660-a5ba-4589-b77f-982707da7391" \
-X POST \
-H "Content-Type: application/json" \
-d '{
    "jsonrpc": "2.0",
    "method": "tenderly_setBalance",
    "params": [["FROM_ADDRESS"], "0x3635C9ADC5DEA00000"]
}'
```

Fund the `USD` token from real `HOLDER` in tenderly dashboard to `FROM_ADDRESS` 

To run the agents, execute the following command:

```bash
python3 main.py
```

The agents will start processing and generating messages based on their defined behaviors.

## Testing

To run the unit tests, use the following command:

```bash
python3 -m unittest test.py
```

The tests will validate the functionality of the agents and their interactions.
