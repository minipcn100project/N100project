# 🛠️ N100 NFT 자동화 - 완벽 설치 가이드

## 📋 목차

1. [사전 준비사항](#사전-준비사항)
2. [단계별 설치](#단계별-설치)
3. [API 키 발급](#api-키-발급)
4. [환경 설정](#환경-설정)
5. [테스트 실행](#테스트-실행)
6. [트러블슈팅](#트러블슈팅)

---

## 사전 준비사항

### ✅ 이미 완료된 것들
- [x] ComfyUI 설치 완료 (C:\StabilityMatrix)
- [x] SD 1.5 모델 다운로드 완료
- [x] LoRA 모델들 다운로드 완료
- [x] 워크플로우 파일들 준비 완료
- [x] ComfyUI CPU 모드 설정 완료

### 📌 새로 준비해야 할 것들

#### 1. Twitter Developer Account
- [ ] Twitter 개발자 계정 생성
- [ ] API 키 발급

#### 2. GitHub Account
- [ ] GitHub 저장소 생성
- [ ] Personal Access Token 발급
- [ ] GitHub Pages 설정

#### 3. Solana Wallet
- [ ] Solana 지갑 생성
- [ ] Devnet SOL 받기 (테스트용)

#### 4. Domain (선택 사항)
- [ ] GitHub Pages 도메인 (username.github.io)

---

## 단계별 설치

### STEP 1: Ollama 설치 (Llama)

#### Windows:
```bash
# 1. Ollama 다운로드
# https://ollama.com/download/windows 접속
# OllamaSetup.exe 다운로드 및 설치

# 2. Llama 3.2 3B 다운로드 (약 2GB)
ollama pull llama3.2:3b

# 3. 설치 확인
ollama run llama3.2:3b "Hello, test message"
```

#### 예상 소요 시간: 10-15분

---

### STEP 2: Python 패키지 설치

```bash
# 프로젝트 폴더로 이동
cd C:\Users\autop\project\nft-automation-project

# 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 패키지 설치
pip install -r requirements.txt
```

#### 예상 소요 시간: 5-10분

---

### STEP 3: Solana CLI 설치

```bash
# Windows PowerShell에서 실행
# https://docs.solana.com/cli/install-solana-cli-tools
sh -c "$(curl -sSfL https://release.solana.com/stable/install)"

# PATH 추가 (환경 변수 설정)
# C:\Users\autop\.local\share\solana\install\active_release\bin

# 설치 확인
solana --version

# Devnet으로 설정 (테스트용)
solana config set --url https://api.devnet.solana.com

# 새 지갑 생성
solana-keygen new --outfile wallet.json

# ⚠️ 중요: 생성된 seed phrase를 안전하게 보관!

# 지갑 주소 확인
solana address

# Devnet SOL 받기 (테스트용 - 무료)
solana airdrop 2

# 잔액 확인
solana balance
```

#### 예상 소요 시간: 15-20분

---

## API 키 발급

### 1️⃣ Twitter API Keys

#### 발급 절차:

1. **Twitter Developer Portal 접속**
   - https://developer.twitter.com/en/portal/dashboard
   - Twitter 계정으로 로그인

2. **Developer Account 신청**
   - "Sign up for Free Account" 클릭
   - 사용 목적: Educational / Hobbyist
   - 프로젝트 설명 작성:
     ```
     I'm building an automated NFT generation bot that:
     - Generates AI art using Stable Diffusion
     - Posts new NFT creations to Twitter
     - Runs on a low-power Intel N100 Mini PC
     ```

3. **Project & App 생성**
   - "Create Project" → 프로젝트 이름 입력
   - "Create App" → 앱 이름 입력

4. **API Keys 발급**
   - App Settings → Keys and Tokens
   - **API Key and Secret** 생성 → 복사 저장
   - **Access Token and Secret** 생성 → 복사 저장
   - **Bearer Token** 복사 저장

5. **App Permissions 설정**
   - User authentication settings → Edit
   - App permissions: **Read and Write**
   - Type of App: Web App
   - Callback URI: http://localhost
   - Website URL: https://github.com/yourusername

#### 필요한 Keys:
```
TWITTER_API_KEY=xxxxxxxxxxx
TWITTER_API_SECRET=xxxxxxxxxxx
TWITTER_ACCESS_TOKEN=xxxxxxxxxxx
TWITTER_ACCESS_SECRET=xxxxxxxxxxx
TWITTER_BEARER_TOKEN=xxxxxxxxxxx
```

#### 예상 소요 시간: 20-30분 (승인 대기 포함)

---

### 2️⃣ GitHub Personal Access Token

#### 발급 절차:

1. **GitHub Settings 접속**
   - https://github.com/settings/tokens
   - Developer settings → Personal access tokens → Tokens (classic)

2. **New token 생성**
   - "Generate new token (classic)" 클릭
   - Note: `NFT Automation Bot`
   - Expiration: No expiration (또는 1년)
   - Scopes 선택:
     - [x] repo (전체)
     - [x] workflow
     - [x] admin:repo_hook

3. **Token 복사**
   - 생성된 토큰을 안전하게 복사 (다시 볼 수 없음!)

#### 필요한 Token:
```
GITHUB_TOKEN=ghp_xxxxxxxxxxx
```

#### 예상 소요 시간: 5분

---

### 3️⃣ GitHub Repository 생성

1. **New Repository**
   - Repository name: `nft-automation-project`
   - Public
   - ✅ Add a README file

2. **GitHub Pages 설정**
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: main → /public
   - Save

3. **Repository URL 확인**
   ```
   GITHUB_REPO=yourusername/nft-automation-project
   DOMAIN=yourusername.github.io/nft-automation-project
   ```

#### 예상 소요 시간: 5분

---

## 환경 설정

### .env 파일 생성

```bash
# .env.example을 .env로 복사
cp .env.example .env
```

### .env 파일 편집

```bash
# Twitter API Keys (위에서 발급받은 키 입력)
TWITTER_API_KEY=your_actual_api_key_here
TWITTER_API_SECRET=your_actual_api_secret_here
TWITTER_ACCESS_TOKEN=your_actual_access_token_here
TWITTER_ACCESS_SECRET=your_actual_access_secret_here
TWITTER_BEARER_TOKEN=your_actual_bearer_token_here
TWITTER_HANDLE=YourTwitterUsername

# Solana Configuration
SOLANA_WALLET_PATH=./wallet.json
SOLANA_RPC_URL=https://api.devnet.solana.com
# Mainnet: https://api.mainnet-beta.solana.com
CANDY_MACHINE_ID=  # 나중에 입력 (선택 사항)

# NFT Configuration
NFT_PRICE_SOL=0.5
NFT_COLLECTION_NAME=N100 Collection
NFT_SYMBOL=N100
NFT_ROYALTY_PERCENT=5

# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=yourusername/nft-automation-project

# Domain
DOMAIN=yourusername.github.io/nft-automation-project

# ComfyUI
COMFYUI_URL=http://localhost:8188

# Schedule
MINT_INTERVAL_HOURS=1
```

---

## 테스트 실행

### 1. ComfyUI 실행 확인

```bash
# ComfyUI가 실행 중인지 확인
curl http://localhost:8188
```

### 2. Ollama 테스트

```bash
ollama run llama3.2:3b "Generate a short NFT title"
```

### 3. 개별 스크립트 테스트

```bash
# 이미지 생성 테스트
cd C:\Users\autop\project\nft-automation-project
python scripts/image_generator.py

# 텍스트 생성 테스트
python scripts/text_generator.py

# 트위터 봇 테스트 (주석 해제 필요)
python scripts/twitter_bot.py
```

### 4. 메인 스크립트 실행

```bash
python main.py
```

프롬프트에서 `y`를 입력하면 즉시 한 번 실행됩니다.

---

## 트러블슈팅

### ❌ ComfyUI 연결 실패

**증상:** `Connection refused to localhost:8188`

**해결:**
```bash
# ComfyUI 실행 확인
# Stability Matrix에서 ComfyUI 실행

# 포트 확인
netstat -ano | findstr :8188
```

### ❌ Ollama 실행 안됨

**증상:** `ollama: command not found`

**해결:**
```bash
# Ollama 재설치
# https://ollama.com/download

# 서비스 시작
ollama serve
```

### ❌ Twitter API 오류

**증상:** `401 Unauthorized`

**해결:**
- API Keys 다시 확인
- App Permissions이 "Read and Write"인지 확인
- Access Token을 Permissions 변경 후 재생성

### ❌ GitHub Push 실패

**증상:** `Authentication failed`

**해결:**
```bash
# Git 인증 설정
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Personal Access Token으로 인증
# .env의 GITHUB_TOKEN 확인
```

### ❌ 이미지 생성 느림

**증상:** 10분 이상 소요

**해결:**
- ComfyUI 워크플로우에서 Steps를 6으로 확인
- LCM LoRA가 적용되었는지 확인
- CPU 사용량 확인 (다른 프로그램 종료)

---

## 🎯 최종 체크리스트

설치가 완료되면 다음을 확인하세요:

- [ ] ComfyUI가 http://localhost:8188 에서 실행 중
- [ ] Ollama로 llama3.2:3b 실행 가능
- [ ] .env 파일에 모든 API 키 입력 완료
- [ ] wallet.json 생성 및 SOL 잔액 확인
- [ ] GitHub Repository 생성 및 Pages 활성화
- [ ] 테스트 이미지 생성 성공
- [ ] 테스트 트윗 포스팅 성공 (선택)

---

## 📞 도움이 필요하신가요?

- GitHub Issues: [프로젝트 이슈](https://github.com/yourusername/nft-automation-project/issues)
- Discord: [커뮤니티 서버](#)

---

**설치 완료! 이제 자동화를 시작하세요! 🚀**
