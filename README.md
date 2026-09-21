# Robinhood Chain Agentic Trader

**Lead Architect & Owner:** Eng. Awsan Adel Abdulbari Ahmed Sultan  
**Location:** Sana'a, Yemen  
**Contact:** awsan.sultan@gmail.com | +967 777852433  
**LinkedIn:** [Eng. Awsan Sultan](https://www.linkedin.com/in/awsan-adel-abdulbari-ahmed-sultan-8aa5a1a9)

---

## Overview
**robinhood-chain-agentic-trader** is an institutional-grade platform integrating decentralized on-chain assets with automated brokerage trading. It bridges:
- **Web3 & DeFi:** Smart contracts deployed on **Robinhood Chain (L2)** and Ethereum-compatible networks.
- **TradFi & Brokerage:** Automated equity, ETF, and crypto execution powered by the **Robinhood Trading MCP** (`https://agent.robinhood.com/mcp/trading`).
- **Autonomous Governance:** Built-in programmatic risk management guardrails ensuring capital safety in isolated agent accounts.

---

## Repository Architecture

```text
robinhood-chain-agentic-trader/
├── .cursor/
│   └── mcp.json                  # IDE-level MCP connection to Robinhood Agentic server
├── contracts/
│   ├── PlatformToken.sol         # ERC-20 utility & governance token ($AWSN)
│   ├── PlatformNFT.sol           # ERC-721 tiered membership NFT with ERC-2981 royalties ($AWNX)
│   └── Treasury.sol              # Autonomous protocol treasury manager
├── agent/
│   ├── mcp_trading_agent.py      # Python agent controller with risk guardrails
│   └── requirements.txt          # Python dependencies
├── hardhat.config.js             # Network configurations for Robinhood Chain Mainnet/Testnet
├── package.json                  # Node.js project manifest and smart contract toolchain
├── .gitignore                    # Exclusion rules for secrets, dependencies, and build artifacts
├── .env.example                  # Template for required environment variables
└── LICENSE                       # Proprietary intellectual property license
