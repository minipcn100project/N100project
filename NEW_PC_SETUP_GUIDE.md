# 새 컴퓨터 셋업 가이드 - N100 NFT 자동화 프로젝트

이 가이드는 **새 컴퓨터**에서 N100 NFT 자동화 시스템을 처음부터 설정하는 방법입니다.

## 📋 목차

1. [필수 소프트웨어 설치](#1-필수-소프트웨어-설치)
2. [프로젝트 다운로드](#2-프로젝트-다운로드)
3. [Python 패키지 설치](#3-python-패키지-설치)
4. [AI 모델 설치](#4-ai-모델-설치)
5. [API 키 설정](#5-api-키-설정)
6. [테스트 실행](#6-테스트-실행)

---

## 1. 필수 소프트웨어 설치

### 1.1 Python 3.11

**다운로드:**
```
https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
```

**설치:**
- "Add Python to PATH" 체크 ✅
- "Install for all users" 선택
- 설치 완료

**확인:**
```bash
python --version
# Python 3.11.9
```

### 1.2 Git

**다운로드:**
```
https://git-scm.com/download/win
```

**설치:**
- 기본 설정으로 설치
- Git Bash 포함

**확인:**
```bash
git --version
```

### 1.3 Node.js (npm 포함)

**다운로드:**
```
https://nodejs.org/en/download/
```

**설치:**
- LTS 버전 권장
- npm 자동 포함

**확인:**
```bash
node --version
npm --version
```

### 1.4 ComfyUI

**다운로드 (Stability Matrix):**
```
https://github.com/LykosAI/StabilityMatrix/releases
```

**설치:**
1. Stability Matrix 실행
2. ComfyUI 설치 선택
3. CPU 모드로 설정
4. SD 1.5 모델 다운로드

**ComfyUI 실행:**
```bash
# Stability Matrix에서 Launch 클릭
# 또는 직접 실행:
cd C:\StabilityMatrix\Packages\ComfyUI
python main.py --cpu
```

**확인:**
- http://localhost:8188 접속

### 1.5 Ollama (LLM)

**다운로드:**
```
https://ollama.com/download/windows
```

**설치:**
- OllamaSetup.exe 실행
- 자동 설치

**Llama 3.2 3B 모델 다운로드:**
```bash
ollama pull llama3.2:3b
```

**확인:**
```bash
ollama list
# llama3.2:3b 표시되어야 함
```

---

## 2. 프로젝트 다운로드

### 2.1 GitHub에서 클론

```bash
cd C:\Users\autop\project
git clone https://github.com/minipcn100project/N100project.git nft-automation-project
cd nft-automation-project
```

### 2.2 프로젝트 구조 확인

```
nft-automation-project/
├── main.py                 # 메인 실행 파일
├── requirements.txt        # Python 패키지 목록
├── .env.example           # 환경 변수 템플릿
├── scripts/               # 모든 스크립트
│   ├── image_generator.py
│   ├── text_generator.py
│   ├── polygon_free_minter.py
│   └── ...
├── config/workflows/      # ComfyUI 워크플로우
├── output/               # 생성된 NFT
│   ├── images/
│   └── metadata/
└── docs/                 # 문서
```

---

## 3. Python 패키지 설치

### 3.1 필수 패키지 설치

```bash
cd C:\Users\autop\project\nft-automation-project
python -m pip install -r requirements.txt
```

**requirements.txt 내용:**
```
tweepy==4.14.0
requests==2.31.0
python-dotenv==1.0.0
Pillow==10.2.0
playwright==1.40.0
solana==0.30.2
web3==7.13.0
eth-account==0.13.7
```

### 3.2 추가 패키지

```bash
python -m pip install websocket-client
```

---

## 4. AI 모델 설치

### 4.1 Stable Diffusion 1.5 모델

**다운로드 위치:**
```
C:\StabilityMatrix\Models\StableDiffusion\
```

**필요한 모델:**
1. **SD 1.5 Base Model**
   - `v1-5-pruned-emaonly.safetensors`
   - https://huggingface.co/runwayml/stable-diffusion-v1-5

2. **LCM LoRA** (빠른 생성)
   - `lcm-lora-sdv1-5.safetensors`
   - https://huggingface.co/latent-consistency/lcm-lora-sdv1-5

3. **스타일 LoRA들**
   - Pixel Art LoRA
   - Realistic LoRA
   - Ghibli Style LoRA
   - Flat2D Anime LoRA

**설치 위치:**
```
C:\StabilityMatrix\Models\Lora\
```

### 4.2 ComfyUI 워크플로우

프로젝트에 포함된 워크플로우:
- `sd15_pixelart_lcm_api.json` (픽셀아트)
- `sd15_realistic_lcm_api.json` (사실적)
- `sd15_ghibli_lcm_api.json` (지브리)
- `sd15_flat2d_lcm_api.json` (플랫 2D)

**복사:**
```bash
# 이미 프로젝트의 config/workflows/에 포함되어 있음
```

---

## 5. API 키 설정

### 5.1 .env 파일 생성

```bash
cp .env.example .env
```

### 5.2 .env 파일 편집

**C:\Users\autop\project\nft-automation-project\.env**

```env
# Twitter API Keys
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_CLIENT_ID=your_client_id
TWITTER_CLIENT_SECRET=your_client_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
TWITTER_BEARER_TOKEN=your_bearer_token
TWITTER_HANDLE=your_handle

# Polygon Configuration
POLYGON_WALLET_PATH=./polygon_wallet.json
POLYGON_WALLET_ADDRESS=your_wallet_address
POLYGON_NETWORK=polygon
POLYGON_RPC_URL=https://polygon-rpc.com

# GitHub Configuration
GITHUB_TOKEN=your_github_token
GITHUB_REPO=your_username/your_repo

# Domain (GitHub Pages)
DOMAIN=your_username.github.io/your_repo

# ComfyUI
COMFYUI_URL=http://localhost:8188

# NFT Configuration
NFT_PRICE_SOL=0.5
NFT_COLLECTION_NAME=N100 Collection
NFT_SYMBOL=N100
NFT_ROYALTY_PERCENT=5

# Schedule
MINT_INTERVAL_HOURS=1

# thirdweb API
THIRDWEB_CLIENT_ID=your_client_id
THIRDWEB_SECRET_KEY=your_secret_key
```

### 5.3 Polygon 지갑 생성

```bash
python scripts/polygon_wallet_generator.py
```

생성된 `polygon_wallet.json` 파일을 **안전하게 백업**하세요!

### 5.4 API 키 받는 방법

**Twitter API:**
1. https://developer.twitter.com/en/portal/dashboard
2. 앱 생성
3. API Keys 생성

**GitHub Token:**
1. https://github.com/settings/tokens
2. Generate new token
3. repo 권한 선택

**thirdweb:**
1. https://thirdweb.com/dashboard
2. 가입 (무료)
3. API Keys 생성

---

## 6. 테스트 실행

### 6.1 ComfyUI 시작

```bash
# Stability Matrix에서 ComfyUI Launch
# 또는:
cd C:\StabilityMatrix\Packages\ComfyUI
python main.py --cpu
```

http://localhost:8188 확인

### 6.2 Ollama 시작

```bash
# Ollama는 자동 실행됨
ollama list
```

### 6.3 NFT 테스트 생성

```bash
cd C:\Users\autop\project\nft-automation-project
python main.py --test
```

**예상 결과:**
- `output/images/nft_001.png` 생성
- `output/metadata/1.json` 생성
- 콘솔에 생성 로그 표시

### 6.4 GitHub Pages 배포 테스트

```bash
git add .
git commit -m "Test NFT generation"
git push origin main

# gh-pages 브랜치에 배포
git checkout gh-pages
cp output/images/* images/
cp output/metadata/* metadata/
git add images/ metadata/
git commit -m "Deploy NFT assets"
git push origin gh-pages
```

**확인:**
https://your_username.github.io/your_repo/

---

## 7. 자동화 실행

### 7.1 수동 실행

```bash
python main.py
```

### 7.2 자동화 스케줄링 (Windows Task Scheduler)

**작업 만들기:**
1. Task Scheduler 열기
2. Create Basic Task
3. 이름: "N100 NFT Auto Mint"
4. Trigger: Hourly
5. Action: Start a program
   - Program: `C:\Users\autop\AppData\Local\Programs\Python\Python311\python.exe`
   - Arguments: `C:\Users\autop\project\nft-automation-project\main.py`
6. Finish

---

## 8. 문제 해결

### Python이 인식되지 않음

```bash
# PATH에 Python 추가
setx PATH "%PATH%;C:\Users\autop\AppData\Local\Programs\Python\Python311"
```

### ComfyUI 연결 실패

```bash
# ComfyUI가 실행 중인지 확인
# http://localhost:8188 접속 테스트
```

### Ollama 모델 로드 실패

```bash
# 모델 다시 다운로드
ollama pull llama3.2:3b
```

### GitHub 푸시 실패

```bash
# GitHub token 재생성
# .env 파일에 새 토큰 추가
```

---

## 9. 주요 파일 위치

| 항목 | 경로 |
|------|------|
| 프로젝트 루트 | `C:\Users\autop\project\nft-automation-project\` |
| Python | `C:\Users\autop\AppData\Local\Programs\Python\Python311\` |
| ComfyUI | `C:\StabilityMatrix\Packages\ComfyUI\` |
| SD 모델 | `C:\StabilityMatrix\Models\StableDiffusion\` |
| LoRA 모델 | `C:\StabilityMatrix\Models\Lora\` |
| 생성된 NFT | `프로젝트\output\images\` |
| 메타데이터 | `프로젝트\output\metadata\` |

---

## 10. 백업 권장 사항

### 필수 백업 파일:
1. `polygon_wallet.json` ⚠️ **매우 중요!**
2. `.env` (API 키 포함)
3. `output/` 폴더 (생성된 NFT)
4. 전체 프로젝트 폴더

### 백업 방법:
```bash
# GitHub에 자동 백업 (자동화됨)
# 또는 수동 백업:
xcopy C:\Users\autop\project\nft-automation-project D:\Backup\ /E /I /Y
```

---

## 11. 시스템 요구사항

| 항목 | 최소 사양 | 권장 사양 |
|------|----------|----------|
| CPU | Intel N100 | Intel N100 이상 |
| RAM | 8GB | 16GB |
| 저장공간 | 50GB | 100GB SSD |
| 인터넷 | 10Mbps | 100Mbps |
| OS | Windows 10 | Windows 11 |

---

## 12. 완료 체크리스트

- [ ] Python 3.11 설치 완료
- [ ] Git 설치 완료
- [ ] Node.js/npm 설치 완료
- [ ] ComfyUI 설치 및 실행 확인
- [ ] Ollama 설치 및 모델 다운로드
- [ ] 프로젝트 클론 완료
- [ ] Python 패키지 설치 완료
- [ ] .env 파일 설정 완료
- [ ] Polygon 지갑 생성 완료
- [ ] 테스트 NFT 생성 성공
- [ ] GitHub Pages 배포 확인
- [ ] 자동화 스케줄링 설정

---

## 📞 지원

문제가 발생하면:
1. GitHub Issues: https://github.com/minipcn100project/N100project/issues
2. 로그 확인: `logs/` 폴더
3. 가이드 재확인

---

**이 가이드로 새 컴퓨터에서 5-10분 안에 전체 시스템을 복구할 수 있습니다!**

Generated with Claude Code
