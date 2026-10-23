// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

/**
 * @title GaleriKuliner
 * @dev Kontrak pencatatan hak cipta dan edisi unik karya kuliner lokal (P7).
 */
contract GaleriKuliner is ERC721URIStorage, AccessControl {
    bytes32 public constant CURATOR_ROLE = keccak256("CURATOR_ROLE");
    bytes32 public constant CREATOR_ROLE = keccak256("CREATOR_ROLE");

    uint256 private _nextTokenId;

    // Mapping untuk mencegah duplikasi karya (workId unik)
    mapping(string => bool) private _registeredWorkIds;
    mapping(uint256 => string) private _tokenToWorkId;

    event DishMinted(
        uint256 indexed tokenId,
        string workId,
        address indexed creator,
        address indexed curator,
        string tokenURI
    );

    constructor(address defaultAdmin, address initialCurator) ERC721("Galeri Kuliner Nusantara", "GKN") {
        require(defaultAdmin != address(0), "Admin tidak valid");
        require(initialCurator != address(0), "Kurator tidak valid");

        _grantRole(DEFAULT_ADMIN_ROLE, defaultAdmin);
        _grantRole(CURATOR_ROLE, initialCurator);
    }

    /**
     * @notice Mencetak NFT kuliner baru setelah diverifikasi oleh Kurator.
     * @param to Alamat penerima NFT (kreator/pemilik).
     * @param workId Identifikasi unik hidangan (misal: "soto-001").
     * @param uri CID metadata IPFS.
     */
    function mintDish(
        address to,
        string memory workId,
        string memory uri
    ) external onlyRole(CURATOR_ROLE) returns (uint256) {
        require(to != address(0), "Alamat penerima tidak valid");
        require(bytes(workId).length > 0, "Work ID tidak boleh kosong");
        require(bytes(uri).length > 0, "URI tidak boleh kosong");
        require(!_registeredWorkIds[workId], "ID karya sudah pernah dicetak");

        uint256 tokenId = _nextTokenId++;
        _registeredWorkIds[workId] = true;
        _tokenToWorkId[tokenId] = workId;

        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);

        emit DishMinted(tokenId, workId, to, msg.sender, uri);

        return tokenId;
    }

    /**
     * @notice Memeriksa apakah suatu ID karya sudah pernah didaftarkan.
     */
    function isWorkRegistered(string memory workId) external view returns (bool) {
        return _registeredWorkIds[workId];
    }

    /**
     * @notice Mendapatkan workId berdasarkan tokenId.
     */
    function getWorkIdByTokenId(uint256 tokenId) external view returns (string memory) {
        _requireOwned(tokenId);
        return _tokenToWorkId[tokenId];
    }

    // Resolusi konflik inheritance antara ERC721URIStorage dan AccessControl
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721URIStorage, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}