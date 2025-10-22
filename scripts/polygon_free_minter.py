# scripts/polygon_free_minter.py
"""
Polygon Free NFT Minter
Mints NFTs on Polygon Mumbai (testnet) or Mainnet with minimal gas fees
Uses NFT.Storage for free IPFS hosting
"""
import json
import os
import requests
from pathlib import Path
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv

load_dotenv()

class PolygonFreeMinter:
    """
    Free NFT Minter for Polygon blockchain
    """
    def __init__(self, network="mumbai"):
        """
        Initialize Polygon minter

        Args:
            network: "mumbai" (testnet) or "polygon" (mainnet)
        """
        self.network = network

        # Set RPC URL based on network
        if network == "polygon":
            # Mainnet - ultra-low gas fees (~$0.01)
            self.rpc_url = os.getenv("POLYGON_RPC_URL", "https://polygon-rpc.com")
            self.chain_id = 137
            self.explorer = "https://polygonscan.com"
        else:
            # Mumbai testnet - completely FREE
            self.rpc_url = os.getenv("POLYGON_MUMBAI_RPC_URL", "https://rpc-mumbai.maticvigil.com")
            self.chain_id = 80001
            self.explorer = "https://mumbai.polygonscan.com"

        # Initialize Web3
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))

        # Load wallet
        wallet_path = Path(os.getenv("POLYGON_WALLET_PATH", "polygon_wallet.json"))
        if wallet_path.exists():
            with open(wallet_path, 'r') as f:
                wallet_data = json.load(f)
            self.private_key = wallet_data["private_key"]
            self.account = Account.from_key(self.private_key)
            self.wallet_address = self.account.address
        else:
            raise FileNotFoundError(
                f"Wallet file not found at {wallet_path}. "
                "Run 'python scripts/polygon_wallet_generator.py' to create one."
            )

        # Contract address (set after deployment)
        self.contract_address = os.getenv("POLYGON_CONTRACT_ADDRESS", "")

        # NFT.Storage API key
        self.nft_storage_key = os.getenv("NFT_STORAGE_API_KEY", "")

        self.metadata_dir = Path("output/metadata")
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

        print(f"Initialized Polygon Minter")
        print(f"Network: {self.network.upper()}")
        print(f"Chain ID: {self.chain_id}")
        print(f"RPC: {self.rpc_url}")
        print(f"Wallet: {self.wallet_address}")
        print(f"Explorer: {self.explorer}")

    def check_balance(self):
        """
        Check wallet MATIC balance

        Returns:
            float: MATIC balance
        """
        try:
            balance_wei = self.w3.eth.get_balance(self.wallet_address)
            balance_matic = self.w3.from_wei(balance_wei, 'ether')
            print(f"Wallet Balance: {balance_matic:.4f} MATIC ({balance_wei} wei)")
            return float(balance_matic)
        except Exception as e:
            print(f"Error checking balance: {e}")
            return 0.0

    def upload_to_nft_storage(self, image_path, metadata):
        """
        Upload image and metadata to NFT.Storage (free IPFS hosting)

        Args:
            image_path: Path to image file
            metadata: NFT metadata dict

        Returns:
            str: IPFS URL for metadata
        """
        if not self.nft_storage_key:
            print("[WARNING] NFT_STORAGE_API_KEY not set!")
            print("Get free API key at: https://nft.storage/")
            print("For now, using local storage...")
            return self._create_local_metadata(image_path, metadata)

        try:
            # Upload image first
            with open(image_path, 'rb') as f:
                image_response = requests.post(
                    'https://api.nft.storage/upload',
                    headers={'Authorization': f'Bearer {self.nft_storage_key}'},
                    files={'file': f}
                )

            if image_response.status_code != 200:
                print(f"[ERROR] Image upload failed: {image_response.text}")
                return self._create_local_metadata(image_path, metadata)

            image_cid = image_response.json()['value']['cid']
            image_url = f"ipfs://{image_cid}"

            # Update metadata with IPFS image URL
            metadata['image'] = image_url

            # Upload metadata
            metadata_response = requests.post(
                'https://api.nft.storage/upload',
                headers={
                    'Authorization': f'Bearer {self.nft_storage_key}',
                    'Content-Type': 'application/json'
                },
                data=json.dumps(metadata)
            )

            if metadata_response.status_code != 200:
                print(f"[ERROR] Metadata upload failed: {metadata_response.text}")
                return self._create_local_metadata(image_path, metadata)

            metadata_cid = metadata_response.json()['value']['cid']
            metadata_url = f"ipfs://{metadata_cid}"

            print(f"[SUCCESS] Uploaded to IPFS:")
            print(f"  Image: {image_url}")
            print(f"  Metadata: {metadata_url}")

            return metadata_url

        except Exception as e:
            print(f"[ERROR] NFT.Storage upload failed: {e}")
            return self._create_local_metadata(image_path, metadata)

    def _create_local_metadata(self, image_path, metadata):
        """
        Create local metadata file (fallback if IPFS upload fails)

        Args:
            image_path: Path to image
            metadata: NFT metadata

        Returns:
            str: URL to metadata
        """
        # Use GitHub Pages URL
        index = metadata.get('index', 1)
        metadata['image'] = f"https://{os.getenv('DOMAIN')}/images/nft_{index:03d}.png"

        metadata_file = self.metadata_dir / f"{index}.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        metadata_url = f"https://{os.getenv('DOMAIN')}/metadata/{index}.json"
        print(f"[INFO] Using local metadata: {metadata_url}")

        return metadata_url

    def mint_nft_simple(self, image_path, title, description, index, style="unknown"):
        """
        Mint NFT on Polygon (simplified version without deployed contract)

        For full minting, you need to:
        1. Deploy SimpleNFT.sol contract
        2. Set POLYGON_CONTRACT_ADDRESS in .env
        3. Call contract's mintNFT function

        This function:
        - Creates metadata
        - Uploads to IPFS (if API key set)
        - Checks wallet balance
        - Prepares for actual minting

        Args:
            image_path: Path to image
            title: NFT title
            description: NFT description
            index: NFT number
            style: Art style

        Returns:
            dict: Minting result
        """
        print("\n" + "=" * 70)
        print(f"  Minting NFT #{index:03d} on Polygon {self.network.upper()}")
        print("=" * 70)

        # Check balance
        balance = self.check_balance()

        if balance < 0.01 and self.network == "mumbai":
            print("\n[WARNING] Low MATIC balance!")
            print("Get FREE test MATIC from:")
            print(f"  - https://faucet.quicknode.com/polygon/mumbai")
            print(f"  - https://mumbaifaucet.com/")
            print(f"\nYour wallet: {self.wallet_address}")
        elif balance < 0.1 and self.network == "polygon":
            print("\n[WARNING] Low MATIC balance for mainnet!")
            print("Please fund your wallet with MATIC")

        # Create metadata
        metadata = {
            "name": f"{title} #{index:03d}",
            "description": description,
            "image": "",  # Will be filled by upload_to_nft_storage
            "external_url": f"https://{os.getenv('DOMAIN')}/nft/{index}.html",
            "attributes": [
                {"trait_type": "Generation", "value": "AI"},
                {"trait_type": "Hardware", "value": "Intel N100 CPU"},
                {"trait_type": "GPU", "value": "None"},
                {"trait_type": "Style", "value": style},
                {"trait_type": "Network", "value": self.network}
            ],
            "index": index
        }

        # Upload to IPFS
        metadata_uri = self.upload_to_nft_storage(image_path, metadata)

        # Prepare result
        result = {
            "status": "metadata_created",
            "network": self.network,
            "chain_id": self.chain_id,
            "wallet": self.wallet_address,
            "balance_matic": balance,
            "nft_index": index,
            "title": title,
            "metadata_uri": metadata_uri,
            "mint_url": f"https://{os.getenv('DOMAIN')}/nft/{index}.html",
            "explorer_url": f"{self.explorer}/address/{self.wallet_address}",
            "note": "To mint on-chain, deploy SimpleNFT.sol contract first"
        }

        print("\n[SUCCESS] NFT Metadata Created!")
        print(f"Metadata URI: {metadata_uri}")
        print(f"View at: {result['mint_url']}")
        print(f"Explorer: {result['explorer_url']}")
        print("=" * 70)

        return result


