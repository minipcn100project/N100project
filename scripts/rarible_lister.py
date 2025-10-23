"""
Python Wrapper for Rarible Auto-Listing
Calls the Node.js Rarible SDK script
"""
import subprocess
import os
import sys
from pathlib import Path

class RaribleLister:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.rarible_script = self.script_dir / "rarible_auto_list.js"

    def list_nft(self, token_id, price_usd=10):
        """
        List single NFT on Rarible
        """
        print(f"[RARIBLE] Listing NFT #{token_id} at ${price_usd} USD...")

        try:
            result = subprocess.run(
                ["node", str(self.rarible_script), str(token_id), str(price_usd)],
                cwd=self.script_dir.parent,
                capture_output=True,
                text=True,
                timeout=120
            )

            print(result.stdout)

            if result.returncode == 0:
                print(f"[OK] NFT #{token_id} listed on Rarible (and OpenSea, LooksRare)")
                return True
            else:
                print(f"[ERROR] Listing failed:")
                print(result.stderr)
                return False

        except subprocess.TimeoutExpired:
            print("[ERROR] Listing timed out after 120 seconds")
            return False
        except Exception as e:
            print(f"[ERROR] {e}")
            return False

    def batch_list(self, token_ids, price_usd=10):
        """
        List multiple NFTs
        """
        token_ids_str = ','.join(map(str, token_ids))
        print(f"[RARIBLE] Batch listing {len(token_ids)} NFTs...")

        try:
            result = subprocess.run(
                ["node", str(self.rarible_script), token_ids_str, str(price_usd)],
                cwd=self.script_dir.parent,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes for batch
            )

            print(result.stdout)

            if result.returncode == 0:
                print(f"[OK] Batch listing complete")
                return True
            else:
                print(f"[ERROR] Batch listing failed:")
                print(result.stderr)
                return False

        except subprocess.TimeoutExpired:
            print("[ERROR] Batch listing timed out")
            return False
        except Exception as e:
            print(f"[ERROR] {e}")
            return False

    def list_all(self, price_usd=10):
        """
        List all NFTs from counter
        """
        print(f"[RARIBLE] Listing all NFTs...")

        try:
            result = subprocess.run(
                ["node", str(self.rarible_script), "all", str(price_usd)],
                cwd=self.script_dir.parent,
                capture_output=True,
                text=True,
                timeout=1800  # 30 minutes for all
            )

            print(result.stdout)

            if result.returncode == 0:
                print(f"[OK] All NFTs listed")
                return True
            else:
                print(f"[ERROR] Listing all failed:")
                print(result.stderr)
                return False

        except subprocess.TimeoutExpired:
            print("[ERROR] Listing all timed out")
            return False
        except Exception as e:
            print(f"[ERROR] {e}")
            return False


if __name__ == "__main__":
    print("=" * 70)
    print("RARIBLE AUTO-LISTING (Python Wrapper)")
    print("=" * 70)
    print()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python rarible_lister.py <tokenId>")
        print("  python rarible_lister.py <tokenId> <price>")
        print("  python rarible_lister.py all")
        print()
        print("Examples:")
        print("  python rarible_lister.py 1")
        print("  python rarible_lister.py 1 15")
        print("  python rarible_lister.py all")
        sys.exit(0)

    lister = RaribleLister()

    if sys.argv[1] == "all":
        price = float(sys.argv[2]) if len(sys.argv) > 2 else 10
        lister.list_all(price)
    else:
        token_id = int(sys.argv[1])
        price = float(sys.argv[2]) if len(sys.argv) > 2 else 10
        lister.list_nft(token_id, price)
