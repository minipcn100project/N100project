# 🎭 Playwright 웹 자동화 가이드

## 📌 개요

Playwright를 사용하면 Twitter API 없이도 웹 브라우저를 통해 직접 트윗을 포스팅할 수 있습니다.

### 언제 사용하나요?
- ✅ Twitter API 승인 대기 중일 때
- ✅ API 키 발급이 어려울 때
- ✅ 웹사이트 UI를 직접 제어하고 싶을 때

---

## 🛠️ 설치 방법

### STEP 1: Python 패키지 설치

```bash
cd C:\Users\autop\project\nft-automation-project

# Playwright 설치
pip install playwright

# 브라우저 드라이버 설치 (약 300MB)
playwright install chromium
```

### STEP 2: 설치 확인

```bash
# Playwright가 제대로 설치되었는지 확인
playwright --version

# 브라우저 테스트
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); browser = p.chromium.launch(); print('✅ OK'); browser.close(); p.stop()"
```

---

## ⚙️ 설정 방법

### .env 파일 수정

```bash
# Twitter Web Automation 활성화
USE_WEB_AUTOMATION=true

# Twitter 로그인 정보 입력
TWITTER_USERNAME=your_twitter_username
TWITTER_PASSWORD=your_twitter_password
```

**⚠️ 중요:**
- Twitter 2단계 인증(2FA)을 **비활성화**해야 자동 로그인 가능
- 비밀번호는 절대 Git에 커밋하지 마세요 (.gitignore에 포함됨)

---

## 🚀 사용 방법

### 옵션 1: 메인 스크립트에서 자동 사용

```bash
# .env에서 USE_WEB_AUTOMATION=true로 설정
python main.py
```

자동으로 Twitter API 대신 Playwright를 사용합니다.

### 옵션 2: 개별 스크립트로 테스트

```python
# test_twitter_web.py
from scripts.web_automation import post_to_twitter_web

result = post_to_twitter_web(
    text="🤖 Test tweet from N100 Mini PC!",
    image_path="output/images/test.png"
)

print(result)
```

---

## 🎯 기능

### 1. Twitter 웹 포스팅
```python
from scripts.web_automation import post_to_twitter_web

# 텍스트만
post_to_twitter_web("Hello from automation!")

# 텍스트 + 이미지
post_to_twitter_web(
    text="Check out my new NFT!",
    image_path="nft_001.png"
)
```

### 2. Solana 트랜잭션 확인
```python
from scripts.web_automation import check_solana_tx

result = check_solana_tx("transaction_hash_here", "devnet")
print(result)
# → 스크린샷 저장: logs/screenshots/tx_xxxxx.png
```

### 3. NFT 마켓플레이스 업로드 (고급)
```python
from scripts.web_automation import NFTMarketplaceUploader

with NFTMarketplaceUploader() as uploader:
    result = uploader.upload_to_magic_eden({
        "title": "My NFT",
        "description": "Description",
        "image_path": "nft.png",
        "price": 0.5
    })
```

---

## 🔧 옵션 설정

### Headless vs 헤드 모드

```python
# 백그라운드 실행 (기본)
from scripts.web_automation import TwitterWebPoster

with TwitterWebPoster(headless=True) as twitter:
    twitter.login()
    twitter.post_tweet("Hello!")

# 브라우저 창 보이기 (디버그용)
with TwitterWebPoster(headless=False) as twitter:
    twitter.login()
    twitter.post_tweet("Hello!")
```

---

## ⚠️ 주의사항

### 장점
- ✅ API 키 불필요
- ✅ 복잡한 웹 작업 가능
- ✅ 실제 사용자처럼 동작

### 단점
- ❌ 느림 (API보다 10-20초 더 소요)
- ❌ Twitter UI 변경 시 수정 필요
- ❌ 2FA 사용 시 자동화 어려움
- ❌ 브라우저 리소스 사용

