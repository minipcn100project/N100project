"""
OpenSea Playwright Auto-Listing Script
Directly automate OpenSea web interface with browser control
"""
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

load_dotenv()

# Configuration
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "0xf5420c3E42bb575a2c15434278655c837ca3783E")
WALLET_ADDRESS = os.getenv("POLYGON_WALLET_ADDRESS", "0xe8345cff87816bb6a657e45cd5ccbb75846c446f")

class OpenSeaPlaywrightLister:
    def __init__(self, headless=False):
        """
        Initialize Playwright browser
        Args:
            headless: If False, browser will be visible (useful for debugging/MetaMask)
        """
        self.headless = headless
        self.contract_address = CONTRACT_ADDRESS
        self.wallet_address = WALLET_ADDRESS

    def list_nft(self, token_id, price_usd=10, wait_for_metamask=True):
        """
        List NFT on OpenSea
        Args:
            token_id: NFT token ID
            price_usd: Price in USD
            wait_for_metamask: If True, wait for user to manually sign MetaMask
        """
        print(f"[OPENSEA PLAYWRIGHT] Listing NFT #{token_id} at ${price_usd} USD...")

        with sync_playwright() as p:
            # Launch browser (visible for MetaMask interaction)
            print("[1/8] Launching browser...")
            browser = p.chromium.launch(headless=self.headless)

            # Create context with viewport
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )

            page = context.new_page()

            try:
                # Navigate to NFT page
                nft_url = f"https://opensea.io/assets/matic/{self.contract_address}/{token_id}"
                print(f"[2/8] Navigating to: {nft_url}")
                page.goto(nft_url, wait_until='networkidle', timeout=30000)

                # Wait for page to load
                time.sleep(3)

                # Take screenshot for debugging
                screenshot_dir = Path(__file__).parent.parent / "screenshots"
                screenshot_dir.mkdir(exist_ok=True)
                page.screenshot(path=str(screenshot_dir / f"opensea_nft_{token_id}_page.png"))
                print(f"[DEBUG] Screenshot saved: opensea_nft_{token_id}_page.png")

                # Check if NFT exists
                try:
                    page.wait_for_selector('h1', timeout=5000)
                    nft_title = page.query_selector('h1')
                    if nft_title:
                        print(f"[INFO] NFT found: {nft_title.inner_text()}")
                except:
                    print("[WARNING] Could not find NFT title - NFT may not exist on OpenSea yet")
                    print("[INFO] NFT may need time to be indexed by OpenSea (5-10 minutes after minting)")
                    browser.close()
                    return False

                # Look for "Sell" button
                print("[3/8] Looking for Sell button...")
                sell_selectors = [
                    'button:has-text("Sell")',
                    'a:has-text("Sell")',
                    '[data-testid="sell-button"]',
                    'button[aria-label="Sell"]'
                ]

                sell_button = None
                for selector in sell_selectors:
                    try:
                        sell_button = page.wait_for_selector(selector, timeout=3000)
                        if sell_button:
                            print(f"[OK] Found Sell button with selector: {selector}")
                            break
                    except:
                        continue

                if not sell_button:
                    print("[ERROR] Could not find Sell button")
                    print("[INFO] Possible reasons:")
                    print("  - NFT not owned by connected wallet")
                    print("  - Already listed for sale")
                    print("  - Need to connect wallet first")
                    page.screenshot(path=str(screenshot_dir / f"opensea_nft_{token_id}_no_sell_button.png"))
                    browser.close()
                    return False

                # Click Sell button
                print("[4/8] Clicking Sell button...")
                sell_button.click()
                time.sleep(2)

                # Screenshot after clicking Sell
                page.screenshot(path=str(screenshot_dir / f"opensea_nft_{token_id}_sell_form.png"))

                # Wait for listing form
                print("[5/8] Waiting for listing form...")
                try:
                    # Look for price input
                    price_selectors = [
                        'input[name="price"]',
                        'input[placeholder*="Amount"]',
                        'input[type="number"]',
                        'input[id*="price"]'
                    ]

                    price_input = None
                    for selector in price_selectors:
                        try:
                            price_input = page.wait_for_selector(selector, timeout=3000)
                            if price_input:
                                print(f"[OK] Found price input: {selector}")
                                break
                        except:
                            continue

                    if price_input:
                        # Clear and enter price
                        print(f"[6/8] Entering price: ${price_usd} USD...")
                        price_input.click()
                        price_input.fill("")
                        price_input.type(str(price_usd), delay=100)
                        time.sleep(1)

                        # Screenshot after price entry
                        page.screenshot(path=str(screenshot_dir / f"opensea_nft_{token_id}_price_entered.png"))

                        # Look for "Complete listing" button
                        print("[7/8] Looking for Complete listing button...")
                        complete_selectors = [
                            'button:has-text("Complete listing")',
                            'button:has-text("Complete")',
                            'button:has-text("List")',
                            '[data-testid="complete-listing-button"]'
                        ]

                        complete_button = None
                        for selector in complete_selectors:
                            try:
                                complete_button = page.wait_for_selector(selector, timeout=3000)
                                if complete_button:
                                    print(f"[OK] Found Complete listing button: {selector}")
                                    break
                            except:
                                continue

                        if complete_button:
                            print("[8/8] Clicking Complete listing...")
                            complete_button.click()

                            if wait_for_metamask:
                                print()
                                print("=" * 70)
                                print("METAMASK SIGNATURE REQUIRED")
                                print("=" * 70)
                                print()
                                print("Please sign the transaction in MetaMask popup window.")
                                print("Waiting 60 seconds for signature...")
                                print()
                                time.sleep(60)

                                # Check if listing succeeded
                                page.screenshot(path=str(screenshot_dir / f"opensea_nft_{token_id}_after_sign.png"))

                                print()
                                print("=" * 70)
                                print("LISTING COMPLETE")
                                print("=" * 70)
                                print(f"NFT #{token_id} listed at ${price_usd} USD")
                                print(f"OpenSea URL: {nft_url}")
                                print()
                                print("Note: It may take a few minutes for the listing to appear")
                                print("=" * 70)

                                browser.close()
                                return True
                        else:
                            print("[ERROR] Could not find Complete listing button")
                            browser.close()
                            return False
                    else:
                        print("[ERROR] Could not find price input field")
                        browser.close()
                        return False

                except PlaywrightTimeout as e:
                    print(f"[ERROR] Timeout waiting for form elements: {e}")
                    browser.close()
                    return False

            except Exception as e:
                print(f"[ERROR] Failed to list NFT: {e}")
                page.screenshot(path=str(screenshot_dir / f"opensea_nft_{token_id}_error.png"))
                browser.close()
                return False

    def batch_list(self, token_ids, price_usd=10):
        """
        List multiple NFTs
        """
        print("=" * 70)
        print(f"BATCH LISTING {len(token_ids)} NFTs ON OPENSEA")
        print("=" * 70)
        print()

        results = []
        for token_id in token_ids:
            result = self.list_nft(token_id, price_usd)
            results.append({
                'token_id': token_id,
                'success': result
            })

            # Wait between listings
            if token_id != token_ids[-1]:
                print()
                print("[INFO] Waiting 10 seconds before next listing...")
                time.sleep(10)

        # Summary
        print()
        print("=" * 70)
        print("BATCH LISTING SUMMARY")
        print("=" * 70)
        print(f"Total: {len(token_ids)}")
        print(f"Success: {sum(1 for r in results if r['success'])}")
        print(f"Failed: {sum(1 for r in results if not r['success'])}")
        print("=" * 70)

        return results


def main():
    if len(sys.argv) < 2:
        print()
        print("=" * 70)
        print("OPENSEA PLAYWRIGHT AUTO-LISTING")
        print("=" * 70)
        print()
        print("Usage:")
        print("  python opensea_playwright_list.py <tokenId>")
        print("  python opensea_playwright_list.py <tokenId> <price>")
        print("  python opensea_playwright_list.py 1,2,3")
        print()
        print("Examples:")
        print("  python opensea_playwright_list.py 1")
        print("  python opensea_playwright_list.py 1 15")
        print("  python opensea_playwright_list.py 1,2,3,4,5")
        print()
        print("=" * 70)
        sys.exit(0)

    lister = OpenSeaPlaywrightLister(headless=False)

    token_arg = sys.argv[1]
    price = float(sys.argv[2]) if len(sys.argv) > 2 else 10

    # Single token
    if ',' not in token_arg:
        token_id = int(token_arg)
        lister.list_nft(token_id, price)
    # Batch tokens
    else:
        token_ids = [int(t.strip()) for t in token_arg.split(',')]
        lister.batch_list(token_ids, price)


if __name__ == "__main__":
    main()
