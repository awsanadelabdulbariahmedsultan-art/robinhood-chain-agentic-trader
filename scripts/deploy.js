/**
 * @title Automated Deployment Script for robinhood-chain-agentic-trader
 * @author Eng. Awsan Adel Abdulbari Ahmed Sultan
 * @notice Deploys PlatformToken, PlatformNFT, and Treasury to Robinhood Chain
 */
const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  console.log("====================================================");
  console.log("Starting Deployment on Network:", hre.network.name);
  console.log("Deployer Address:", deployer.address);
  console.log("Deployer Balance:", (await hre.ethers.provider.getBalance(deployer.address)).toString());
  console.log("Architect & Owner: Eng. Awsan Adel Abdulbari Ahmed Sultan");
  console.log("====================================================");

  // 1. نشر عقد الخزينة اللامركزية (Treasury)
  console.log("\n1. Deploying Treasury Contract...");
  const Treasury = await hre.ethers.getContractFactory("Treasury");
  const treasury = await Treasury.deploy(deployer.address);
  await treasury.waitForDeployment();
  const treasuryAddress = await treasury.getAddress();
  console.log("✔ Treasury deployed at:", treasuryAddress);

  // 2. نشر عقد التوكن (PlatformToken - AWSN)
  console.log("\n2. Deploying Platform Governance Token ($AWSN)...");
  const PlatformToken = await hre.ethers.getContractFactory("PlatformToken");
  const token = await PlatformToken.deploy(deployer.address);
  await token.waitForDeployment();
  const tokenAddress = await token.getAddress();
  console.log("✔ PlatformToken deployed at:", tokenAddress);

  // 3. نشر عقد الـ NFT (PlatformNFT - AWNX) وتعيين الخزينة لتلقي العوائد
  console.log("\n3. Deploying Platform Membership NFT ($AWNX)...");
  const PlatformNFT = await hre.ethers.getContractFactory("PlatformNFT");
  const nft = await PlatformNFT.deploy(deployer.address, treasuryAddress);
  await nft.waitForDeployment();
  const nftAddress = await nft.getAddress();
  console.log("✔ PlatformNFT deployed at:", nftAddress);

  console.log("\n====================================================");
  console.log("Deployment Summary:");
  console.log("Network:", hre.network.name);
  console.log("PlatformToken (ERC-20):", tokenAddress);
  console.log("PlatformNFT (ERC-721):", nftAddress);
  console.log("Treasury:", treasuryAddress);
  console.log("====================================================");
}

main().catch((error) => {
  console.error("Deployment failed:", error);
  process.exitCode = 1;
});
