# scripts/web_automation.py
"""
Playwright    
Twitter API    
NFT     
"""
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import os
import time
from pathlib import Path

class WebAutomation:
    def __init__(self, headless=True):
        """
        Args:
            headless: True  , False   
        """
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    def start(self):
        """ """
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            self.page = self.browser.new_page()
            print(" Browser started")
        except Exception as e:
            print(f" Failed to start browser: {e}")
            raise

    def stop(self):
        """ """
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print(" Browser closed")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def take_screenshot(self, filename):
        """ """
        screenshot_dir = Path("logs/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        path = screenshot_dir / filename
        self.page.screenshot(path=str(path))
        return str(path)


class TwitterWebPoster(WebAutomation):
    """
    Twitter   
    API    
    """
    def __init__(self, headless=True):
        super().__init__(headless)
        self.twitter_username = os.getenv("TWITTER_USERNAME")
        self.twitter_password = os.getenv("TWITTER_PASSWORD")

    def login(self):
        """Twitter """
        try:
            print(" Logging in to Twitter...")
            self.page.goto("https://twitter.com/i/flow/login", wait_until="networkidle")

            #  
            self.page.fill("input[autocomplete='username']", self.twitter_username)
            self.page.click("div[role='button']:has-text('Next')")
            time.sleep(2)

            #  
            self.page.fill("input[autocomplete='current-password']", self.twitter_password)
            self.page.click("div[data-testid='LoginForm_Login_Button']")
            time.sleep(3)

            #  
            self.page.wait_for_url("https://twitter.com/home", timeout=10000)
            print(" Logged in to Twitter")
            return True

        except Exception as e:
            print(f" Twitter login failed: {e}")
            self.take_screenshot("twitter_login_error.png")
            return False

    def post_tweet(self, text, image_path=None):
        """
         

        Args:
            text:  
            image_path:    ()
        """
        try:
            print(" Posting tweet...")

            #    
            self.page.goto("https://twitter.com/compose/tweet", wait_until="networkidle")
            time.sleep(2)

            #  
            textbox = self.page.locator("div[role='textbox']").first
            textbox.fill(text)

            #   ( )
            if image_path and os.path.exists(image_path):
                print(f" Uploading image: {image_path}")
                file_input = self.page.locator("input[type='file']").first
                file_input.set_input_files(image_path)
                time.sleep(3)  #   

            #   
            self.page.click("div[data-testid='tweetButtonInline']")
            time.sleep(5)  #   

            print(" Tweet posted successfully")
            self.take_screenshot("tweet_success.png")

            return {
                "success": True,
                "message": "Tweet posted"
            }

        except Exception as e:
            print(f" Failed to post tweet: {e}")
            self.take_screenshot("tweet_error.png")
            return {
                "success": False,
                "error": str(e)
            }


class SolanaExplorerChecker(WebAutomation):
    """
    Solana Explorer  
    """
    def check_transaction(self, tx_hash, network="devnet"):
        """
            

        Args:
            tx_hash:  
            network: "mainnet-beta" or "devnet"
        """
        try:
            url = f"https://explorer.solana.com/tx/{tx_hash}"
            if network == "devnet":
                url += "?cluster=devnet"

            print(f" Checking transaction: {tx_hash}")
            self.page.goto(url, wait_until="networkidle")
            time.sleep(3)

            #  
            screenshot_path = self.take_screenshot(f"tx_{tx_hash[:8]}.png")

            #  
            try:
                success_element = self.page.locator("text=Success").first
                if success_element.is_visible():
                    status = "Success"
                else:
                    status = "Failed"
            except:
                status = "Unknown"

            print(f" Transaction status: {status}")

            return {
                "tx_hash": tx_hash,
                "status": status,
                "screenshot": screenshot_path,
                "url": url
            }

        except Exception as e:
            print(f" Failed to check transaction: {e}")
            return {
                "tx_hash": tx_hash,
                "status": "Error",
                "error": str(e)
            }


class NFTMarketplaceUploader(WebAutomation):
    """
    NFT   
    (Magic Eden, Tensor )
    """
    def upload_to_magic_eden(self, nft_data):
        """
        Magic Eden Launchpad NFT 

        Args:
            nft_data: {
                "title": "NFT Title",
                "description": "Description",
                "image_path": "path/to/image.png",
                "price": 0.5,
                "collection": "collection_id"
            }
        """
        try:
            print(" Uploading to Magic Eden...")

            # Magic Eden Launchpad
            self.page.goto("https://magiceden.io/launchpad/create")
            time.sleep(3)

            #   (Phantom)
            # :  Phantom       
            try:
                connect_btn = self.page.locator("button:has-text('Connect Wallet')").first
                if connect_btn.is_visible():
                    connect_btn.click()
                    time.sleep(2)

                    # Phantom 
                    phantom_btn = self.page.locator("button:has-text('Phantom')").first
                    phantom_btn.click()
                    time.sleep(5)
            except:
                pass

            # NFT  
            self.page.fill("input[name='name']", nft_data['title'])
            self.page.fill("textarea[name='description']", nft_data['description'])

            #  
            if nft_data.get('image_path'):
                file_input = self.page.locator("input[type='file']").first
                file_input.set_input_files(nft_data['image_path'])
                time.sleep(5)

            #  
            self.page.fill("input[name='price']", str(nft_data['price']))

            # Submit
            self.page.click("button:has-text('Create')")
            time.sleep(10)

            #  
            mint_url = self.page.url
            self.take_screenshot("magic_eden_upload_success.png")

            print(f" Uploaded to Magic Eden: {mint_url}")

            return {
                "success": True,
                "mint_url": mint_url
            }

        except Exception as e:
            print(f" Magic Eden upload failed: {e}")
            self.take_screenshot("magic_eden_upload_error.png")
            return {
                "success": False,
                "error": str(e)
            }


#   
def post_to_twitter_web(text, image_path=None):
    """
    Twitter    ( )
    """
    with TwitterWebPoster(headless=True) as twitter:
        if twitter.login():
            return twitter.post_tweet(text, image_path)
        else:
            return {"success": False, "error": "Login failed"}


def check_solana_tx(tx_hash, network="devnet"):
    """
    Solana   ( )
    """
    with SolanaExplorerChecker(headless=True) as checker:
        return checker.check_transaction(tx_hash, network)


if __name__ == "__main__":
    # 
    print("Testing web automation...")

    # Solana   
    # result = check_solana_tx("test_hash_123", "devnet")
    # print(result)

    print("Web automation module ready!")
