# 🤖 N100 NFT 자동화 프로젝트 - 완전 설치 가이드

**새로운 PC에서 처음부터 NFT 자동 발행까지 완벽 가이드**

---

## 📋 목차

1. [시스템 요구사항](#1-시스템-요구사항)
2. [기본 소프트웨어 설치](#2-기본-소프트웨어-설치)
3. [AI 모델 설치 (ComfyUI + Ollama)](#3-ai-모델-설치-comfyui--ollama)
4. [프로젝트 다운로드 및 설정](#4-프로젝트-다운로드-및-설정)
5. [블록체인 지갑 설정](#5-블록체인-지갑-설정)
6. [환경 변수 설정 (.env)](#6-환경-변수-설정-env)
7. [스마트 컨트랙트 배포](#7-스마트-컨트랙트-배포)
8. [자동 발행 시작](#8-자동-발행-시작)
9. [문제 해결](#9-문제-해결)

---

## 1. 시스템 요구사항

### 하드웨어
- **CPU**: Intel N100 (또는 4코어 이상)
- **RAM**: 8GB 이상 (16GB 권장)
- **GPU**: 불필요 (CPU 전용!)
- **저장공간**: 50GB 이상
- **인터넷**: 안정적인 연결

### 운영체제
- **Windows 10/11** (64-bit)
- **Linux** (Ubuntu 20.04+)
- **macOS** (10.15+)

---

## 2. 기본 소프트웨어 설치

### 2.1 Python 3.11 설치

**다운로드**: https://www.python.org/downloads/

#### Windows
1. 위 링크에서 **Python 3.11.x** 다운로드
2. 설치 시 **"Add Python to PATH"** 체크 필수!
3. 설치 완료 후 확인:
```bash
python --version
# 출력: Python 3.11.x
```

#### Linux/macOS
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# macOS (Homebrew)
brew install python@3.11
```

### 2.2 Git 설치

**다운로드**: https://git-scm.com/downloads

#### Windows
1. 설치 파일 다운로드 및 실행
2. 기본 설정으로 진행

#### Linux/macOS
```bash
# Ubuntu/Debian
sudo apt install git

# macOS
brew install git
```

확인:
```bash
git --version
```

### 2.3 Node.js 설치 (선택 사항 - OpenSea SDK용)

**다운로드**: https://nodejs.org/

- **LTS 버전** (18.x 이상) 설치
- 기본 설정으로 진행

확인:
```bash
node --version
npm --version
```

---

## 3. AI 모델 설치 (ComfyUI + Ollama)

### 3.1 ComfyUI 설치 (이미지 생성)

**GitHub**: https://github.com/comfyanonymous/ComfyUI

#### Windows (간편 설치)
1. **Portable 버전 다운로드**: https://github.com/comfyanonymous/ComfyUI/releases
2. `ComfyUI_windows_portable.zip` 압축 해제
3. `run_cpu.bat` 실행 (GPU 없으므로 CPU 모드)
4. 브라우저에서 `http://127.0.0.1:8188` 접속 확인

#### Linux/macOS (수동 설치)
```bash
# ComfyUI 클론
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

# 실행
python main.py --cpu
```

#### Stable Diffusion 모델 다운로드
1. **Stable Diffusion 1.5**: https://huggingface.co/runwayml/stable-diffusion-v1-5
2. `v1-5-pruned.safetensors` 다운로드
3. `ComfyUI/models/checkpoints/` 폴더에 저장

### 3.2 Ollama 설치 (텍스트 생성)

**공식 사이트**: https://ollama.com/download

#### Windows
1. `OllamaSetup.exe` 다운로드 및 설치
2. 설치 완료 후 자동 실행

#### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### macOS
```bash
brew install ollama
```

#### Llama 3.2 1B 모델 다운로드
```bash
ollama pull llama3.2:1b
```

확인:
```bash
ollama list
# 출력: llama3.2:1b
```

---

## 4. 프로젝트 다운로드 및 설정

### 4.1 프로젝트 클론

```bash
# 프로젝트 폴더로 이동
cd C:\Users\autop\project  # Windows
# cd ~/projects  # Linux/macOS

# 프로젝트 클론
git clone https://github.com/minipcn100project/N100project.git
cd N100project
```

### 4.2 Python 가상환경 생성

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 4.3 Python 패키지 설치

```bash
pip install --upgrade pip

# 핵심 패키지
pip install web3==6.11.3
pip install python-dotenv==1.0.0
pip install requests==2.31.0
pip install schedule==1.2.0
pip install websocket-client==1.6.4
pip install pillow==10.1.0

# Solana 지원
pip install solana==0.30.2
pip install solders==0.18.1
pip install base58==2.1.1

# IPFS 업로드
pip install pinatapy-vourhey==0.2.0
```

또는 한 번에:
```bash
pip install -r requirements.txt
```

---

## 5. 블록체인 지갑 설정

### 5.1 Polygon 지갑 (MetaMask)

#### MetaMask 설치
**다운로드**: https://metamask.io/download/

1. Chrome/Firefox/Brave 확장 프로그램 설치
2. 새 지갑 생성 또는 기존 지갑 복구
3. **복구 문구 안전하게 보관!**

#### Polygon 네트워크 추가
1. MetaMask 열기
2. 네트워크 → "네트워크 추가"
3. 다음 정보 입력:

```
네트워크 이름: Polygon Mainnet
RPC URL: https://polygon-rpc.com/
체인 ID: 137
통화 기호: MATIC
블록 탐색기: https://polygonscan.com/
```

#### MATIC 구매 및 전송
**구매처**:
- **Binance**: https://www.binance.com/
- **Coinbase**: https://www.coinbase.com/
- **Upbit** (한국): https://upbit.com/

**필요 금액**: 10 MATIC (약 100 NFT 민팅 가능, $7-10 USD)

1. 거래소에서 MATIC 구매
2. MetaMask 지갑 주소로 출금 (Polygon 네트워크 선택!)
3. 약 1-5분 후 도착 확인

#### Private Key 추출
⚠️ **절대 타인과 공유하지 마세요!**

1. MetaMask → 계정 세부정보
2. "프라이빗 키 내보내기"
3. 비밀번호 입력
4. Private Key 복사 (나중에 `.env` 파일에 사용)

### 5.2 Solana 지갑 (Phantom)

#### Phantom 지갑 설치
**다운로드**: https://phantom.app/download

1. Chrome/Firefox/Brave 확장 프로그램 설치
2. 새 지갑 생성
3. **복구 문구 안전하게 보관!**

#### SOL 구매 및 전송
**구매처**:
- **Binance**: https://www.binance.com/
- **Coinbase**: https://www.coinbase.com/
- **Upbit** (한국): https://upbit.com/

**필요 금액**: 0.5 SOL (약 500 NFT 민팅 가능, $75-100 USD)

1. 거래소에서 SOL 구매
2. Phantom 지갑 주소로 출금
3. 약 1-5분 후 도착 확인

#### Private Key 추출
⚠️ **절대 타인과 공유하지 마세요!**

1. Phantom → 설정 → "프라이빗 키 내보내기"
2. 비밀번호 입력
3. Private Key 복사 (나중에 `.env` 파일에 사용)

---

## 6. 환경 변수 설정 (.env)

### 6.1 .env 파일 생성

프로젝트 루트 폴더에 `.env` 파일 생성:

```bash
# Windows
notepad .env

# Linux/macOS
nano .env
```

### 6.2 .env 파일 내용

다음 내용을 복사하여 **자신의 정보로 수정**:

```env
# ========================================
# POLYGON (EVM) 설정
# ========================================

# Polygon RPC (무료)
POLYGON_RPC_URL=https://polygon-rpc.com/

# MetaMask Private Key (0x 포함)
PRIVATE_KEY=0x여기에_메타마스크_프라이빗_키_입력

# 스마트 컨트랙트 주소 (배포 후 입력)
CONTRACT_ADDRESS=0x여기에_배포된_컨트랙트_주소_입력

# ========================================
# SOLANA 설정
# ========================================

# Solana RPC (무료)
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com

# Phantom Private Key (Base58 형식)
SOLANA_PRIVATE_KEY=여기에_팬텀_프라이빗_키_입력

# ========================================
# IPFS (Pinata) 설정
# ========================================

# Pinata API 키 (https://app.pinata.cloud/developers/api-keys)
PINATA_API_KEY=여기에_Pinata_API_키_입력
PINATA_SECRET_API_KEY=여기에_Pinata_시크릿_키_입력

# ========================================
# ComfyUI 설정
# ========================================

# ComfyUI API 주소
COMFYUI_URL=http://127.0.0.1:8188

# ========================================
# Ollama 설정
# ========================================

# Ollama API 주소
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b

# ========================================
# 프로젝트 설정
# ========================================

# GitHub Pages 도메인 (또는 사용자 정의 도메인)
DOMAIN=minipcn100project.github.io/N100project

# NFT 가격 (USD)
NFT_PRICE=10

# 민팅 간격 (시간)
MINT_INTERVAL=3

# ========================================
# 선택 사항
# ========================================

# Google Drive 백업 (선택)
# GOOGLE_DRIVE_FOLDER_ID=여기에_구글드라이브_폴더ID_입력
```

### 6.3 Pinata API 키 발급

**Pinata 가입**: https://app.pinata.cloud/register

1. 무료 계정 생성 (1GB 무료)
2. Dashboard → API Keys
3. "New Key" 클릭
4. 권한 설정:
   - **pinFileToIPFS**: ✅
   - **pinJSONToIPFS**: ✅
5. Key Name 입력 (예: "N100-NFT-Automation")
6. "Create Key" 클릭
7. **API Key**와 **API Secret** 복사 → `.env` 파일에 입력

---

## 7. 스마트 컨트랙트 배포

### 7.1 컨트랙트 배포 스크립트 실행

```bash
# 가상환경 활성화 확인
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

# 컨트랙트 배포
python deploy_contract.py
```

### 7.2 배포 성공 확인

출력 예시:
```
========================================
DEPLOYING NFT CONTRACT TO POLYGON
========================================
Contract deployed at: 0xf5420c3E42bb575a2c15434278655c837ca3783E
Transaction hash: 0xabc123...
========================================
```

### 7.3 .env 파일 업데이트

배포된 컨트랙트 주소를 `.env` 파일에 입력:
```env
CONTRACT_ADDRESS=0xf5420c3E42bb575a2c15434278655c837ca3783E
```

### 7.4 PolygonScan에서 확인

https://polygonscan.com/address/0xf5420c3E42bb575a2c15434278655c837ca3783E

---

## 8. 자동 발행 시작

### 8.1 테스트 민팅 (1회)

먼저 단일 NFT 민팅 테스트:

#### Polygon 테스트
```bash
python sequential_dual_mint.py --polygon
```

#### Solana 테스트
```bash
python sequential_dual_mint.py --solana
```

#### 듀얼 체인 테스트
```bash
python sequential_dual_mint.py --once
```

### 8.2 자동화 시작 (3시간 간격)

#### ComfyUI 실행 확인
먼저 ComfyUI가 실행 중인지 확인:
```bash
# Windows
cd C:\path\to\ComfyUI
run_cpu.bat

# Linux/macOS
cd /path/to/ComfyUI
python main.py --cpu
```

브라우저에서 http://127.0.0.1:8188 접속 확인

#### Ollama 실행 확인
```bash
ollama serve
```

#### 자동 민팅 시작
```bash
# 새 터미널에서
cd C:\Users\autop\project\N100project
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# 자동 민팅 시작 (Polygon → Solana 순차)
python sequential_dual_mint.py --schedule
```

### 8.3 백그라운드 실행 (선택)

#### Windows (pythonw 사용)
```bash
pythonw sequential_dual_mint.py --schedule
```

#### Linux/macOS (nohup 사용)
```bash
nohup python sequential_dual_mint.py --schedule > automation.log 2>&1 &
```

### 8.4 상태 확인

```bash
# 현재 NFT 개수 확인
python sequential_dual_mint.py --status
```

출력 예시:
```
======================================================================
SEQUENTIAL DUAL-CHAIN STATUS
======================================================================
Polygon NFTs: 5
Solana NFTs:  5
Total:        10
======================================================================
```

### 8.5 중지 방법

#### 포그라운드 실행 시
- `Ctrl + C` 누르기

#### 백그라운드 실행 시 (Windows)
```bash
# Python 프로세스 전체 종료
taskkill /F /IM python.exe /T
taskkill /F /IM pythonw.exe /T
```

#### 백그라운드 실행 시 (Linux/macOS)
```bash
# 프로세스 ID 찾기
ps aux | grep sequential_dual_mint

# 종료 (PID는 위에서 확인한 번호)
kill -9 [PID]
```

---

## 9. 문제 해결

### 9.1 Python 관련

#### "python을 찾을 수 없습니다"
- Python 설치 시 "Add to PATH" 체크 확인
- 재설치 또는 환경 변수 수동 추가

#### "ModuleNotFoundError"
```bash
# 가상환경 활성화 확인
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# 패키지 재설치
pip install -r requirements.txt
```

### 9.2 ComfyUI 관련

#### "ComfyUI에 연결할 수 없습니다"
1. ComfyUI 실행 확인: http://127.0.0.1:8188
2. `.env` 파일의 `COMFYUI_URL` 확인
3. 방화벽 설정 확인

#### "모델을 찾을 수 없습니다"
- `ComfyUI/models/checkpoints/` 폴더에 `v1-5-pruned.safetensors` 확인
- Stable Diffusion 1.5 다운로드: https://huggingface.co/runwayml/stable-diffusion-v1-5

#### "이미지 생성이 너무 느립니다"
- 정상입니다! CPU 모드는 60초 소요
- GPU 없이 작동하므로 느린 것이 정상

### 9.3 Ollama 관련

#### "Ollama에 연결할 수 없습니다"
```bash
# Ollama 서비스 시작
ollama serve

# 모델 확인
ollama list

# 모델 다운로드 (없을 경우)
ollama pull llama3.2:1b
```

### 9.4 블록체인 관련

#### "insufficient funds for gas"
- **Polygon**: MATIC 잔액 확인 (최소 0.1 MATIC 필요)
- **Solana**: SOL 잔액 확인 (최소 0.01 SOL 필요)
- MetaMask/Phantom에서 잔액 확인

#### "nonce too low"
```bash
# MetaMask 리셋: 설정 → 고급 → 계정 재설정
# 또는 10분 기다렸다가 재시도
```

#### "transaction underpriced"
- 가스비 부족
- `.env` 파일에 `GAS_PRICE` 추가:
```env
GAS_PRICE=50  # Gwei
```

### 9.5 IPFS/Pinata 관련

#### "Pinata 업로드 실패"
1. API 키 확인: https://app.pinata.cloud/developers/api-keys
2. `.env` 파일의 `PINATA_API_KEY`, `PINATA_SECRET_API_KEY` 재확인
3. Pinata 무료 한도 확인 (1GB)

#### "IPFS 이미지가 표시되지 않습니다"
- 10-30초 대기 (IPFS 전파 시간)
- Pinata 대시보드에서 업로드 확인: https://app.pinata.cloud/pinmanager

### 9.6 NFT 마켓플레이스 관련

#### "OpenSea에 NFT가 표시되지 않습니다"
- 민팅 후 5-10분 대기 (인덱싱 시간)
- 직접 링크로 확인:
```
https://opensea.io/assets/matic/[CONTRACT_ADDRESS]/[TOKEN_ID]
```
- OpenSea 새로고침: NFT 페이지에서 "Refresh metadata" 클릭

#### "Magic Eden에 NFT가 표시되지 않습니다"
- 민팅 후 10-20분 대기
- Solana Explorer에서 먼저 확인:
```
https://explorer.solana.com/address/[MINT_ADDRESS]
```

### 9.7 자동 민팅 관련

#### "자동 민팅이 멈췄습니다"
1. 로그 확인:
```bash
# 백그라운드 실행 시
cat automation.log  # Linux/macOS
type automation.log  # Windows
```

2. ComfyUI 실행 상태 확인
3. Ollama 실행 상태 확인
4. 인터넷 연결 확인
5. 가스비 잔액 확인

#### "일부 NFT만 민팅됩니다"
- Polygon은 성공했지만 Solana 실패 시:
  - SOL 잔액 확인
  - Solana RPC 상태 확인
  - 로그에서 에러 메시지 확인

---

## 10. 시작 체크리스트

모든 설정이 완료되었는지 확인:

### ✅ 소프트웨어 설치
- [ ] Python 3.11 설치 및 PATH 추가
- [ ] Git 설치
- [ ] ComfyUI 설치 및 실행 확인
- [ ] Ollama 설치 및 Llama 3.2 1B 다운로드
- [ ] Node.js 설치 (선택)

### ✅ 프로젝트 설정
- [ ] 프로젝트 클론 완료
- [ ] Python 가상환경 생성
- [ ] 모든 패키지 설치 (`pip install -r requirements.txt`)

### ✅ 블록체인 설정
- [ ] MetaMask 설치 및 Polygon 네트워크 추가
- [ ] MATIC 구매 및 전송 (10 MATIC)
- [ ] Polygon Private Key 추출
- [ ] Phantom 설치
- [ ] SOL 구매 및 전송 (0.5 SOL)
- [ ] Solana Private Key 추출

### ✅ API 설정
- [ ] Pinata 가입 및 API 키 발급
- [ ] `.env` 파일 생성 및 모든 값 입력

### ✅ 컨트랙트 배포
- [ ] `python deploy_contract.py` 실행
- [ ] 컨트랙트 주소를 `.env`에 입력
- [ ] PolygonScan에서 확인

### ✅ 테스트
- [ ] ComfyUI 실행 중 (http://127.0.0.1:8188)
- [ ] Ollama 실행 중
- [ ] `python sequential_dual_mint.py --once` 성공
- [ ] Polygon NFT #0 민팅 확인
- [ ] Solana NFT #0 민팅 확인

### ✅ 자동화 시작
- [ ] `python sequential_dual_mint.py --schedule` 실행
- [ ] 백그라운드에서 정상 작동 확인
- [ ] 3시간 후 NFT #1 생성 확인

---

## 11. 주요 링크 모음

### 소프트웨어 다운로드
- **Python**: https://www.python.org/downloads/
- **Git**: https://git-scm.com/downloads
- **Node.js**: https://nodejs.org/
- **ComfyUI**: https://github.com/comfyanonymous/ComfyUI
- **Ollama**: https://ollama.com/download

### 블록체인 지갑
- **MetaMask**: https://metamask.io/download/
- **Phantom**: https://phantom.app/download

### API 서비스
- **Pinata (IPFS)**: https://app.pinata.cloud/register
- **Alchemy (RPC)**: https://www.alchemy.com/ (선택)
- **Infura (RPC)**: https://www.infura.io/ (선택)

### 거래소 (암호화폐 구매)
- **Binance**: https://www.binance.com/
- **Coinbase**: https://www.coinbase.com/
- **Upbit** (한국): https://upbit.com/

### NFT 마켓플레이스
- **OpenSea**: https://opensea.io/
- **Rarible**: https://rarible.com/
- **Magic Eden**: https://magiceden.io/
- **Solanart**: https://solanart.io/

### 블록체인 탐색기
- **PolygonScan**: https://polygonscan.com/
- **Solana Explorer**: https://explorer.solana.com/

### AI 모델
- **Stable Diffusion 1.5**: https://huggingface.co/runwayml/stable-diffusion-v1-5
- **Llama Models**: https://ollama.com/library

---

## 12. 자주 묻는 질문 (FAQ)

### Q1: GPU 없이도 작동하나요?
**A**: 네! 이 프로젝트는 Intel N100 같은 저사양 CPU 전용으로 설계되었습니다. 이미지 생성에 60초 정도 걸리지만 완벽히 작동합니다.

### Q2: 비용이 얼마나 드나요?
**A**:
- **하드웨어**: Intel N100 Mini PC (~$150)
- **Polygon**: NFT당 ~$0.04 (10 MATIC = 약 100 NFT)
- **Solana**: NFT당 ~$0.15 (0.5 SOL = 약 500 NFT)
- **IPFS**: 무료 (Pinata 1GB)
- **총계**: 초기 투자 $170, NFT당 $0.19

### Q3: 자동 리스팅이 되나요?
**A**: 아니요. OpenSea와 Magic Eden은 직접 리스팅 API를 제공하지 않습니다. NFT는 자동으로 마켓에 표시되지만, 가격 설정은 수동으로 해야 합니다 (NFT당 30초 소요).

### Q4: 100개 NFT가 언제 완성되나요?
**A**: 3시간 간격으로 듀얼 민팅하므로:
- 하루 8개 NFT (양쪽 체인 합산 16개)
- 100개 NFT = 약 12.5일

### Q5: 중간에 멈춰도 되나요?
**A**: 네! 언제든지 중지했다가 재시작 가능합니다. `nft_counter.txt`와 `nft_counter_solana.txt` 파일이 진행 상황을 기억합니다.

### Q6: 다른 블록체인도 지원하나요?
**A**: 현재는 Polygon과 Solana만 지원합니다. Ethereum 메인넷은 가스비가 너무 비쌉니다 ($10-50 per NFT).

### Q7: NFT 디자인을 바꿀 수 있나요?
**A**: 네! `scripts/story_metadata_generator.py`의 `get_robot_prompt()` 함수를 수정하면 됩니다.

### Q8: 상업적으로 사용해도 되나요?
**A**: 네! 이 프로젝트는 오픈소스입니다. 단, NFT 판매는 본인 책임하에 진행하세요.

---

## 13. 다음 단계

### 설치 완료 후
1. **첫 NFT 민팅**: `python sequential_dual_mint.py --once`
2. **자동화 시작**: `python sequential_dual_mint.py --schedule`
3. **OpenSea 확인**: https://opensea.io/account
4. **Magic Eden 확인**: https://magiceden.io/me/[YOUR_WALLET]

### 수동 리스팅
1. OpenSea에서 NFT 찾기 (5-10분 소요)
2. "Sell" 버튼 클릭
3. 가격 설정: **$10 USD**
4. 서명 (가스비 무료!)

### 커뮤니티
- **Discord**: (준비 중)
- **Twitter**: (준비 중)
- **GitHub Issues**: https://github.com/minipcn100project/N100project/issues

---

## 14. 지원 및 문의

### 문제 발생 시
1. 먼저 [9. 문제 해결](#9-문제-해결) 섹션 확인
2. 로그 파일 확인 (`automation.log`)
3. GitHub Issues에 질문: https://github.com/minipcn100project/N100project/issues

### 버그 리포트
다음 정보 포함:
- 운영체제 (Windows/Linux/macOS)
- Python 버전
- 에러 메시지 전체
- 재현 방법

---

## 15. 면책 조항

⚠️ **중요 공지**

- 이 프로젝트는 **실험적 프로젝트**입니다
- NFT 투자는 위험할 수 있습니다
- 손실에 대한 책임은 본인에게 있습니다
- 프로젝트는 언제든지 종료될 수 있습니다
- 기술적 흥미/교육 목적으로만 사용하세요

---

**마지막 업데이트**: 2025-10-24
**버전**: 2.0.0
**라이선스**: MIT

---

**🚀 이제 준비되었습니다! CPU만으로 NFT 자동 생성을 시작하세요!**

**Built with ❤️ on Intel N100 - Proving CPU-only AI is viable**
