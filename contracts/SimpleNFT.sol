// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title SimpleNFT
 * @dev Simple NFT contract for N100 AI-generated art
 * Deployed on Polygon for ultra-low gas fees
 */
contract SimpleNFT is ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    // Collection metadata
    string public collectionName = "N100 AI Collection";
    string public collectionSymbol = "N100";

    // Royalty info (5% = 500 basis points)
    uint256 public royaltyBasisPoints = 500;
    address public royaltyReceiver;

    // Events
    event NFTMinted(address indexed to, uint256 indexed tokenId, string tokenURI);

    constructor() ERC721("N100 AI Collection", "N100") {
        royaltyReceiver = msg.sender;
    }

    /**
     * @dev Mint a new NFT
     * @param recipient Address to receive the NFT
     * @param tokenURI Metadata URI (IPFS link)
     * @return tokenId The ID of the newly minted NFT
     */
    function mintNFT(address recipient, string memory tokenURI)
        public
        onlyOwner
        returns (uint256)
    {
        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();

        _mint(recipient, newTokenId);
        _setTokenURI(newTokenId, tokenURI);

        emit NFTMinted(recipient, newTokenId, tokenURI);

        return newTokenId;
    }

    /**
     * @dev Batch mint multiple NFTs
     * @param recipient Address to receive the NFTs
     * @param tokenURIs Array of metadata URIs
     */
    function batchMint(address recipient, string[] memory tokenURIs)
        public
        onlyOwner
    {
        for (uint256 i = 0; i < tokenURIs.length; i++) {
            mintNFT(recipient, tokenURIs[i]);
        }
    }

    /**
     * @dev Update royalty receiver
     * @param newReceiver New royalty receiver address
     */
    function setRoyaltyReceiver(address newReceiver) public onlyOwner {
        royaltyReceiver = newReceiver;
    }

    /**
     * @dev Update royalty percentage
     * @param newBasisPoints New royalty in basis points (500 = 5%)
     */
    function setRoyaltyBasisPoints(uint256 newBasisPoints) public onlyOwner {
        require(newBasisPoints <= 1000, "Royalty cannot exceed 10%");
        royaltyBasisPoints = newBasisPoints;
    }

    /**
     * @dev Get total supply of NFTs
     * @return Total number of minted NFTs
     */
    function totalSupply() public view returns (uint256) {
        return _tokenIds.current();
    }

    /**
     * @dev EIP-2981 royalty standard support
     */
    function royaltyInfo(uint256 /* tokenId */, uint256 salePrice)
        external
        view
        returns (address receiver, uint256 royaltyAmount)
    {
        royaltyAmount = (salePrice * royaltyBasisPoints) / 10000;
        return (royaltyReceiver, royaltyAmount);
    }

    /**
     * @dev Check interface support
     */
    function supportsInterface(bytes4 interfaceId)
        public
        view
        virtual
        override(ERC721URIStorage)
        returns (bool)
    {
        // EIP-2981 interface ID
        return interfaceId == 0x2a55205a || super.supportsInterface(interfaceId);
    }
}
