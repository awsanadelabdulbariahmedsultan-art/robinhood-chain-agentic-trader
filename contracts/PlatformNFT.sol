// SPDX-License-Identifier: Proprietary
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/common/ERC2981.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title PlatformNFT
 * @dev Tiered Membership & Asset Backed NFT
 * @author Eng. Awsan Adel Abdulbari Ahmed Sultan
 */
contract PlatformNFT is ERC721URIStorage, ERC2981, Ownable {
    uint256 private _nextTokenId;
    uint256 public mintPrice = 0.05 ether;
    uint256 public maxSupply = 5000;

    constructor(address initialOwner, address royaltyReceiver)
        ERC721("Awsan Nexus Asset NFT", "AWNX")
        Ownable(initialOwner)
    {
        _setDefaultRoyalty(royaltyReceiver, 500); // 5% Royalties
    }

    function mint(address to, string memory uri) external payable returns (uint256) {
        require(msg.value >= mintPrice, "Insufficient ETH/Gas sent");
        require(_nextTokenId < maxSupply, "Max supply reached");

        uint256 tokenId = _nextTokenId++;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);

        return tokenId;
    }

    function withdraw(address payable recipient) external onlyOwner {
        require(recipient != address(0), "Invalid address");
        recipient.transfer(address(this).balance);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721URIStorage, ERC2981)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
