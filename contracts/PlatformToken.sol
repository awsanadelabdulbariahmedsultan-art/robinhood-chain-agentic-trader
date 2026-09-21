// SPDX-License-Identifier: Proprietary
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title PlatformToken
 * @dev Governance & Utility Token
 * @author Eng. Awsan Adel Abdulbari Ahmed Sultan
 */
contract PlatformToken is ERC20, ERC20Burnable, Ownable {
    uint256 public constant MAX_SUPPLY = 100_000_000 * 10**18; // 100 Million Tokens

    constructor(address initialOwner) 
        ERC20("Awsan FinTech Governance Token", "AWSN") 
        Ownable(initialOwner) 
    {
        _mint(initialOwner, 10_000_000 * 10**18); // 10% Initial allocation
    }

    function mint(address to, uint256 amount) external onlyOwner {
        require(totalSupply() + amount <= MAX_SUPPLY, "Exceeds max supply");
        _mint(to, amount);
    }
}
