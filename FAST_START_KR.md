# ⚡ 빠른 시작 가이드

모든 설치를 **한 번에 자동으로** 완료하는 방법입니다.

---

## 🚀 단 1개 명령어로 모두 설치하기

### 방법 1: PowerShell 스크립트 실행 (권장)

#### 1️⃣ PowerShell 관리자 권한으로 열기

1. 키보드에서 `Windows 키` 누르기
2. `PowerShell` 입력
3. **Windows PowerShell** 우클릭
4. **"관리자 권한으로 실행"** 클릭

#### 2️⃣ 다음 명령어 복사 & 붙여넣기 & 엔터

```powershell
cd C:\Users\autop\project\nft-automation-project
Set-ExecutionPolicy Bypass -Scope Process -Force
.\quick-setup.ps1
```

#### 3️⃣ 자동으로 설치됩니다!

스크립트가 다음 작업을 **자동으로** 실행합니다:

1. ✅ Ollama 설치
2. ✅ Llama 3.2 3B 모델 다운로드 (5-10분)
3. ✅ Python 설치 (필요시)
4. ✅ Python 패키지 설치
5. ✅ Playwright 브라우저 설치
6. ✅ Solana CLI 설치
7. ✅ Solana 지갑 생성
8. ✅ ComfyUI 워크플로우 복사

**총 소요 시간:** 약 15-20분

---

## 📺 설치 과정 화면

설치하는 동안 다음과 같은 메시지가 표시됩니다:

```
🚀 N100 NFT Automation Quick Setup
=====================================

1️⃣ Checking Ollama...
   📥 Installing Ollama...
   ✅ Ollama installed

2️⃣ Starting Ollama service...
   ✅ Ollama service started

3️⃣ Downloading Llama 3.2 3B model...
   📥 Downloading model (this may take 5-10 minutes)...
   pulling manifest
   pulling 6a0746a1ec1a... 100% ████████████ 1.9 GB
   ✅ Llama 3.2 3B downloaded

4️⃣ Checking Python...
   ✅ Python 3.11.9

5️⃣ Installing Python packages...
   ✅ Python packages installed

6️⃣ Installing Playwright browser...
   ✅ Playwright chromium installed

7️⃣ Installing Solana CLI...
   ✅ Solana CLI installed

8️⃣ Creating Solana wallet...
   🔑 Generating wallet (press Enter for no passphrase)...
   💰 Requesting airdrop...
   ✅ Wallet created with balance: 2 SOL

9️⃣ Copying ComfyUI workflows...
   ✅ Copied 4 workflow files

=====================================
✅ Setup Complete!
=====================================
```

---

## 🧪 설치 완료 후 테스트

### 1️⃣ ComfyUI 실행

1. **Stability Matrix** 열기
2. **ComfyUI** 카드에서 **Launch** 버튼 클릭
3. 브라우저에서 `http://localhost:8188` 열림 확인

### 2️⃣ 테스트 실행

PowerShell에서:

```powershell
cd C:\Users\autop\project\nft-automation-project
python main.py --test
```

### 3️⃣ 결과 확인

다음이 모두 성공하면 완료:

- ✅ 이미지 생성 (ComfyUI)
- ✅ 텍스트 생성 (Llama)
- ✅ Solana 민팅
- ✅ Twitter 포스팅
- ✅ 랜딩 페이지 업데이트
- ✅ GitHub 푸시

### 4️⃣ 자동화 시작 (1시간마다 자동 실행)

```powershell
python main.py
```

**출력:**
```
🚀 N100 NFT Automation Starting...
⏰ Scheduled to run every 1 hour(s)
⏳ Next run at: 2025-10-22 16:30:00

Press Ctrl+C to stop
```

---

## ❓ 문제가 발생하면?

### Python이 설치되지 않았다고 나오면

PowerShell을 **닫고 다시** 관리자 권한으로 열어서 스크립트를 다시 실행하세요.

```powershell
cd C:\Users\autop\project\nft-automation-project
.\quick-setup.ps1
```

### Solana CLI 설치 실패

수동으로 설치:

```powershell
# 7-Zip이 설치되어 있다면 자동으로 설치됨
# 없다면 수동 설치 필요
```

**또는 Scoop으로 설치:**

```powershell
# Scoop 설치
iwr -useb get.scoop.sh | iex

# Solana CLI 설치
scoop install solana
```

### 더 자세한 문제 해결

- [AUTO_SETUP_STATUS.md](./AUTO_SETUP_STATUS.md) - 설정 상태 및 수동 단계
- [COMPLETE_SETUP_GUIDE_KR.md](./COMPLETE_SETUP_GUIDE_KR.md) - 완벽 가이드

---

## 📦 설치 확인 체크리스트

모든 항목이 체크되어야 합니다:

```powershell
# 각 명령어를 PowerShell에서 실행하여 확인
ollama --version        # Ollama 확인
ollama list             # Llama 모델 확인
python --version        # Python 확인
solana --version        # Solana CLI 확인
solana balance          # Solana 지갑 및 잔액 확인
```

**예상 출력:**
```
ollama version is 0.1.17
NAME              ID              SIZE      MODIFIED
llama3.2:3b       6a0746a1ec1a    1.9 GB    2 minutes ago

Python 3.11.9
solana-cli 1.17.0
2 SOL
```

모두 표시되면 설치 완료! 🎉

---

## 🎯 다음 단계

1. ✅ ComfyUI 실행 (Stability Matrix에서 Launch)
2. ✅ 테스트 실행: `python main.py --test`
3. ✅ 성공하면 자동화 시작: `python main.py`
4. ✅ 1시간마다 자동으로 NFT 생성, 민팅, 트위터 포스팅!

---

**🔗 GitHub 저장소:** https://github.com/minipcn100project/N100project

**🌐 랜딩 페이지:** https://minipcn100project.github.io/N100project/ (5-10분 후 접속 가능)
