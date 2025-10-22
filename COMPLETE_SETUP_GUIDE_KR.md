# 🚀 N100 NFT 자동화 프로젝트 - 완벽 설정 가이드

이 가이드는 **처음부터 끝까지 모든 단계**를 상세하게 설명합니다.
각 단계마다 **정확한 링크, 클릭할 버튼, 입력할 값**까지 모두 포함되어 있습니다.

---

## 📋 목차

1. [Twitter Developer 계정 및 API 키 발급](#1-twitter-developer-계정-및-api-키-발급) ✅ **완료**
2. [GitHub Personal Access Token 발급](#2-github-personal-access-token-발급) ✅ **완료**
3. [GitHub Pages 활성화](#3-github-pages-활성화) ✅ **완료**
4. [Solana 지갑 생성](#4-solana-지갑-생성) ⏳ **진행 필요**
5. [Ollama + Llama 3.2 3B 설치](#5-ollama--llama-32-3b-설치) ⏳ **진행 필요**
6. [Python 패키지 설치](#6-python-패키지-설치) ⏳ **진행 필요**
7. [ComfyUI 워크플로우 복사](#7-comfyui-워크플로우-복사) ⏳ **진행 필요**
8. [최종 테스트 실행](#8-최종-테스트-실행) ⏳ **진행 필요**

---

## 1. Twitter Developer 계정 및 API 키 발급

### ✅ 상태: 완료
모든 Twitter API 키가 `.env` 파일에 저장되었습니다.

<details>
<summary>📖 완료된 설정 내용 보기</summary>

### 발급받은 키 목록:
- ✅ API Key: `8LoEQAHKyqzLa5ABchUd0TFOd`
- ✅ API Key Secret: `majBC7Gky7jfKB80BqHj5CqxA1mJU1eDlxkga7li6FEtFULg7C`
- ✅ Bearer Token: `AAAAAAAAAAAAAAAAAAAAABHV4wEAAAAAoEMQCBX0P08GSlkVo5WX6wiE688%3D...`
- ✅ Access Token: `1980854874893139968-QkqV8JqmD9Yek43UX0eK9v4ClPAI5J`
- ✅ Access Token Secret: `YbJHzZFv46KeLEVqMoHZAGgJlUsRyNhFJIUGx4kTIUxOv`

### Twitter 핸들:
- ✅ `@N100project`

</details>

---

## 2. GitHub Personal Access Token 발급

### ✅ 상태: 완료
GitHub Token이 발급되어 `.env` 파일에 저장되었고, 모든 자동화 작업이 완료되었습니다.

### 자동으로 완료된 작업:
- ✅ Git 저장소 초기화
- ✅ 원격 저장소 연결
- ✅ 모든 파일 커밋 및 푸시
- ✅ `gh-pages` 브랜치 생성
- ✅ 랜딩 페이지 배포

### 저장소 정보:
- ✅ Repository: `minipcn100project/N100project`
- ✅ URL: https://github.com/minipcn100project/N100project

---

## 3. GitHub Pages 활성화

### ✅ 상태: 완료 (자동 배포됨)

GitHub Pages가 자동으로 활성화되었습니다. 아래 단계로 확인하세요.

### 📍 확인 방법:

#### 1️⃣ GitHub 저장소 Settings 페이지 열기
👉 **https://github.com/minipcn100project/N100project/settings/pages**

#### 2️⃣ GitHub Pages 설정 확인
페이지를 열면 다음과 같이 표시되어야 합니다:

```
✅ Your site is live at https://minipcn100project.github.io/N100project/
```

**Build and deployment** 섹션:
- **Source**: `Deploy from a branch` 선택됨
- **Branch**: `gh-pages` / `/ (root)` 선택됨
- **Save** 버튼이 비활성화됨 (이미 저장됨)

#### 3️⃣ 웹사이트 접속 테스트
👉 **https://minipcn100project.github.io/N100project/**

위 링크를 클릭하면 **N100 NFT Collection** 랜딩 페이지가 보여야 합니다.

⚠️ **주의:** GitHub Pages는 첫 배포 시 **최대 5-10분** 소요될 수 있습니다.
- 만약 404 에러가 나오면 5분 후 다시 시도하세요.

---

## 4. Solana 지갑 생성

### ⏳ 상태: 진행 필요

Solana 지갑을 생성하여 NFT를 민팅할 수 있도록 설정합니다.

### 📍 단계별 가이드:

#### 1️⃣ Solana CLI 설치 확인

Windows PowerShell을 열고 다음 명령어 실행:

```powershell
solana --version
```

**결과:**
- ✅ 버전이 표시되면 → **2️⃣단계로 이동**
- ❌ 명령을 찾을 수 없다면 → **Solana CLI 설치 필요**

#### 1-a. Solana CLI 설치 (필요한 경우만)

**Windows 설치 방법:**

1. PowerShell을 **관리자 권한**으로 실행
2. 다음 명령어 실행:

```powershell
cmd /c "curl https://release.solana.com/stable/solana-install-init-x86_64-pc-windows-msvc.exe --output C:\solana-install-tmp\solana-install-init.exe --create-dirs"
```

3. 설치 파일 실행:

```powershell
C:\solana-install-tmp\solana-install-init.exe stable
```

4. PowerShell 재시작 후 확인:

```powershell
solana --version
```

#### 2️⃣ Solana 네트워크 설정 (Devnet)

개발용으로 먼저 Devnet에서 테스트합니다:

```powershell
solana config set --url https://api.devnet.solana.com
```

**출력 예시:**
```
Config File: C:\Users\autop\.config\solana\cli\config.yml
RPC URL: https://api.devnet.solana.com
WebSocket URL: wss://api.devnet.solana.com/ (computed)
Keypair Path: C:\Users\autop\.config\solana\id.json
Commitment: confirmed
```

#### 3️⃣ 지갑 생성

프로젝트 폴더에서 지갑 생성:

```powershell
cd C:\Users\autop\project\nft-automation-project
solana-keygen new --outfile wallet.json
```

**중요 프롬프트:**

1. **"Enter passphrase (empty for no passphrase):"**
   - 빈 칸으로 두고 **Enter** 누르기 (자동화를 위해 비밀번호 없이)
   - 또는 비밀번호 입력 (보안 강화, 하지만 자동화 시 매번 입력 필요)

2. **Seed Phrase 저장**
   ```
   pubkey: 7xK3...abcd (예시)
   Save this seed phrase to recover your new keypair:
   apple banana cherry ... (12단어)
   ```

   ⚠️ **매우 중요:**
   - 이 12단어를 **안전한 곳에 반드시 저장**하세요
   - 이 단어를 잃어버리면 지갑을 복구할 수 없습니다
   - 절대로 다른 사람과 공유하지 마세요

#### 4️⃣ 지갑 주소 확인

```powershell
solana address
```

**출력 예시:**
```
7xK3TqW9mZ4vL2Pq8nR6sH5jC9Mx1Fy3Dw7bN8tK5cA9
```

이 주소를 복사해두세요. (NFT 민팅 시 사용)

#### 5️⃣ Devnet SOL 받기 (테스트용 무료)

Devnet에서는 무료로 테스트용 SOL을 받을 수 있습니다:

```powershell
solana airdrop 2
```

**출력 예시:**
```
Requesting airdrop of 2 SOL
Signature: 3Kq...xyz
2 SOL
```

잔액 확인:

```powershell
solana balance
```

**출력 예시:**
```
2 SOL
```

#### 6️⃣ wallet.json 파일 확인

프로젝트 폴더에 `wallet.json` 파일이 생성되었는지 확인:

```powershell
dir wallet.json
```

**파일 내용 예시:**
```json
[123,45,67,89,...]
```

⚠️ **보안 경고:**
- 이 파일은 `.gitignore`에 이미 포함되어 있어 GitHub에 업로드되지 않습니다
- 절대로 이 파일을 공유하거나 공개하지 마세요

#### 7️⃣ (선택) Mainnet으로 전환 (실제 배포 시)

테스트가 완료되고 실제로 NFT를 판매할 준비가 되면:

```powershell
solana config set --url https://api.mainnet-beta.solana.com
```

**실제 SOL 구매:**
- 거래소에서 SOL 구매 (Upbit, Binance 등)
- 위에서 확인한 지갑 주소로 전송
- 민팅 비용 + 가스비로 **최소 0.1 SOL** 권장

---

## 5. Ollama + Llama 3.2 3B 설치

### ⏳ 상태: 진행 필요

Ollama는 로컬에서 AI 텍스트 생성 모델(Llama)을 실행하는 도구입니다.

### 📍 단계별 가이드:

#### 1️⃣ Ollama 다운로드

**공식 웹사이트 접속:**
👉 **https://ollama.com/download**

#### 2️⃣ Windows 버전 설치

1. **"Download for Windows"** 버튼 클릭
2. `OllamaSetup.exe` 파일 다운로드
3. 다운로드한 파일 실행
4. 설치 마법사 따라가기:
   - **Next** 클릭
   - 기본 설치 경로 유지 (`C:\Users\autop\AppData\Local\Programs\Ollama`)
   - **Install** 클릭
   - **Finish** 클릭

#### 3️⃣ Ollama 실행 확인

PowerShell 또는 명령 프롬프트(CMD) 열기:

```powershell
ollama --version
```

**출력 예시:**
```
ollama version is 0.1.17
```

#### 4️⃣ Llama 3.2 3B 모델 다운로드

```powershell
ollama pull llama3.2:3b
```

**출력 예시:**
```
pulling manifest
pulling 6a0746a1ec1a... 100% ████████████████ 1.9 GB
pulling 4fa551d4f938... 100% ████████████████  11 KB
pulling 8ab4849b038c... 100% ████████████████  254 B
pulling 577073ffcc6c... 100% ████████████████  110 B
pulling ad1518640c43... 100% ████████████████  483 B
verifying sha256 digest
writing manifest
removing any unused layers
success
```

⏱️ **소요 시간:** 약 5-10분 (인터넷 속도에 따라)

#### 5️⃣ 모델 테스트

```powershell
ollama run llama3.2:3b "Generate a creative NFT title and description for a futuristic cyberpunk artwork"
```

**출력 예시:**
```
**"NeoTokyo Uprising"**

In the neon-drenched streets of a dystopian metropolis,
a lone hacker emerges from the shadows...
```

모델이 정상적으로 응답하면 설치 완료!

#### 6️⃣ Ollama 백그라운드 실행 확인

Ollama는 설치 후 자동으로 백그라운드에서 실행됩니다.

작업 관리자(Task Manager)에서 확인:
1. `Ctrl + Shift + Esc` 누르기
2. **프로세스** 탭에서 `ollama` 검색
3. `Ollama` 프로세스가 실행 중이어야 함

만약 실행 중이 아니라면:

```powershell
ollama serve
```

이 명령어를 실행하면 백그라운드로 계속 실행됩니다.

---

## 6. Python 패키지 설치

### ⏳ 상태: 진행 필요

프로젝트에 필요한 모든 Python 라이브러리를 설치합니다.

### 📍 단계별 가이드:

#### 1️⃣ Python 설치 확인

PowerShell에서:

```powershell
python --version
```

**출력 예시:**
```
Python 3.11.5
```

✅ Python 3.8 이상이면 OK
❌ 설치되지 않았다면 → https://www.python.org/downloads/ 에서 설치

#### 2️⃣ 프로젝트 폴더로 이동

```powershell
cd C:\Users\autop\project\nft-automation-project
```

#### 3️⃣ 가상 환경 생성 (권장)

```powershell
python -m venv venv
```

가상 환경 활성화:

```powershell
.\venv\Scripts\Activate
```

프롬프트가 `(venv)` 로 시작하면 활성화 완료:
```
(venv) PS C:\Users\autop\project\nft-automation-project>
```

#### 4️⃣ pip 업그레이드

```powershell
python -m pip install --upgrade pip
```

#### 5️⃣ 의존성 패키지 설치

```powershell
pip install -r requirements.txt
```

**출력 예시:**
```
Collecting websocket-client==1.6.4
  Downloading websocket_client-1.6.4-py3-none-any.whl (56 kB)
Collecting requests==2.31.0
  Downloading requests-2.31.0-py3-none-any.whl (62 kB)
...
Successfully installed Pillow-10.1.0 requests-2.31.0 schedule-1.2.0 ...
```

⏱️ **소요 시간:** 약 2-5분

#### 6️⃣ Playwright 브라우저 설치

```powershell
playwright install chromium
```

**출력 예시:**
```
Downloading Chromium 119.0.6045.9 (playwright build v1091)
...
✔ Chromium 119.0.6045.9 downloaded to C:\Users\autop\...
```

⏱️ **소요 시간:** 약 1-3분

#### 7️⃣ 설치 확인

```powershell
pip list
```

**필수 패키지 확인:**
```
Package              Version
-------------------- -------
websocket-client     1.6.4
requests             2.31.0
Pillow               10.1.0
tweepy               4.14.0
solders              0.18.1
solana               0.30.2
schedule             1.2.0
python-dotenv        1.0.0
playwright           1.40.0
```

모두 설치되었으면 완료!

---

## 7. ComfyUI 워크플로우 복사

### ⏳ 상태: 진행 필요

Stability Matrix에서 다운로드한 워크플로우 파일을 프로젝트로 복사합니다.

### 📍 단계별 가이드:

#### 1️⃣ 워크플로우 파일 위치 확인

Stability Matrix의 ComfyUI 워크플로우 폴더:
```
C:\StabilityMatrix\Data\Packages\ComfyUI\user\default\workflows\
```

#### 2️⃣ 다음 4개 파일 확인

파일 탐색기에서 위 경로로 이동하여 다음 파일들이 있는지 확인:

- ✅ `sd15_realistic_lcm.json`
- ✅ `sd15_ghibli_lcm.json`
- ✅ `sd15_pixelart_lcm.json`
- ✅ `sd15_flat2d_anime_lcm.json`

#### 3️⃣ 프로젝트 config 폴더로 복사

PowerShell에서:

```powershell
# config 폴더 생성
mkdir C:\Users\autop\project\nft-automation-project\config\workflows

# 워크플로우 파일 복사
copy "C:\StabilityMatrix\Data\Packages\ComfyUI\user\default\workflows\sd15_*.json" "C:\Users\autop\project\nft-automation-project\config\workflows\"
```

#### 4️⃣ 복사 확인

```powershell
dir C:\Users\autop\project\nft-automation-project\config\workflows\
```

**출력 예시:**
```
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---           10/22/2025  3:45 PM         15234 sd15_flat2d_anime_lcm.json
-a---           10/22/2025  3:45 PM         14876 sd15_ghibli_lcm.json
-a---           10/22/2025  3:45 PM         14234 sd15_pixelart_lcm.json
-a---           10/22/2025  3:45 PM         15012 sd15_realistic_lcm.json
```

4개 파일이 모두 복사되었으면 완료!

#### 5️⃣ .env 파일에서 경로 확인

`.env` 파일을 열어 다음 설정 확인:

```env
COMFYUI_URL=http://localhost:8188
```

ComfyUI가 실행 중이어야 이미지 생성이 가능합니다.

---

## 8. 최종 테스트 실행

### ⏳ 상태: 진행 필요

모든 설정이 완료되었으니 실제로 NFT 자동화 시스템을 테스트합니다.

### 📍 단계별 가이드:

#### 1️⃣ 사전 확인 체크리스트

다음 항목들이 모두 실행 중인지 확인:

- [ ] **ComfyUI 실행 중**
  - Stability Matrix 열기
  - ComfyUI 카드에서 **Launch** 버튼 클릭
  - 브라우저에서 `http://localhost:8188` 접속 확인

- [ ] **Ollama 실행 중**
  - 작업 관리자에서 `ollama` 프로세스 확인
  - 또는 PowerShell에서: `ollama list` 실행

- [ ] **Solana 지갑 준비됨**
  - `wallet.json` 파일이 프로젝트 폴더에 존재
  - Devnet SOL 잔액 확인: `solana balance`

- [ ] **인터넷 연결 정상**
  - Twitter API, GitHub, Solana RPC 접근 필요

#### 2️⃣ 테스트 실행 (단일 NFT 생성)

프로젝트 폴더로 이동:

```powershell
cd C:\Users\autop\project\nft-automation-project
```

가상 환경 활성화 (설정했다면):

```powershell
.\venv\Scripts\Activate
```

**테스트 실행:**

```powershell
python main.py --test
```

#### 3️⃣ 실행 과정 확인

터미널에 다음과 같은 로그가 출력됩니다:

```
🚀 N100 NFT Automation Starting...
📅 Current time: 2025-10-22 15:30:00

=== 🎨 Image Generation ===
🔌 Connecting to ComfyUI at http://localhost:8188
📁 Loading workflow: sd15_realistic_lcm.json
🎲 Generating with random seed: 1234567890
⏳ Waiting for generation...
✅ Image saved: output/nft_001_realistic.png

=== ✍️ Text Generation ===
🦙 Running Llama 3.2 3B...
✅ Generated:
   Title: "Neon Dreams #001"
   Description: "A cyberpunk masterpiece depicting..."

=== 💎 Solana Minting ===
🔗 Connected to Devnet
💰 Wallet balance: 2.0 SOL
📦 Uploading metadata to IPFS...
✅ Metadata URI: ipfs://Qm...abc
⛏️ Creating NFT...
✅ NFT Minted! Signature: 3Kq...xyz
🔗 Explorer: https://solscan.io/tx/3Kq...xyz?cluster=devnet

=== 🐦 Twitter Posting ===
🔑 Using Twitter API
📤 Uploading image...
✅ Tweeted! URL: https://twitter.com/N100project/status/1234567890

=== 🌐 Landing Page Update ===
📄 Updating gallery.json...
📝 Regenerating index.html...
✅ Landing page updated

=== 📂 Git Sync ===
🔄 Syncing to GitHub...
✅ Pushed to main branch
✅ Deployed to GitHub Pages

🎉 NFT #001 Complete!
🔗 View at: https://minipcn100project.github.io/N100project/
```

#### 4️⃣ 결과 확인

각 단계가 성공했는지 확인:

1. **이미지 생성 확인**
   ```powershell
   dir output\
   ```
   → `nft_001_realistic.png` 파일이 있어야 함

2. **Twitter 포스팅 확인**
   👉 https://twitter.com/N100project
   → 최신 트윗에 이미지와 설명이 포스팅되어 있어야 함

3. **GitHub Pages 확인**
   👉 https://minipcn100project.github.io/N100project/
   → 랜딩 페이지에 새 NFT가 표시되어야 함

4. **Solana Explorer 확인**
   터미널에 출력된 Explorer 링크 클릭
   → NFT 민팅 트랜잭션이 확인되어야 함

#### 5️⃣ 자동 스케줄 실행 (1시간마다)

테스트가 성공했다면, 자동 실행 모드로 전환:

```powershell
python main.py
```

**출력 예시:**
```
🚀 N100 NFT Automation Starting...
⏰ Scheduled to run every 1 hour(s)
⏳ Next run at: 2025-10-22 16:30:00

Press Ctrl+C to stop
```

이제 1시간마다 자동으로:
- 새 이미지 생성
- 텍스트 생성
- NFT 민팅
- Twitter 포스팅
- GitHub 업데이트

가 모두 자동으로 실행됩니다!

#### 6️⃣ 백그라운드 실행 (선택)

컴퓨터를 끄지 않고 계속 실행하려면 **Windows Task Scheduler** 사용:

1. **작업 스케줄러** 열기
   - `Win + R` → `taskschd.msc` 입력 → Enter

2. **새 작업 만들기**
   - 우측 패널에서 **"작업 만들기..."** 클릭

3. **일반 탭**
   - 이름: `N100 NFT Automation`
   - "사용자가 로그온할 때만 실행" 선택
   - "가장 높은 수준의 권한으로 실행" 체크

4. **트리거 탭**
   - **새로 만들기** 클릭
   - "시작": **"로그온할 때"** 선택
   - **확인**

5. **동작 탭**
   - **새로 만들기** 클릭
   - "프로그램/스크립트": `C:\Users\autop\project\nft-automation-project\venv\Scripts\python.exe`
   - "인수 추가": `main.py`
   - "시작 위치": `C:\Users\autop\project\nft-automation-project`
   - **확인**

6. **조건 탭**
   - "컴퓨터의 전원이 AC일 때만 작업 시작" **체크 해제**
   - "작업을 실행하려고 할 때 컴퓨터가 절전 모드에서 해제" **체크**

7. **설정 탭**
   - "작업이 실패하면 다시 시작 간격": **1분** 선택
   - "다시 시작 시도 횟수": **3** 입력

8. **확인** 클릭하여 저장

이제 컴퓨터가 켜지면 자동으로 NFT 자동화가 백그라운드에서 실행됩니다!

---

## 🎯 완료 확인

모든 단계를 완료했다면:

- ✅ Twitter에 자동으로 NFT가 포스팅됨
- ✅ GitHub Pages에 NFT 갤러리가 업데이트됨
- ✅ Solana 블록체인에 NFT가 민팅됨
- ✅ 1시간마다 자동으로 새 NFT가 생성됨

---

## ❓ 문제 해결

### ComfyUI 연결 오류
```
ConnectionRefusedError: [Errno 61] Connection refused
```
→ ComfyUI가 실행 중인지 확인 (`http://localhost:8188`)

### Ollama 모델 없음
```
Error: model 'llama3.2:3b' not found
```
→ `ollama pull llama3.2:3b` 다시 실행

### Twitter API 오류
```
Unauthorized: 401
```
→ `.env` 파일의 Twitter 키가 정확한지 확인

### Solana 잔액 부족
```
Error: insufficient funds
```
→ Devnet: `solana airdrop 2` 실행
→ Mainnet: 거래소에서 SOL 전송

### GitHub Push 실패
```
Authentication failed
```
→ `.env` 파일의 `GITHUB_TOKEN`이 정확한지 확인

---

## 📞 추가 도움

더 자세한 정보는 다음 문서를 참조하세요:

- [README.md](./README.md) - 프로젝트 개요
- [SETUP_GUIDE.md](./SETUP_GUIDE.md) - 기본 설정 가이드
- [PLAYWRIGHT_GUIDE.md](./PLAYWRIGHT_GUIDE.md) - 웹 자동화 가이드
- [CHECKLIST.md](./CHECKLIST.md) - 설정 체크리스트

---

**🎉 모든 설정이 완료되었습니다! N100으로 NFT 자동화를 즐기세요!**
