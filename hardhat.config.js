/**
 * @author Eng. Awsan Adel Abdulbari Ahmed Sultan
 * @notice Hardhat Configuration for Robinhood Chain & EVM Networks
 */
require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

const PRIVATE_KEY = process.env.PRIVATE_KEY || "0x0000000000000000000000000000000000000000000000000000000000000000";

module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    robinhoodMainnet: {
      url: "https://rpc.mainnet.chain.robinhood.com",
      chainId: 4663,
      accounts: [PRIVATE_KEY],
    },
    robinhoodTestnet: {
      url: "https://rpc.testnet.chain.robinhood.com",
      chainId: 46630,
      accounts: [PRIVATE_KEY],
    },
    ethereum: {
      url: process.env.ETH_RPC_URL || "https://rpc.ankr.com/eth",
      chainId: 1,
      accounts: [PRIVATE_KEY],
    },
  },
  etherscan: {
    apiKey: {
      robinhoodMainnet: "empty",
      robinhoodTestnet: "empty",
    },
    customChains: [
      {
        network: "robinhoodMainnet",
        chainId: 4663,
        urls: {
          apiURL: "https://robinhoodchain.blockscout.com/api",
          browserURL: "https://robinhoodchain.blockscout.com",
        },
      },
    ],
  },
};
