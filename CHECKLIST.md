# ✅ N100 NFT 자동화 - 준비사항 체크리스트

이 문서는 프로젝트를 시작하기 전에 준비해야 할 모든 것을 정리한 체크리스트입니다.

---

## 📦 1. 소프트웨어 설치

### 이미 완료됨 ✅
- [x] Windows 10/11
- [x] Python 3.11+
- [x] Git
- [x] ComfyUI (Stability Matrix)
- [x] Stable Diffusion 1.5 모델
- [x] LoRA 모델들
- [x] VSCode

### 새로 설치 필요 🔴
- [ ] **Ollama** (Llama 실행 환경)
  - 다운로드: https://ollama.com/download/windows
  - 설치 후: `ollama pull llama3.2:3b`
  - 소요 시간: 15분

- [ ] **Solana CLI**
  - 설치: `sh -c "$(curl -sSfL https://release.solana.com/stable/install)"`
  - 소요 시간: 10분

- [ ] **Python 패키지**
  - 설치: `pip install -r requirements.txt`
  - 소요 시간: 5분

---

## 🔑 2. API 키 발급

### Twitter API Keys (필수)
- [ ] **Twitter Developer Account 생성**
  - URL: https://developer.twitter.com
  - 소요 시간: 20-30분 (승인 대기 포함)

- [ ] **필요한 키 5개 발급:**
  - [ ] API Key
  - [ ] API Secret
  - [ ] Access Token
  - [ ] Access Token Secret
  - [ ] Bearer Token

- [ ] **App Permissions 설정**
  - Read and Write 권한 필수

**상세 가이드:** [SETUP_GUIDE.md](SETUP_GUIDE.md#1️⃣-twitter-api-keys)

---

### GitHub Personal Access Token (필수)
- [ ] **GitHub Token 생성**
  - URL: https://github.com/settings/tokens
  - Scopes: repo, workflow, admin:repo_hook
  - 소요 시간: 5분

- [ ] **Token 안전하게 저장**
  - ⚠️ 한 번만 볼 수 있으니 주의!

**상세 가이드:** [SETUP_GUIDE.md](SETUP_GUIDE.md#2️⃣-github-personal-access-token)

---

## 🏦 3. Solana 지갑 설정

### Devnet (테스트용) - 무료
- [ ] **지갑 생성**
  ```bash
  solana-keygen new --outfile wallet.json
  ```

- [ ] **Seed Phrase 안전하게 보관**
  - ⚠️ 절대 잃어버리지 마세요!

- [ ] **Devnet으로 설정**
  ```bash
  solana config set --url https://api.devnet.solana.com
  ```

- [ ] **테스트 SOL 받기**
  ```bash
  solana airdrop 2
  ```

- [ ] **잔액 확인**
  ```bash
  solana balance
  ```

### Mainnet (실제 운영) - 나중에
- [ ] Mainnet SOL 구매 (~$10 정도면 충분)
- [ ] RPC URL 변경: `https://api.mainnet-beta.solana.com`

**소요 시간:** 15분

---

## 📂 4. GitHub Repository 설정

- [ ] **Repository 생성**
  - Repository name: `nft-automation-project`
  - Visibility: Public

- [ ] **GitHub Pages 활성화**
  - Settings → Pages
  - Source: Deploy from a branch
  - Branch: main → /public
  - Save

- [ ] **Repository URL 메모**
  ```
  https://github.com/yourusername/nft-automation-project
  ```

**소요 시간:** 5분

---

## ⚙️ 5. 환경 변수 설정

- [ ] **.env 파일 생성**
  ```bash
  cp .env.example .env
  ```

- [ ] **모든 값 입력:**

### Twitter (5개)
```bash
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_SECRET=
TWITTER_BEARER_TOKEN=
TWITTER_HANDLE=YourUsername
```

### GitHub (2개)
```bash
GITHUB_TOKEN=
GITHUB_REPO=yourusername/nft-automation-project
```

### Solana (2개)
```bash
SOLANA_WALLET_PATH=./wallet.json
SOLANA_RPC_URL=https://api.devnet.solana.com
```

### Domain (1개)
```bash
DOMAIN=yourusername.github.io/nft-automation-project
```

### NFT Settings (4개)
```bash
NFT_PRICE_SOL=0.5
NFT_COLLECTION_NAME=N100 Collection
NFT_SYMBOL=N100
NFT_ROYALTY_PERCENT=5
```

---

## 🧪 6. 테스트 실행

- [ ] **ComfyUI 실행 확인**
  ```bash
  curl http://localhost:8188
  ```

- [ ] **Ollama 테스트**
  ```bash
  ollama run llama3.2:3b "Hello"
  ```

- [ ] **이미지 생성 테스트**
  ```bash
  python scripts/image_generator.py
  ```

- [ ] **텍스트 생성 테스트**
  ```bash
  python scripts/text_generator.py
  ```

- [ ] **메인 스크립트 테스트**
  ```bash
  python main.py
  # y 입력하여 즉시 실행
  ```

---

## 📋 7. 최종 확인

### 파일 존재 확인
- [ ] `wallet.json` (Solana 지갑)
- [ ] `.env` (환경 변수)
- [ ] `config/workflows/` (워크플로우 4개)
- [ ] `venv/` (가상환경)

### 서비스 실행 확인
- [ ] ComfyUI 실행 중 (localhost:8188)
- [ ] Ollama 실행 가능
- [ ] Git 설정 완료

### API 연결 확인
- [ ] Twitter API 작동
- [ ] GitHub API 작동
- [ ] Solana 지갑 잔액 확인

---

## 🚀 시작 준비 완료!

모든 체크박스에 ✅가 표시되면 다음 명령어로 시작하세요:

```bash
python main.py
```

---

## 📞 도움이 필요하면?

- **설치 가이드:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **README:** [README.md](README.md)
- **트러블슈팅:** [SETUP_GUIDE.md#트러블슈팅](SETUP_GUIDE.md#트러블슈팅)

---

## ⏱️ 예상 총 소요 시간

| 작업 | 소요 시간 |
|------|----------|
| 소프트웨어 설치 | 30분 |
| API 키 발급 | 30-40분 |
| Solana 지갑 설정 | 15분 |
| GitHub 설정 | 10분 |
| 환경 변수 설정 | 10분 |
| 테스트 | 15분 |
| **총합** | **약 2시간** |

---

**준비가 완료되면 자동화가 시작됩니다! 🎉**
