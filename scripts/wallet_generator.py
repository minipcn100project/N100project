# scripts/wallet_generator.py
"""
Solana Wallet Generator
Creates a new Solana wallet for NFT minting
"""
import json
from pathlib import Path
from solders.keypair import Keypair
from solders.pubkey import Pubkey

def generate_wallet(output_path="wallet.json"):
    """
    Generate a new Solana wallet keypair

    Args:
        output_path: Path to save the wallet JSON file

    Returns:
        dict: Wallet information including public key and private key
    """
    # Generate new keypair
    keypair = Keypair()

    # Get public key (wallet address)
    public_key = str(keypair.pubkey())

    # Get private key as byte array (compatible with Solana CLI format)
    private_key = list(bytes(keypair))

    # Prepare wallet data
    wallet_data = private_key

    # Save to file
    output_file = Path(output_path)
    with open(output_file, 'w') as f:
        json.dump(wallet_data, f)

    print("=" * 60)
    print("")
    print("  Solana Wallet Generated Successfully!")
    print("")
    print("=" * 60)
    print(f"\nPublic Key (Wallet Address): {public_key}")
    print(f"Wallet file saved to: {output_file.absolute()}")
    print("\nIMPORTANT: Keep your wallet.json file secure!")
    print("This file contains your private key.")
    print("\nFor Devnet testing:")
    print(f"  1. Request airdrop: solana airdrop 2 {public_key} --url devnet")
    print(f"  2. Or use: https://faucet.solana.com/")
    print("\nFor Mainnet:")
    print("  Transfer real SOL to this address to start minting")
    print("=" * 60)

    return {
        "public_key": public_key,
        "wallet_file": str(output_file.absolute())
    }

if __name__ == "__main__":
    # Generate wallet
    generate_wallet()