def mint_nft(image_path, title, description, index, network="mumbai"):
    """
    Mint NFT to Polygon blockchain

    Args:
        image_path: Path to NFT image
        title: NFT title
        description: Description
        index: NFT number
        network: "mumbai" (free testnet) or "polygon" (mainnet, ~$0.01)

    Returns:
        dict: Minting result
    """
    # Extract style from image path
    style = Path(image_path).stem.split('_')[0] if '_' in Path(image_path).stem else "unknown"

    try:
        minter = PolygonFreeMinter(network=network)
        return minter.mint_nft_simple(image_path, title, description, index, style)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        print("\nTo create a wallet, run:")
        print("  python scripts/polygon_wallet_generator.py")
        return {
            "status": "error",
            "error": str(e)
        }
    except Exception as e:
        print(f"[ERROR] Minting failed: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


if __name__ == "__main__":
    # Test minting
    import sys

    network = "mumbai"
    if len(sys.argv) > 1 and sys.argv[1] == "--mainnet":
        network = "polygon"

    print(f"\nTesting NFT Minting on Polygon {network.upper()}\n")

    result = mint_nft(
        image_path="output/images/nft_002.png",
        title="Test Polygon NFT",
        description="Test NFT for Polygon blockchain - FREE on Mumbai testnet!",
        index=999,
        network=network
    )

    print("\nResult:")
    print(json.dumps(result, indent=2))
