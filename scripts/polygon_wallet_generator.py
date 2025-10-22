# scripts/polygon_wallet_generator.py
"""
Polygon/Ethereum Wallet Generator
Creates a new wallet for Polygon NFT minting
"""
import json
from pathlib import Path
from eth_account import Account

def generate_polygon_wallet(output_path="polygon_wallet.json"):
    """
    Generate a new Polygon/Ethereum wallet

    Args:
        output_path: Path to save the wallet JSON file

    Returns:
        dict: Wallet information including address and private key
    """
    # Enable unaudited HD features for account generation
    Account.enable_unaudited_hdwallet_features()

    # Generate new account
    account = Account.create()

    # Get wallet address and private key
    address = account.address
    private_key = account.key.hex()

    # Prepare wallet data for storage
    wallet_data = {
        "address": address,
        "private_key": private_key
    }

    # Save to file
    output_file = Path(output_path)
    with open(output_file, 'w') as f:
        json.dump(wallet_data, f, indent=2)

    print("=" * 70)
    print("")
    print("  Polygon Wallet Generated Successfully!")
    print("")
    print("=" * 70)
    print(f"\nWallet Address: {address}")
    print(f"Wallet file saved to: {output_file.absolute()}")
    print("\nIMPORTANT: Keep your polygon_wallet.json file SECURE!")
    print("This file contains your private key.")
    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("\n1. FOR TESTING (Mumbai Testnet - FREE):")
    print(f"   - Visit: https://faucet.quicknode.com/polygon/mumbai")
    print(f"   - Enter address: {address}")
    print(f"   - Get FREE test MATIC (0.05 MATIC)")
    print(f"   - Repeat every 12 hours if needed")
    print("\n   Alternative faucets:")
    print(f"   - https://mumbaifaucet.com/")
    print(f"   - https://faucet.polygon.technology/")
    print("\n2. FOR PRODUCTION (Polygon Mainnet - ALMOST FREE):")
    print(f"   - Buy MATIC on exchange (Binance, Coinbase, etc)")
    print(f"   - Send to: {address}")
    print(f"   - Cost: ~$0.01 per NFT mint")
    print("\n3. Check your balance:")
    print("   Mumbai Testnet:")
    print(f"   https://mumbai.polygonscan.com/address/{address}")
    print("\n   Polygon Mainnet:")
    print(f"   https://polygonscan.com/address/{address}")
    print("\n" + "=" * 70)

    return {
        "address": address,
        "wallet_file": str(output_file.absolute())
    }

if __name__ == "__main__":
    # Generate wallet
    generate_polygon_wallet()
