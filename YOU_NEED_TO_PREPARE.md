# 🎯 당신이 준비해야 할 것들

## 빠른 요약 (TL;DR)

프로젝트를 시작하려면 다음을 준비하세요:

1. **Twitter Developer Account** + API Keys (5개)
2. **GitHub Account** + Personal Access Token
3. **Solana 지갑** (무료 생성 가능)
4. **Ollama 설치** (Llama 실행용)
5. **환경 변수 설정** (.env 파일)

**예상 소요 시간: 약 2시간**

---

## 📋 상세 준비사항

### 1️⃣ Twitter Developer Account (필수)

#### 왜 필요한가요?
NFT가 생성될 때마다 자동으로 트위터에 포스팅하기 위해 필요합니다.

#### 어떻게 준비하나요?

1. **Twitter Developer Portal 가입**
   - 링크: https://developer.twitter.com
   - 기존 Twitter 계정으로 로그인
   - "Apply for Developer Account" 클릭

2. **신청서 작성**
   - Use case: Educational / Hobbyist
   - 프로젝트 설명 예시:
     ```
     I'm building an automated NFT art generation bot that creates
     AI-generated artwork using Stable Diffusion on a low-power
     Intel N100 Mini PC (without GPU). The bot will:
     - Generate unique AI art every hour
     - Post new NFT creations to Twitter with images
     - Help showcase that powerful AI can run on budget hardware
     ```

3. **API Keys 발급**
   - Project 생성 → App 생성
   - Keys and Tokens 탭에서 발급:
     - ✅ API Key
     - ✅ API Secret
     - ✅ Access Token
     - ✅ Access Token Secret
     - ✅ Bearer Token
   - ⚠️ 모두 안전하게 저장! (다시 볼 수 없음)

4. **App Permissions 설정**
   - Settings → User authentication settings
   - App permissions: **Read and Write** (필수!)

#### 예상 소요 시간
- 승인 대기 없으면: 15분
- 승인 대기 있으면: 1-2일 (드물게)

#### 비용
- **무료** (Elevated Access 사용)

---

### 2️⃣ GitHub Account (필수)

#### 왜 필요한가요?
- 프로젝트 코드 저장
- NFT 이미지 호스팅
- 랜딩페이지 배포 (GitHub Pages)

#### 어떻게 준비하나요?

1. **GitHub 계정 생성** (이미 있다면 생략)
   - 링크: https://github.com/signup

2. **Personal Access Token 발급**
   - Settings → Developer settings → Personal access tokens
   - "Generate new token (classic)" 클릭
   - Scopes 선택:
     - ✅ repo (전체 체크)
     - ✅ workflow
     - ✅ admin:repo_hook
   - Token 복사 및 저장

3. **Repository 생성**
   - "New repository" 클릭
   - Name: `nft-automation-project`
   - Public 선택
   - "Add a README file" 체크

4. **GitHub Pages 활성화**
   - Repository → Settings → Pages
   - Source: Deploy from a branch
   - Branch: main → `/public`
   - Save

#### 예상 소요 시간
- 10분

#### 비용
- **무료**

---

### 3️⃣ Solana 지갑 (필수)

#### 왜 필요한가요?
NFT를 Solana 블록체인에 민팅하기 위해 필요합니다.

#### 어떻게 준비하나요?

**옵션 A: Devnet (테스트용 - 추천)**

```bash
# 1. Solana CLI 설치
sh -c "$(curl -sSfL https://release.solana.com/stable/install)"

# 2. 새 지갑 생성
solana-keygen new --outfile wallet.json

# ⚠️ 중요: 출력된 seed phrase를 안전하게 보관!

# 3. Devnet으로 설정
solana config set --url https://api.devnet.solana.com

# 4. 무료 테스트 SOL 받기
solana airdrop 2

# 5. 잔액 확인
solana balance
```

**옵션 B: Mainnet (실제 운영)**
- Devnet으로 먼저 테스트 후 전환 권장
- Mainnet SOL 필요 (약 $10 정도면 충분)

#### 예상 소요 시간
- 15분

#### 비용
- Devnet: **무료**
- Mainnet: 약 $10 (SOL 구매)

---

### 4️⃣ Ollama + Llama 설치 (필수)

#### 왜 필요한가요?
NFT 제목과 설명을 자동 생성하기 위해 필요합니다.

