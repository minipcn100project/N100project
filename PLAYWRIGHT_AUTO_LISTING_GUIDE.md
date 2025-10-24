# 🎭 Playwright 브라우저 자동화 가이드

**OpenSea & Rarible 직접 브라우저 조작으로 NFT 자동 리스팅**

---

## 📋 목차

1. [Playwright란?](#1-playwright란)
2. [왜 브라우저 자동화가 필요한가?](#2-왜-브라우저-자동화가-필요한가)
3. [설치 및 설정](#3-설치-및-설정)
4. [OpenSea 자동 리스팅](#4-opensea-자동-리스팅)
5. [Rarible 자동 리스팅](#5-rarible-자동-리스팅)
6. [배치 리스팅](#6-배치-리스팅)
7. [문제 해결](#7-문제-해결)

---

## 1. Playwright란?

### **Microsoft Playwright**
- ✅ 브라우저 자동화 프레임워크
- ✅ Chromium, Firefox, WebKit 지원
- ✅ 실제 브라우저에서 클릭, 입력, 스크롤 자동화
- ✅ MetaMask 지갑 연동 가능

### **주요 기능**
- 🖱️ **마우스 클릭** - 버튼 자동 클릭
- ⌨️ **키보드 입력** - 가격 입력 자동화
- 📸 **스크린샷** - 각 단계 캡처 (디버깅)
- ⏱️ **대기/타이밍** - 페이지 로딩 기다리기
- 🔍 **요소 찾기** - CSS Selector로 버튼/입력란 찾기

---

## 2. 왜 브라우저 자동화가 필요한가?

### **API 방식의 한계**

| 항목 | Rarible SDK (API) | Playwright (브라우저) |
|------|------------------|---------------------|
| 설치 복잡도 | 높음 (Node.js + SDK) | 중간 (Python만) |
| 지갑 연결 | 복잡 (EthereumWallet) | 자동 (MetaMask) |
| 에러 처리 | 어려움 (SDK 에러) | 쉬움 (화면 보임) |
| 디버깅 | 로그만 | 스크린샷 + 브라우저 |
| **성공률** | **중간 (SDK 버전 충돌)** | **높음 (실제 사용자처럼)** |

### **Playwright의 장점**
- ✅ **실제 브라우저 조작** - API 없이 직접 클릭
- ✅ **시각적 확인** - 브라우저 창 보면서 작동
- ✅ **MetaMask 통합** - 자동으로 서명 대기
- ✅ **범용성** - OpenSea, Rarible, LooksRare 모두 가능

---

## 3. 설치 및 설정

### **Step 1: Playwright 설치**

```bash
# Python Playwright 설치
pip install playwright

# Chromium 브라우저 설치
python -m playwright install chromium
```

**설치 확인:**
```bash
python -c "from playwright.sync_api import sync_playwright; print('OK')"
```

**출력:**
```
OK
```

### **Step 2: 스크립트 확인**

프로젝트에 이미 포함된 스크립트:
- ✅ `scripts/opensea_playwright_list.py` - OpenSea 자동 리스팅
- ✅ `scripts/rarible_playwright_list.py` - Rarible 자동 리스팅
- ✅ `scripts/verify_minted_nfts.py` - NFT 민팅 상태 확인

### **Step 3: MetaMask 준비**

브라우저 자동화는 MetaMask 확장 프로그램과 함께 작동합니다:

1. **Chromium 브라우저 열기**
2. **MetaMask 확장 설치** (수동 또는 프로필 사용)
3. **지갑 연결** - Polygon 네트워크
4. **스크립트 실행 시 MetaMask 팝업에서 서명**

---

## 4. OpenSea 자동 리스팅

### **4.1 단일 NFT 리스팅**

```bash
# NFT #1을 $10 USD로 리스팅
python scripts/opensea_playwright_list.py 1

# 사용자 정의 가격
python scripts/opensea_playwright_list.py 1 15
```

### **4.2 실행 과정**

```
[OPENSEA PLAYWRIGHT] Listing NFT #1 at $10 USD...
[1/8] Launching browser...
[2/8] Navigating to: https://opensea.io/assets/matic/0xf5420c.../1
[DEBUG] Screenshot saved: opensea_nft_1_page.png
[INFO] NFT found: Cute Robot #001
[3/8] Looking for Sell button...
[OK] Found Sell button with selector: button:has-text("Sell")
[4/8] Clicking Sell button...
[5/8] Waiting for listing form...
[OK] Found price input: input[name="price"]
[6/8] Entering price: $10 USD...
[7/8] Looking for Complete listing button...
[OK] Found Complete listing button: button:has-text("Complete listing")
[8/8] Clicking Complete listing...

======================================================================
METAMASK SIGNATURE REQUIRED
======================================================================

Please sign the transaction in MetaMask popup window.
Waiting 60 seconds for signature...

======================================================================
LISTING COMPLETE
======================================================================
NFT #1 listed at $10 USD
OpenSea URL: https://opensea.io/assets/matic/0xf5420c.../1

Note: It may take a few minutes for the listing to appear
======================================================================
```

### **4.3 수동 작업 (MetaMask 서명)**

스크립트가 "METAMASK SIGNATURE REQUIRED" 메시지 표시 시:

1. **Chromium 브라우저 창 찾기**
2. **MetaMask 팝업 찾기** (자동으로 열림)
3. **"Sign" 버튼 클릭**
4. **60초 내 완료**

스크립트가 자동으로 계속 진행됩니다.

### **4.4 디버깅 스크린샷**

각 단계마다 스크린샷 저장 위치:
- `screenshots/opensea_nft_1_page.png` - NFT 페이지
- `screenshots/opensea_nft_1_sell_form.png` - 리스팅 폼
- `screenshots/opensea_nft_1_price_entered.png` - 가격 입력 후
- `screenshots/opensea_nft_1_after_sign.png` - 서명 완료 후
- `screenshots/opensea_nft_1_error.png` - 에러 발생 시

---

## 5. Rarible 자동 리스팅

### **5.1 단일 NFT 리스팅**

```bash
# NFT #1을 $10 USD로 리스팅
python scripts/rarible_playwright_list.py 1

# 사용자 정의 가격
python scripts/rarible_playwright_list.py 1 15
```

### **5.2 Rarible의 차이점**

**가격 입력:**
- OpenSea: USD 직접 입력
- Rarible: MATIC 입력 (자동 변환: `$10 / $0.90 = 11.1111 MATIC`)

**서명 횟수:**
- OpenSea: 1번 서명 (리스팅)
- Rarible: 2번 서명 (첫 사용 시)
  1. **Approve Rarible Exchange** - Rarible에 NFT 전송 권한 부여
  2. **Create Sell Order** - 실제 리스팅 생성

### **5.3 실행 과정**

```
[RARIBLE PLAYWRIGHT] Listing NFT #1 at $10 USD...
[1/8] Launching browser...
[2/8] Navigating to: https://rarible.com/token/polygon/0xf5420c.../1
[DEBUG] Screenshot saved: rarible_nft_1_page.png
[INFO] NFT found: Cute Robot #001
[3/8] Looking for Sell button...
[OK] Found Sell button with selector: button:has-text("Put on sale")
[4/8] Clicking Sell button...
[5/8] Waiting for listing form...
[OK] Found price input: input[name="price"]
[6/8] Entering price: $10 USD...
[INFO] Found currency selector, ensuring MATIC selected...
[7/8] Looking for Put on sale button...
[OK] Found Put on sale button: button:has-text("Put on sale")
[8/8] Clicking Put on sale...

======================================================================
METAMASK SIGNATURE REQUIRED
======================================================================

Please sign the transaction in MetaMask popup window.
Rarible may require 2 signatures:
  1. Approve Rarible Exchange (if first time)
  2. Create sell order

Waiting 90 seconds for signature(s)...

======================================================================
LISTING COMPLETE
======================================================================
NFT #1 listed at $10 USD (11.1111 MATIC)
Rarible URL: https://rarible.com/token/polygon/0xf5420c.../1

Note: Listing will appear on Rarible, OpenSea, LooksRare within minutes
======================================================================
```

---

## 6. 배치 리스팅

### **6.1 여러 NFT 동시 리스팅**

```bash
# OpenSea 배치 리스팅
python scripts/opensea_playwright_list.py 1,2,3,4,5

# Rarible 배치 리스팅
python scripts/rarible_playwright_list.py 1,2,3,4,5
```

### **6.2 배치 실행 과정**

```
======================================================================
BATCH LISTING 5 NFTs ON OPENSEA
======================================================================

[OPENSEA PLAYWRIGHT] Listing NFT #1 at $10 USD...
(NFT #1 리스팅 과정...)

[INFO] Waiting 10 seconds before next listing...

[OPENSEA PLAYWRIGHT] Listing NFT #2 at $10 USD...
(NFT #2 리스팅 과정...)

...

======================================================================
BATCH LISTING SUMMARY
======================================================================
Total: 5
Success: 5
Failed: 0
======================================================================
```

### **6.3 주의사항**

**대기 시간:**
- NFT 간 10초 대기 (서버 부하 방지)
- MetaMask 서명: 각 NFT당 60초 대기

**예상 소요 시간:**
- OpenSea: NFT당 약 2분 (서명 포함)
- Rarible: NFT당 약 3분 (2번 서명 가능)
- 10개 NFT: 약 20-30분

---

## 7. 문제 해결

### **7.1 "Could not find Sell button"**

**원인:**
- NFT가 아직 OpenSea/Rarible에 인덱싱되지 않음
- 이미 리스팅되어 있음
- 지갑이 NFT를 소유하지 않음

**해결:**
1. **NFT 민팅 확인:**
   ```bash
   python scripts/verify_minted_nfts.py
   ```

2. **OpenSea 인덱싱 대기 (5-10분)**

3. **수동 확인:**
   - OpenSea: `https://opensea.io/assets/matic/0xf5420c.../[TOKEN_ID]`
   - Rarible: `https://rarible.com/token/polygon/0xf5420c...:[TOKEN_ID]`

### **7.2 "Timeout waiting for form elements"**

**원인:**
페이지 로딩 느림 또는 UI 변경

**해결:**
1. **스크린샷 확인:**
   ```bash
   ls screenshots/
   ```

2. **수동으로 브라우저에서 확인:**
   - 어떤 단계에서 멈췄는지 스크린샷 보기
   - 페이지 구조가 변경되었는지 확인

3. **Selector 업데이트 필요 시:**
   - `scripts/opensea_playwright_list.py` 또는 `rarible_playwright_list.py` 수정
   - CSS Selector를 현재 OpenSea/Rarible UI에 맞게 업데이트

### **7.3 "MetaMask signature timeout"**

**원인:**
60초 (OpenSea) 또는 90초 (Rarible) 내 서명하지 않음

**해결:**
1. **타이밍 늘리기:**
   ```python
   # opensea_playwright_list.py 또는 rarible_playwright_list.py 수정
   time.sleep(60)  # → time.sleep(120)
   ```

2. **수동 완료 후 재시도:**
   - 스크립트는 실패하지만 리스팅은 완료될 수 있음
   - OpenSea/Rarible에서 수동 확인

### **7.4 "NFT not found"**

**원인:**
NFT가 아직 블록체인에 민팅되지 않음

**해결:**
1. **민팅 상태 확인:**
   ```bash
   python scripts/verify_minted_nfts.py
   ```

2. **출력 예시:**
   ```
   ======================================================================
   SUMMARY
   ======================================================================

   Local images: 11
   On-chain minted: 10
   Not minted: 1

   Images NOT minted on-chain: [0]
   [ACTION REQUIRED] These NFTs need to be minted!
   ```

3. **민팅되지 않은 NFT 민팅:**
   ```bash
   # NFT #0 민팅
   python scripts/polygon_mint.py 0
   ```

### **7.5 Chromium 설치 오류**

**증상:**
```
playwright._impl._api_types.Error: Executable doesn't exist
```

**해결:**
```bash
# Chromium 재설치
python -m playwright install chromium --force

# 또는 관리자 권한으로 실행
# (PowerShell을 관리자로 열고)
python -m playwright install chromium
```

---

## 8. 고급 사용법

### **8.1 Headless 모드 (브라우저 숨기기)**

기본값: `headless=False` (브라우저 보임)

```python
# 스크립트 수정 (opensea_playwright_list.py)
lister = OpenSeaPlaywrightLister(headless=True)  # 브라우저 숨김
```

**주의:**
- Headless 모드에서는 MetaMask 서명 불가
- 디버깅 어려움
- 프로덕션에서만 사용 권장

### **8.2 자동 리스팅 스케줄링**

**Windows Task Scheduler:**

1. **작업 스케줄러 열기**
2. **작업 만들기** 클릭
3. **트리거:** 매일 오전 9시
4. **작업:**
   ```
   프로그램: python
   인수: C:\Users\autop\project\nft-automation-project\scripts\opensea_playwright_list.py all
   시작 위치: C:\Users\autop\project\nft-automation-project
   ```

**주의:**
- MetaMask 서명은 여전히 수동 필요
- 알림 설정하여 서명 시간에 PC 앞에 있어야 함

### **8.3 민팅 후 자동 리스팅**

`sequential_dual_mint.py` 수정:

```python
# 민팅 완료 후 추가
from scripts.opensea_playwright_list import OpenSeaPlaywrightLister

# Polygon 민팅 완료 후
polygon_mint_success = mint_on_polygon(nft_id)

if polygon_mint_success:
    # 자동 리스팅
    lister = OpenSeaPlaywrightLister(headless=False)
    lister.list_nft(nft_id, price_usd=10)
```

---

## 9. 현재 프로젝트 상태

### **9.1 NFT 민팅 상태 확인**

```bash
python scripts/verify_minted_nfts.py
```

**출력:**
```
======================================================================
NFT MINTING VERIFICATION
======================================================================

[1/3] Checking local images...
[OK] Found 11 local images: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

[2/3] Checking on-chain NFTs...
[INFO] Connecting to Polygon...
[OK] Connected to Polygon (Block #78081290)
[INFO] Checking tokens 0-10...
  Token #0: Not minted
  Token #1: Minted (Owner: 0xe8345c...)
  Token #2: Minted (Owner: 0xe8345c...)
  ...

======================================================================
SUMMARY
======================================================================

Local images: 11
On-chain minted: 10
Not minted: 1

Images NOT minted on-chain: [0]
[ACTION REQUIRED] These NFTs need to be minted!
```

### **9.2 다음 단계**

1. **NFT #0 민팅** (현재 미완료)
2. **OpenSea에 NFT #1-#10 리스팅**
3. **Rarible에 NFT #1-#10 리스팅**
4. **5-10분 후 OpenSea에서 확인**

---

## 10. 자주 묻는 질문

### **Q1: Playwright와 Rarible SDK 중 어떤 것을 사용해야 하나요?**

**A**: Playwright를 추천합니다.

| 방법 | 장점 | 단점 |
|------|------|------|
| **Playwright** | 시각적 확인, 높은 성공률, 범용성 | MetaMask 수동 서명 필요 |
| **Rarible SDK** | 완전 자동화 가능 | SDK 버전 충돌, 디버깅 어려움 |

### **Q2: MetaMask 서명을 자동화할 수 있나요?**

**A**: 기술적으로 가능하지만 권장하지 않습니다.

- ✅ **가능:** MetaMask 확장 프로그램 자동화 (고급)
- ❌ **위험:** 프라이빗 키 노출 위험
- ⚠️ **대안:** 하드웨어 지갑 (Ledger/Trezor) 사용 권장

### **Q3: 브라우저가 보이지 않게 할 수 있나요?**

**A**: Headless 모드 가능하지만 MetaMask 서명 문제.

```python
lister = OpenSeaPlaywrightLister(headless=True)
```

**주의:**
- MetaMask 팝업 보이지 않음
- 서명 불가 (자동화 필요)

### **Q4: 100개 NFT를 한 번에 리스팅하려면?**

**A**: 배치 스크립트 사용:

```bash
# 1-100번 NFT 리스팅
python scripts/opensea_playwright_list.py $(seq -s, 1 100)
```

**예상 시간:**
- 100개 × 2분 = 약 200분 (3.3시간)
- MetaMask 서명 계속 필요 (자리 비울 수 없음)

### **Q5: 스크린샷이 너무 많이 쌓이면?**

**A**: 주기적으로 정리:

```bash
# 스크린샷 삭제
rm screenshots/*.png

# 또는 7일 이상된 것만 삭제 (Linux/macOS)
find screenshots/ -name "*.png" -mtime +7 -delete
```

---

## 11. 참고 자료

### **공식 문서**
- **Playwright Docs**: https://playwright.dev/python/
- **OpenSea API**: https://docs.opensea.io/
- **Rarible Docs**: https://docs.rarible.org/

### **관련 파일**
- `scripts/opensea_playwright_list.py` - OpenSea 자동화 스크립트
- `scripts/rarible_playwright_list.py` - Rarible 자동화 스크립트
- `scripts/verify_minted_nfts.py` - NFT 상태 확인
- `RARIBLE_AUTO_LISTING_GUIDE.md` - Rarible SDK 가이드 (대안)

---

**마지막 업데이트**: 2025-10-24
**버전**: 1.0.0 (Playwright 자동화 추가)

---

**🎭 Playwright로 NFT를 쉽게 리스팅하세요!**

**브라우저 자동화 + MetaMask = 안전하고 확실한 리스팅!**
