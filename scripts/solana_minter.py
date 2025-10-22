# scripts/solana_minter.py
"""
Solana NFT Lazy Minting (간소화 버전)
실제로는 Candy Machine 또는 Metaplex를 사용해야 합니다.
"""
import json
import os
from pathlib import Path

class SolanaNFTMinter:
    """
    간소화된 솔라나 NFT Minter
    실제 구현은 Metaplex Candy Machine 사용
    """
    def __init__(self):
        self.metadata_dir = Path("output/metadata")
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        self.candy_machine_id = os.getenv("CANDY_MACHINE_ID", "")

    def add_to_candy_machine(self, image_path, title, description, index):
        """
        Candy Machine에 NFT 추가 (Lazy Minting)

        실제로는 Sugar CLI 또는 Metaplex SDK 사용
        여기서는 메타데이터만 준비
        """
        # 메타데이터 생성
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

        # 메타데이터 저장
        metadata_file = self.metadata_dir / f"{index}.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"📝 Metadata saved: {metadata_file}")

        # 민팅 URL 생성 (실제로는 Candy Machine URL)
        if self.candy_machine_id:
            mint_url = f"https://magiceden.io/launchpad/{self.candy_machine_id}"
        else:
            # 개발 중에는 랜딩페이지 URL 사용
            mint_url = f"https://{os.getenv('DOMAIN')}/nft/{index}.html"

        return {
            "status": "added_to_candy_machine",
            "mint_url": mint_url,
            "metadata_uri": f"https://arweave.net/{index}.json"  # 실제로는 업로드 필요
        }


def mint_nft(image_path, title, description, index):
    """
    간편 사용 함수
    """
    minter = SolanaNFTMinter()
    return minter.add_to_candy_machine(image_path, title, description, index)


if __name__ == "__main__":
    # 테스트
    result = mint_nft("test.png", "Test NFT", "Test Description", 999)
    print(json.dumps(result, indent=2))
