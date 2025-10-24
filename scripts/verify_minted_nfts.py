"""
Verify Minted NFTs
Check which NFTs are actually minted on-chain vs local images only
"""
import os
from pathlib import Path
from web3 import Web3
from dotenv import load_dotenv
import json

load_dotenv()

# Configuration
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "0xf5420c3E42bb575a2c15434278655c837ca3783E")
POLYGON_RPC_URL = os.getenv("POLYGON_RPC_URL", "https://polygon-rpc.com/")

# ERC-721 ABI (minimal - just what we need)
ERC721_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"name": "owner", "type": "address"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "tokenURI",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function"
    }
]

def check_local_images():
    """Check which NFTs have images locally"""
    # Check multiple possible locations
    possible_dirs = [
        Path(__file__).parent.parent / "output" / "images",
        Path(__file__).parent.parent / "output",
        Path(__file__).parent.parent / "docs" / "images"
    ]

    token_ids = []

    for output_dir in possible_dirs:
        if not output_dir.exists():
            continue

        image_files = list(output_dir.glob("nft_*.png"))

        for img in image_files:
            # Extract token ID from filename (nft_000.png -> 0)
            try:
                token_str = img.stem.split('_')[1]
                token_id = int(token_str)
                if token_id not in token_ids:
                    token_ids.append(token_id)
            except:
                continue

    if not token_ids:
        print("[WARNING] No NFT images found")

    return sorted(token_ids)

def check_onchain_nfts(max_token_id=20):
    """Check which NFTs are actually minted on Polygon"""
    print("[INFO] Connecting to Polygon...")
    w3 = Web3(Web3.HTTPProvider(POLYGON_RPC_URL))

    if not w3.is_connected():
        print("[ERROR] Could not connect to Polygon RPC")
        return []

    print(f"[OK] Connected to Polygon (Block #{w3.eth.block_number})")

    # Get contract
    contract_checksum = Web3.to_checksum_address(CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=contract_checksum, abi=ERC721_ABI)

    minted_tokens = []

    print(f"[INFO] Checking tokens 0-{max_token_id}...")

    for token_id in range(max_token_id + 1):
        try:
            # Try to get owner
            owner = contract.functions.ownerOf(token_id).call()

            # If no error, token is minted
            minted_tokens.append({
                'token_id': token_id,
                'owner': owner,
                'minted': True
            })
            print(f"  Token #{token_id}: Minted (Owner: {owner[:8]}...)")

        except Exception as e:
            # Token not minted
            if "execution reverted" in str(e).lower() or "invalid" in str(e).lower():
                print(f"  Token #{token_id}: Not minted")
                minted_tokens.append({
                    'token_id': token_id,
                    'owner': None,
                    'minted': False
                })
            else:
                print(f"  Token #{token_id}: Error - {str(e)[:50]}")

    return minted_tokens

def main():
    print("=" * 70)
    print("NFT MINTING VERIFICATION")
    print("=" * 70)
    print()

    # Check local images
    print("[1/3] Checking local images...")
    local_tokens = check_local_images()
    print(f"[OK] Found {len(local_tokens)} local images: {local_tokens}")
    print()

    # Check on-chain
    print("[2/3] Checking on-chain NFTs...")
    max_token = max(local_tokens) if local_tokens else 20
    onchain_data = check_onchain_nfts(max_token)
    print()

    # Analysis
    print("[3/3] Analysis...")
    print()

    minted_tokens = [d['token_id'] for d in onchain_data if d['minted']]
    unminted_tokens = [d['token_id'] for d in onchain_data if not d['minted']]

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()

    print(f"Local images: {len(local_tokens)}")
    print(f"On-chain minted: {len(minted_tokens)}")
    print(f"Not minted: {len(unminted_tokens)}")
    print()

    # Images with no on-chain mint
    local_set = set(local_tokens)
    minted_set = set(minted_tokens)

    images_not_minted = local_set - minted_set
    minted_no_image = minted_set - local_set

    if images_not_minted:
        print(f"Images NOT minted on-chain: {sorted(images_not_minted)}")
        print("[ACTION REQUIRED] These NFTs need to be minted!")
    else:
        print("All local images are minted on-chain!")
    print()

    if minted_no_image:
        print(f"Minted but no local image: {sorted(minted_no_image)}")
        print("[WARNING] Images may have been deleted or moved")
    print()

    # Save report
    report = {
        'local_images': local_tokens,
        'minted_tokens': minted_tokens,
        'unminted_tokens': unminted_tokens,
        'images_not_minted': sorted(images_not_minted),
        'minted_no_image': sorted(minted_no_image),
        'onchain_details': onchain_data
    }

    report_file = Path(__file__).parent.parent / "nft_verification_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"[OK] Report saved to: {report_file.name}")
    print("=" * 70)

    return report

if __name__ == "__main__":
    main()