#### 어떻게 준비하나요?

**Windows:**
```bash
# 1. Ollama 다운로드 및 설치
# https://ollama.com/download/windows
# OllamaSetup.exe 실행

# 2. Llama 3.2 3B 다운로드 (약 2GB)
ollama pull llama3.2:3b

# 3. 테스트
ollama run llama3.2:3b "Hello, how are you?"
```

**Linux/Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b
```

#### 예상 소요 시간
- 15분 (다운로드 속도에 따라)

#### 비용
- **무료** (로컬 실행)

---

### 5️⃣ 환경 변수 설정 (.env)

#### 왜 필요한가요?
모든 API 키와 설정을 안전하게 저장하기 위해 필요합니다.

#### 어떻게 준비하나요?

1. `.env.example`을 `.env`로 복사
2. 모든 값을 입력:

```bash
# Twitter (위에서 발급받은 5개 키)
TWITTER_API_KEY=your_key_here
TWITTER_API_SECRET=your_secret_here
TWITTER_ACCESS_TOKEN=your_token_here
TWITTER_ACCESS_SECRET=your_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
TWITTER_HANDLE=YourUsername

# GitHub
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
GITHUB_REPO=yourusername/nft-automation-project

# Solana
SOLANA_WALLET_PATH=./wallet.json
SOLANA_RPC_URL=https://api.devnet.solana.com

# Domain
DOMAIN=yourusername.github.io/nft-automation-project

# NFT Settings
NFT_PRICE_SOL=0.5
NFT_COLLECTION_NAME=N100 Collection
NFT_SYMBOL=N100
NFT_ROYALTY_PERCENT=5

# ComfyUI (이미 설정됨)
COMFYUI_URL=http://localhost:8188

# Schedule
MINT_INTERVAL_HOURS=1
```

3. ⚠️ **절대 Git에 커밋하지 마세요!** (.gitignore에 포함됨)

---

## 🔒 보안 주의사항

### 절대 공유하면 안 되는 것들:
- ❌ Twitter API Keys
- ❌ GitHub Personal Access Token
- ❌ Solana wallet.json
- ❌ Seed phrase (지갑 복구 키)
- ❌ .env 파일

### 안전하게 보관하세요:
- 📁 Password Manager (1Password, Bitwarden 등)
- 📝 물리적 백업 (종이에 적어 금고에 보관)
- 🔐 암호화된 USB

---

## ✅ 준비 완료 체크리스트

시작하기 전에 다음을 확인하세요:

- [ ] Twitter API Keys 5개 발급 완료
- [ ] Twitter App Permissions = Read and Write
- [ ] GitHub Personal Access Token 발급
- [ ] GitHub Repository 생성 및 Pages 활성화
- [ ] Solana 지갑 생성 (wallet.json)
- [ ] Devnet SOL 잔액 확인 (최소 1 SOL)
- [ ] Ollama 설치 및 llama3.2:3b 다운로드
- [ ] .env 파일 생성 및 모든 값 입력
- [ ] .env 파일이 .gitignore에 포함되어 있는지 확인

---

## 📞 도움이 필요하면?

### 상세 가이드
- **설치 가이드:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **체크리스트:** [CHECKLIST.md](CHECKLIST.md)

### 자주 묻는 질문

**Q: Twitter API 승인이 오래 걸려요**
A: 보통 즉시 승인되지만, 1-2일 걸릴 수 있습니다. 신청서를 자세히 작성하면 빨라집니다.

**Q: Solana 지갑을 잃어버리면?**
A: Seed phrase가 있으면 복구 가능합니다. 반드시 안전하게 백업하세요!

**Q: GitHub Pages가 안 보여요**
A: 첫 배포 후 5-10분 정도 소요될 수 있습니다.

**Q: 비용이 얼마나 드나요?**
A: Devnet 테스트는 완전 무료입니다. Mainnet 운영 시 월 $3-5 정도 (전기료 + 소량의 SOL).

---

## 🚀 다음 단계

모든 준비가 완료되면:

1. [SETUP_GUIDE.md](SETUP_GUIDE.md)를 따라 설치
2. `python main.py` 실행
3. 첫 NFT 생성 및 트위터 포스팅 확인!

---

**준비만 잘하면 나머지는 자동입니다! 🤖**
