# scripts/solana_minter.py
"""
Solana NFT Lazy Minting ( )
 Candy Machine  Metaplex  .
"""
import json
import os
from pathlib import Path

class SolanaNFTMinter:
    """
      NFT Minter
      Metaplex Candy Machine 
    """
    def __init__(self):
        self.metadata_dir = Path("output/metadata")
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        self.candy_machine_id = os.getenv("CANDY_MACHINE_ID", "")

    def add_to_candy_machine(self, image_path, title, description, index):
        """
        Candy Machine NFT  (Lazy Minting)

         Sugar CLI  Metaplex SDK 
          
        """
        #  
        metadata = {
            "name": f"{title} #{index:03d}",
            "symbol": os.getenv("NFT_SYMBOL", "N100"),
            "description": description,
            "seller_fee_basis_points": int(os.getenv("NFT_ROYALTY_PERCENT", "5")) * 100,
            "image": f"{index}.png",
            "attributes": [
                {"trait_type": "Generation", "value": "AI"},
                {"trait_type": "Hardware", "value": "Intel N100 CPU"},
                {"trait_type": "GPU", "value": "None"},
                {"trait_type": "Style", "value": os.path.basename(image_path).split('_')[0]}
            ],
            "properties": {
                "files": [
                    {"uri": f"{index}.png", "type": "image/png"}
                ],
                "category": "image",
                "creators": [
                    {
                        "address": os.getenv("SOLANA_WALLET_ADDRESS", ""),
                        "share": 100
                    }
                ]
            }
        }

        #  
        metadata_file = self.metadata_dir / f"{index}.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f" Metadata saved: {metadata_file}")

        #  URL  ( Candy Machine URL)
        if self.candy_machine_id:
            mint_url = f"https://magiceden.io/launchpad/{self.candy_machine_id}"
        else:
            #    URL 
            mint_url = f"https://{os.getenv('DOMAIN')}/nft/{index}.html"

        return {
            "status": "added_to_candy_machine",
            "mint_url": mint_url,
            "metadata_uri": f"https://arweave.net/{index}.json"  #   
        }


def mint_nft(image_path, title, description, index):
    """
      
    """
    minter = SolanaNFTMinter()
    return minter.add_to_candy_machine(image_path, title, description, index)


if __name__ == "__main__":
    # 
    result = mint_nft("test.png", "Test NFT", "Test Description", 999)
    print(json.dumps(result, indent=2))
