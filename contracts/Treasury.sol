// SPDX-License-Identifier: Proprietary
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/**
 * @title PlatformTreasury
 * @dev Treasury Management and Fund Allocation
 * @author Eng. Awsan Adel Abdulbari Ahmed Sultan
 */
contract PlatformTreasury is Ownable {
    event FundsReceived(address indexed from, uint256 amount);
    event FundsDispatched(address indexed to, uint256 amount, string reason);

    constructor(address initialOwner) Ownable(initialOwner) {}

    receive() external payable {
        emit FundsReceived(msg.sender, msg.value);
    }

    function dispatchNativeFunds(address payable recipient, uint256 amount, string calldata reason) 
        external 
        onlyOwner 
    {
        require(address(this).balance >= amount, "Insufficient treasury balance");
        recipient.transfer(amount);
        emit FundsDispatched(recipient, amount, reason);
    }

    function dispatchToken(address tokenAddress, address recipient, uint256 amount) 
        external 
        onlyOwner 
    {
        require(IERC20(tokenAddress).transfer(recipient, amount), "Token transfer failed");
    }
}
