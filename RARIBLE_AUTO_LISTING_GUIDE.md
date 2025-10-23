# 🎨 Rarible 자동 리스팅 가이드

**NFT 민팅 후 자동으로 Rarible (+ OpenSea, LooksRare, X2Y2)에 리스팅하기**

---

## 📋 목차

1. [Rarible이란?](#1-rarible이란)
2. [자동 리스팅의 장점](#2-자동-리스팅의-장점)
3. [Rarible API 키 발급](#3-rarible-api-키-발급)
4. [환경 변수 설정](#4-환경-변수-설정)
5. [자동 리스팅 사용법](#5-자동-리스팅-사용법)
6. [OpenSea 연동 확인](#6-opensea-연동-확인)
7. [문제 해결](#7-문제-해결)

---

## 1. Rarible이란?

### **Rarible Protocol**
- ✅ NFT 마켓플레이스 및 프로토콜
- ✅ **Seaport Protocol 사용** → OpenSea와 호환
- ✅ Polygon, Ethereum, Tezos 등 지원
- ✅ **자동 리스팅 API 제공**

### **핵심 기능**
**Rarible에 리스팅하면 다음 마켓에서 모두 판매됩니다:**
- ✅ **Rarible** - 직접 리스팅
- ✅ **OpenSea** - 5-10분 후 자동 표시
- ✅ **LooksRare** - 자동 표시
- ✅ **X2Y2** - 자동 표시

**⭐ 한 번만 리스팅하면 4개 마켓에서 동시 판매!**

---

## 2. 자동 리스팅의 장점

### **수동 리스팅 (기존)**
1. NFT 민팅
2. OpenSea에서 NFT 찾기 (5-10분 대기)
3. "Sell" 버튼 클릭
4. 가격 입력 ($10 USD)
5. MetaMask 서명
6. **NFT당 2-3분 소요**

### **자동 리스팅 (Rarible)**
1. NFT 민팅
2. **자동으로 Rarible에 리스팅** (5초)
3. **5-10분 후 OpenSea에도 자동 표시**
4. **수동 작업 불필요!**

**⏱️ 시간 절약: 100개 NFT = 200분 → 0분!**

---

## 3. Rarible API 키 발급

### **Step 1: Rarible 개발자 포털 접속**

**공식 문서**: https://docs.rarible.org/

**API 키는 필요 없습니다!** Rarible Protocol은 **지갑 서명만으로 작동**합니다.

### **Step 2: API Key 설정 (선택 사항)**

프로젝트에 이미 API 키가 포함되어 있습니다:
```
RARIBLE_API_KEY=0fcbe561-ef4d-4190-9896-313c9e55e818
```

**이 키로 바로 사용 가능합니다!**

---

## 4. 환경 변수 설정

`.env` 파일에 다음 내용이 있는지 확인:

```env
# Rarible API
RARIBLE_API_KEY=0fcbe561-ef4d-4190-9896-313c9e55e818

# Polygon (민팅용)
POLYGON_RPC_URL=https://polygon-rpc.com/
PRIVATE_KEY=0x여기에_메타마스크_프라이빗_키

# NFT 가격
NFT_PRICE=10

# 스마트 컨트랙트
CONTRACT_ADDRESS=0xf5420c3E42bb575a2c15434278655c837ca3783E
```

---

## 5. 자동 리스팅 사용법

### **5.1 단일 NFT 리스팅**

#### **Python 사용**
```bash
# NFT #1을 $10 USD로 리스팅
python scripts/rarible_lister.py 1

# 사용자 정의 가격으로 리스팅
python scripts/rarible_lister.py 1 15
```

#### **Node.js 사용**
```bash
# NFT #1을 $10 USD로 리스팅
node scripts/rarible_auto_list.js 1

# 사용자 정의 가격으로 리스팅
node scripts/rarible_auto_list.js 1 15
```

### **5.2 배치 리스팅 (여러 NFT 동시)**

```bash
# Python
python scripts/rarible_lister.py 1,2,3,4,5

# Node.js
node scripts/rarible_auto_list.js 1,2,3,4,5
```

### **5.3 모든 NFT 리스팅**

```bash
# Python (nft_counter.txt 기반)
python scripts/rarible_lister.py all

# Node.js
node scripts/rarible_auto_list.js all
```

### **5.4 출력 예시**

```
======================================================================
RARIBLE AUTO-LISTING SCRIPT
======================================================================

[INFO] Wallet: 0xe8345cff87816bb6a657e45cd5ccbb75846c446f
[OK] Rarible SDK initialized

======================================================================
LISTING NFT #1 ON RARIBLE
======================================================================

[INFO] Price: $10 USD
[INFO] Price: 11.1111 MATIC
[INFO] Token ID: 1

[1/3] Preparing sell order...
[2/3] Sending listing transaction...
[3/3] Listing successful!

======================================================================
SUCCESS! NFT LISTED ON MULTIPLE MARKETPLACES
======================================================================

Token ID: 1
Price: $10 USD (11.1111 MATIC)

Marketplace Links:
Rarible:   https://rarible.com/token/polygon/0xf5420c.../1
OpenSea:   https://opensea.io/assets/matic/0xf5420c.../1
LooksRare: https://looksrare.org/collections/0xf5420c.../1

Note: May take 5-10 minutes to appear on OpenSea
======================================================================
```

---

## 6. OpenSea 연동 확인

### **Step 1: Rarible에서 확인 (즉시)**

리스팅 직후 바로 확인 가능:
```
https://rarible.com/token/polygon/0xf5420c3E42bb575a2c15434278655c837ca3783E:1
```

**표시 내용:**
- ✅ "Buy for $10" 버튼 활성화
- ✅ 가격 표시
- ✅ 소유자 정보

### **Step 2: OpenSea에서 확인 (5-10분 후)**

```
https://opensea.io/assets/matic/0xf5420c3E42bb575a2c15434278655c837ca3783E/1
```

**표시 내용:**
- ✅ "Buy now" 버튼 활성화
- ✅ 가격 $10 USD 표시
- ✅ Rarible과 동일한 가격

### **Step 3: LooksRare에서 확인**

```
https://looksrare.org/collections/0xf5420c3E42bb575a2c15434278655c837ca3783E/1
```

**⭐ 모든 마켓에서 동일한 가격으로 판매됩니다!**

---

## 7. 문제 해결

### **7.1 "NFT contract may need to approve Rarible Exchange"**

#### **원인**
스마트 컨트랙트가 Rarible Exchange에 NFT 전송 권한을 부여하지 않음

#### **해결 방법**

1. **Polygonscan에서 수동 Approve:**
   ```
   https://polygonscan.com/address/0xf5420c3E42bb575a2c15434278655c837ca3783E#writeContract
   ```

2. **setApprovalForAll 호출:**
   - operator: `0x00000000000001ad428e4906aE43D8F9852d0dD6` (Rarible Exchange Polygon)
   - approved: `true`

3. **MetaMask 서명**

4. **재시도:**
   ```bash
   python scripts/rarible_lister.py 1
   ```

### **7.2 "This NFT may already be listed"**

#### **원인**
NFT가 이미 리스팅되어 있음

#### **해결 방법**

Rarible에서 확인:
```
https://rarible.com/token/polygon/0xf5420c3E42bb575a2c15434278655c837ca3783E:[TOKEN_ID]
```

이미 "Buy" 버튼이 있으면 정상 리스팅된 것입니다.

### **7.3 "MATIC balance too low"**

#### **원인**
가스비 부족

#### **해결 방법**

MetaMask에 MATIC 추가:
- 최소: 0.1 MATIC
- 권장: 1 MATIC (100개 NFT 리스팅 가능)

### **7.4 "Timeout after 120 seconds"**

#### **원인**
Polygon 네트워크 혼잡

#### **해결 방법**

1. **잠시 대기 후 재시도:**
   ```bash
   python scripts/rarible_lister.py 1
   ```

2. **RPC 변경:**
   `.env` 파일 수정:
   ```env
   POLYGON_RPC_URL=https://polygon-mainnet.g.alchemy.com/v2/YOUR_KEY
   ```

---

## 8. 고급 사용법

### **8.1 민팅 직후 자동 리스팅**

`story_auto_mint.py` 또는 `complete_auto_mint.py` 수정:

```python
# 민팅 코드 끝에 추가
from scripts.rarible_lister import RaribleLister

# NFT 민팅 완료 후
lister = RaribleLister()
lister.list_nft(token_id, price_usd=10)
```

### **8.2 예약 리스팅 (매일 자동)**

**Windows (Task Scheduler)**

1. 작업 스케줄러 열기
2. "작업 만들기" 클릭
3. 트리거: 매일 오전 9시
4. 작업: `python scripts/rarible_lister.py all`

**Linux/macOS (Cron)**

```bash
# Crontab 편집
crontab -e

# 매일 오전 9시 실행
0 9 * * * cd /path/to/project && python scripts/rarible_lister.py all
```

### **8.3 배치 파일 생성 (Windows)**

`list_all_nfts.bat` 생성:

```batch
@echo off
cd C:\Users\autop\project\nft-automation-project
python scripts/rarible_lister.py all
pause
```

더블 클릭만으로 모든 NFT 리스팅!

---

## 9. 비용 및 수수료

### **리스팅 비용**
- ✅ **Rarible 리스팅 수수료**: 무료!
- ⚠️ **가스비 (Polygon)**: NFT당 ~0.001 MATIC ($0.0009)
- ✅ **100개 NFT 리스팅**: ~0.1 MATIC ($0.09)

### **판매 수수료**

| 마켓 | 수수료 | 구매자가 어디서 사든 |
|------|--------|---------------------|
| **Rarible** | 1% | Rarible 수수료 |
| **OpenSea** | 2.5% | OpenSea 수수료 |
| **LooksRare** | 2% | LooksRare 수수료 |

**⭐ 중요:** 수수료는 **구매자가 어느 마켓에서 사느냐**에 따라 결정됩니다.

**예시:**
- Rarible에 리스팅 → 구매자가 OpenSea에서 구매 → OpenSea 수수료 2.5% 부과

---

## 10. 자주 묻는 질문 (FAQ)

### **Q1: Rarible에 리스팅하면 OpenSea에도 보이나요?**
**A**: 네! Rarible과 OpenSea는 Seaport Protocol을 공유하므로 한 곳에 리스팅하면 양쪽 모두에서 판매됩니다.

### **Q2: OpenSea에만 리스팅하고 싶으면?**
**A**: OpenSea는 자동 리스팅 API를 제공하지 않습니다. 수동으로 하거나 Rarible을 사용하세요.

### **Q3: 자동 리스팅 시 가격을 바꿀 수 있나요?**
**A**: 네! 스크립트 실행 시 가격을 지정하면 됩니다:
```bash
python scripts/rarible_lister.py 1 15  # $15 USD로 리스팅
```

### **Q4: 리스팅을 취소할 수 있나요?**
**A**: 네! Rarible 또는 OpenSea에서 "Cancel Listing" 버튼을 클릭하면 됩니다. 가스비가 소량 발생합니다.

### **Q5: 100개 NFT를 한 번에 리스팅하면 시간이 얼마나 걸리나요?**
**A**: 약 5-10분 소요 (NFT당 3-6초). 배치 리스팅 스크립트가 자동으로 처리합니다.

### **Q6: Solana NFT도 Rarible에 리스팅할 수 있나요?**
**A**: 네! Rarible은 Solana도 지원합니다. 단, 이 가이드는 Polygon 기준입니다.

---

## 11. 다음 단계

### **완료된 것:**
- ✅ Rarible SDK 설치
- ✅ 자동 리스팅 스크립트 생성
- ✅ Python 래퍼 생성
- ✅ API 키 설정

### **해야 할 것:**
1. **첫 NFT 테스트 리스팅:**
   ```bash
   python scripts/rarible_lister.py 1
   ```

2. **5-10분 후 OpenSea 확인:**
   ```
   https://opensea.io/assets/matic/0xf5420c3E42bb575a2c15434278655c837ca3783E/1
   ```

3. **모든 NFT 자동 리스팅:**
   ```bash
   python scripts/rarible_lister.py all
   ```

4. **자동화에 통합:** (선택)
   - `story_auto_mint.py`에 자동 리스팅 추가
   - 민팅 → 리스팅 → 랜딩페이지 생성 → 완료!

---

## 12. 주요 링크

### **공식 문서**
- **Rarible Docs**: https://docs.rarible.org/
- **Rarible SDK**: https://github.com/rarible/sdk
- **Seaport Protocol**: https://docs.opensea.io/reference/seaport-overview

### **마켓플레이스**
- **Rarible**: https://rarible.com/
- **OpenSea**: https://opensea.io/
- **LooksRare**: https://looksrare.org/
- **X2Y2**: https://x2y2.io/

### **블록체인 탐색기**
- **PolygonScan**: https://polygonscan.com/
- **Rarible Exchange (Polygon)**: https://polygonscan.com/address/0x00000000000001ad428e4906aE43D8F9852d0dD6

---

## 13. 지원

### **문제 발생 시:**
1. [7. 문제 해결](#7-문제-해결) 확인
2. 로그 확인 (`node` 출력)
3. GitHub Issues: https://github.com/minipcn100project/N100project/issues

### **버그 리포트:**
다음 정보 포함:
- NFT Token ID
- 에러 메시지 전체
- Polygon 지갑 주소 (프라이빗 키 제외!)
- RPC URL

---

**마지막 업데이트**: 2025-10-24
**버전**: 3.0.0 (Rarible 자동 리스팅 추가)

---

**🎨 이제 NFT를 자동으로 리스팅하세요!**

**한 번의 명령으로 Rarible + OpenSea + LooksRare + X2Y2에 동시 리스팅!**
