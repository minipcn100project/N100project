# scripts/web_automation.py
"""
Playwright를 사용한 웹 브라우저 자동화
Twitter API 대신 웹에서 직접 포스팅하거나
NFT 마켓플레이스에 직접 업로드할 때 사용
"""
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import os
import time
from pathlib import Path

class WebAutomation:
    def __init__(self, headless=True):
        """
        Args:
            headless: True면 백그라운드 실행, False면 브라우저 창 보임
        """
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    def start(self):
        """브라우저 시작"""
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            self.page = self.browser.new_page()
            print("✅ Browser started")
        except Exception as e:
            print(f"❌ Failed to start browser: {e}")
            raise

    def stop(self):
        """브라우저 종료"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        print("✅ Browser closed")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def take_screenshot(self, filename):
        """스크린샷 저장"""
        screenshot_dir = Path("logs/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        path = screenshot_dir / filename
        self.page.screenshot(path=str(path))
        return str(path)


class TwitterWebPoster(WebAutomation):
    """
    Twitter 웹에서 직접 포스팅
    API 키 없이 사용 가능
    """
    def __init__(self, headless=True):
        super().__init__(headless)
        self.twitter_username = os.getenv("TWITTER_USERNAME")
        self.twitter_password = os.getenv("TWITTER_PASSWORD")

    def login(self):
        """Twitter 로그인"""
        try:
            print("🔐 Logging in to Twitter...")
            self.page.goto("https://twitter.com/i/flow/login", wait_until="networkidle")

            # 사용자명 입력
            self.page.fill("input[autocomplete='username']", self.twitter_username)
            self.page.click("div[role='button']:has-text('Next')")
            time.sleep(2)

            # 비밀번호 입력
            self.page.fill("input[autocomplete='current-password']", self.twitter_password)
            self.page.click("div[data-testid='LoginForm_Login_Button']")
            time.sleep(3)

            # 로그인 확인
            self.page.wait_for_url("https://twitter.com/home", timeout=10000)
            print("✅ Logged in to Twitter")
            return True

        except Exception as e:
            print(f"❌ Twitter login failed: {e}")
            self.take_screenshot("twitter_login_error.png")
            return False

    def post_tweet(self, text, image_path=None):
        """
        트윗 포스팅

        Args:
            text: 트윗 텍스트
            image_path: 이미지 파일 경로 (선택)
        """
        try:
            print("🐦 Posting tweet...")

            # 트윗 작성 페이지로 이동
            self.page.goto("https://twitter.com/compose/tweet", wait_until="networkidle")
            time.sleep(2)

            # 텍스트 입력
            textbox = self.page.locator("div[role='textbox']").first
            textbox.fill(text)

            # 이미지 업로드 (있는 경우)
            if image_path and os.path.exists(image_path):
                print(f"📸 Uploading image: {image_path}")
                file_input = self.page.locator("input[type='file']").first
                file_input.set_input_files(image_path)
                time.sleep(3)  # 이미지 업로드 대기

            # 트윗 버튼 클릭
            self.page.click("div[data-testid='tweetButtonInline']")
            time.sleep(5)  # 포스팅 완료 대기

            print("✅ Tweet posted successfully")
            self.take_screenshot("tweet_success.png")

            return {
                "success": True,
                "message": "Tweet posted"
            }

        except Exception as e:
            print(f"❌ Failed to post tweet: {e}")
            self.take_screenshot("tweet_error.png")
            return {
                "success": False,
                "error": str(e)
            }


class SolanaExplorerChecker(WebAutomation):
    """
    Solana Explorer에서 트랜잭션 확인
    """
    def check_transaction(self, tx_hash, network="devnet"):
        """
        트랜잭션 상태 확인 및 스크린샷

        Args:
            tx_hash: 트랜잭션 해시
            network: "mainnet-beta" or "devnet"
        """
        try:
            url = f"https://explorer.solana.com/tx/{tx_hash}"
            if network == "devnet":
                url += "?cluster=devnet"

            print(f"🔍 Checking transaction: {tx_hash}")
            self.page.goto(url, wait_until="networkidle")
            time.sleep(3)

            # 스크린샷 저장
            screenshot_path = self.take_screenshot(f"tx_{tx_hash[:8]}.png")

            # 상태 확인
            try:
                success_element = self.page.locator("text=Success").first
                if success_element.is_visible():
                    status = "Success"
                else:
                    status = "Failed"
            except:
                status = "Unknown"

            print(f"✅ Transaction status: {status}")

            return {
                "tx_hash": tx_hash,
                "status": status,
                "screenshot": screenshot_path,
                "url": url
            }

        except Exception as e:
            print(f"❌ Failed to check transaction: {e}")
            return {
                "tx_hash": tx_hash,
                "status": "Error",
                "error": str(e)
            }


class NFTMarketplaceUploader(WebAutomation):
    """
    NFT 마켓플레이스 자동 업로드
    (Magic Eden, Tensor 등)
    """
    def upload_to_magic_eden(self, nft_data):
        """
        Magic Eden Launchpad에 NFT 업로드

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
            print("🎨 Uploading to Magic Eden...")

            # Magic Eden Launchpad
            self.page.goto("https://magiceden.io/launchpad/create")
            time.sleep(3)

            # 지갑 연결 (Phantom)
            # 주의: 실제로는 Phantom 확장 프로그램 설치 및 자동 승인 필요
            try:
                connect_btn = self.page.locator("button:has-text('Connect Wallet')").first
                if connect_btn.is_visible():
                    connect_btn.click()
                    time.sleep(2)

                    # Phantom 선택
                    phantom_btn = self.page.locator("button:has-text('Phantom')").first
                    phantom_btn.click()
                    time.sleep(5)
            except:
                pass

            # NFT 정보 입력
            self.page.fill("input[name='name']", nft_data['title'])
            self.page.fill("textarea[name='description']", nft_data['description'])

            # 이미지 업로드
            if nft_data.get('image_path'):
                file_input = self.page.locator("input[type='file']").first
                file_input.set_input_files(nft_data['image_path'])
                time.sleep(5)

            # 가격 설정
            self.page.fill("input[name='price']", str(nft_data['price']))

            # Submit
            self.page.click("button:has-text('Create')")
            time.sleep(10)

            # 성공 확인
            mint_url = self.page.url
            self.take_screenshot("magic_eden_upload_success.png")

            print(f"✅ Uploaded to Magic Eden: {mint_url}")

            return {
                "success": True,
                "mint_url": mint_url
            }

        except Exception as e:
            print(f"❌ Magic Eden upload failed: {e}")
            self.take_screenshot("magic_eden_upload_error.png")
            return {
                "success": False,
                "error": str(e)
            }


# 간편 사용 함수들
def post_to_twitter_web(text, image_path=None):
    """
    Twitter 웹에서 직접 포스팅 (간편 함수)
    """
    with TwitterWebPoster(headless=True) as twitter:
        if twitter.login():
            return twitter.post_tweet(text, image_path)
        else:
            return {"success": False, "error": "Login failed"}


def check_solana_tx(tx_hash, network="devnet"):
    """
    Solana 트랜잭션 확인 (간편 함수)
    """
    with SolanaExplorerChecker(headless=True) as checker:
        return checker.check_transaction(tx_hash, network)


if __name__ == "__main__":
    # 테스트
    print("Testing web automation...")

    # Solana 트랜잭션 체크 테스트
    # result = check_solana_tx("test_hash_123", "devnet")
    # print(result)

    print("Web automation module ready!")