### 권장 사항
- **개발/테스트:** Playwright 사용 (빠른 시작)
- **프로덕션:** Twitter API 사용 (안정적)

---

## 🐛 트러블슈팅

### 문제 1: playwright install 실패

```bash
# 관리자 권한으로 실행
# PowerShell을 관리자 권한으로 열고:
playwright install chromium --force
```

### 문제 2: Twitter 로그인 실패

**원인:** 2단계 인증 또는 보안 체크

**해결:**
1. Twitter 2FA 비활성화
2. Twitter Security 설정에서 "Less secure app access" 허용
3. headless=False로 설정하여 수동 로그인 확인

```python
# 디버그 모드로 실행
with TwitterWebPoster(headless=False) as twitter:
    twitter.login()
    # 브라우저 창에서 직접 확인 가능
```

### 문제 3: 로그인은 되는데 트윗 실패

**원인:** Twitter UI 선택자 변경

**해결:**
```python
# web_automation.py 수정 필요
# Twitter의 HTML 구조가 변경되었을 수 있음
# 최신 선택자로 업데이트
```

### 문제 4: 브라우저가 너무 느림

**원인:** CPU 성능 또는 네트워크

**해결:**
```python
# 타임아웃 늘리기
self.page.set_default_timeout(60000)  # 60초

# 이미지/CSS 로딩 비활성화 (속도 향상)
context = self.browser.new_context(
    bypass_csp=True,
    ignore_https_errors=True
)
```

---

## 📊 성능 비교

| 방식 | 소요 시간 | 안정성 | API 키 필요 |
|------|----------|--------|------------|
| **Twitter API** | 5-10초 | 높음 | 필요 |
| **Playwright** | 20-30초 | 중간 | 불필요 |

---

## 🎓 고급 사용법

### 여러 계정 관리

```python
# 계정별로 다른 프로필 사용
from playwright.sync_api import sync_playwright

playwright = sync_playwright().start()

# 계정 1
context1 = playwright.chromium.launch_persistent_context(
    "./user-data/account1",
    headless=True
)

# 계정 2
context2 = playwright.chromium.launch_persistent_context(
    "./user-data/account2",
    headless=True
)
```

### 프록시 사용

```python
browser = playwright.chromium.launch(
    proxy={
        "server": "http://proxy.example.com:8080",
        "username": "user",
        "password": "pass"
    }
)
```

### 스크린샷 자동 저장

```python
# 매 단계마다 스크린샷
self.page.screenshot(path=f"debug_{step}.png")
```

---

## 📝 전체 예시

```python
# complete_example.py
import os
from dotenv import load_dotenv
from scripts.web_automation import TwitterWebPoster

load_dotenv()

def main():
    # Twitter 웹 자동화
    with TwitterWebPoster(headless=True) as twitter:
        # 로그인
        if twitter.login():
            print("✅ Logged in")

            # 트윗 포스팅
            result = twitter.post_tweet(
                text="🤖 Automated tweet from N100 Mini PC!\n\n#NFT #AI #Automation",
                image_path="output/images/nft_001.png"
            )

            if result["success"]:
                print("✅ Tweet posted!")
            else:
                print(f"❌ Failed: {result['error']}")
        else:
            print("❌ Login failed")

if __name__ == "__main__":
    main()
```

---

## 🔄 API로 전환하기

나중에 Twitter API를 받으면 쉽게 전환 가능:

```bash
# .env 파일만 수정
USE_WEB_AUTOMATION=false

# Twitter API 키 입력
TWITTER_API_KEY=xxx
TWITTER_API_SECRET=xxx
...
```

코드 수정 없이 자동으로 API로 전환됩니다!

---

## 📞 도움이 필요하면?

- **메인 가이드:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Web Automation 스크립트:** [scripts/web_automation.py](scripts/web_automation.py)

---

**Playwright로 자동화를 시작하세요! 🚀**
