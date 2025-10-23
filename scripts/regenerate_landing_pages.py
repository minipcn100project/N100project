"""
Regenerate all existing NFT landing pages with updated template
"""
import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).parent.parent))

from scripts.landing_page_generator import LandingPageGenerator

def load_nft_data():
    """Load NFT data from gallery.json"""
    gallery_file = Path("public/gallery.json")

    if not gallery_file.exists():
        print("No gallery.json found. No NFTs to regenerate.")
        return []

    with open(gallery_file, 'r', encoding='utf-8') as f:
        gallery = json.load(f)

    return gallery.get("nfts", [])

def regenerate_all():
    """Regenerate all NFT landing pages"""
    print("=" * 70)
    print("REGENERATING ALL NFT LANDING PAGES")
    print("Updated features: Holder address + Collection view")
    print("=" * 70)
    print()

    nfts = load_nft_data()

    if not nfts:
        print("No NFTs found to regenerate.")
        return

    gen = LandingPageGenerator()

    for i, nft in enumerate(nfts, 1):
        print(f"[{i}/{len(nfts)}] Regenerating NFT #{nft['index']}...")

        # Convert gallery data to format expected by generator
        nft_data = {
            "index": nft["index"],
            "title": nft["title"],
            "description": nft["description"],
            "mint_url": nft.get("mint_url", ""),
            "price": nft.get("price", 10),
            "style": nft.get("style", "pixelart"),
            "blockchain": nft.get("blockchain", "Polygon"),
            "created_at": nft.get("created_at", "")
        }

        url = gen.generate_nft_page(nft_data)
        print(f"    OK: {url}")

    print()
    print("=" * 70)
    print(f"SUCCESS! Regenerated {len(nfts)} landing pages")
    print("=" * 70)
    print()
    print("New features:")
    print("  - Real-time holder address display")
    print("  - Holder's NFT collection (up to 12 NFTs)")
    print("  - OpenSea profile link")
    print("  - Blockchain data fetched in real-time")
    print()
    print("Next step: Deploy to GitHub Pages")
    print()

if __name__ == "__main__":
    regenerate_all()
