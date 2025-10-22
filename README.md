# 🤖 N100 NFT Automation Project

**GPU 없는 Intel N100 Mini PC로 완전 자동화된 NFT 생성 및 민팅 시스템**

## 📋 프로젝트 개요

이 프로젝트는 Intel N100 Mini PC (CPU 전용)를 사용하여:
- ✅ AI로 이미지 자동 생성 (ComfyUI + Stable Diffusion 1.5)
- ✅ Llama로 제목/설명 자동 생성
- ✅ Solana 블록체인에 Lazy Minting (구매 시점 민팅)
- ✅ Twitter 자동 포스팅
- ✅ GitHub 자동 동기화
- ✅ 랜딩페이지 자동 업데이트

## 🎨 생성 스타일

- **Realistic**: 사실적인 이미지
- **Studio Ghibli**: 지브리 애니메이션 스타일
- **Pixel Art**: 레트로 픽셀 아트
- **Flat 2D Anime**: 평면 애니메이션

## 🛠️ 기술 스택

### Backend
- Python 3.11+
- ComfyUI (Stable Diffusion 1.5)
- Ollama (Llama 3.2 3B)
- Solana + Metaplex

### Frontend
- HTML/CSS/JavaScript (Vanilla)
- GitHub Pages

### APIs
- Twitter API v2
- GitHub API

## 📂 프로젝트 구조

```
nft-automation-project/
├── main.py                      # 메인 자동화 스크립트
├── requirements.txt             # Python 패키지
├── .env.example                 # 환경 변수 템플릿
├── .gitignore
├── README.md
├── SETUP_GUIDE.md              # 설치 가이드
├── scripts/
│   ├── image_generator.py      # ComfyUI 이미지 생성
│   ├── text_generator.py       # Llama 텍스트 생성
│   ├── solana_minter.py        # NFT 민팅
│   ├── twitter_bot.py          # 트위터 봇
│   ├── landing_page_generator.py
│   └── git_sync.py             # GitHub 동기화
├── config/
│   └── workflows/              # ComfyUI 워크플로우
├── output/
│   ├── images/                 # 생성된 이미지
│   └── metadata/               # NFT 메타데이터
├── public/                     # GitHub Pages
│   ├── index.html
│   ├── gallery.json
│   ├── images/                 # 공개 이미지
│   └── nft/                    # 개별 NFT 페이지
└── logs/                       # 실행 로그
```

## ⚙️ 시스템 요구사항

### 하드웨어
- Intel N100 Mini PC (또는 유사 CPU)
- 8GB RAM 이상 권장
- 50GB 저장공간

### 소프트웨어
- Windows 10/11 또는 Linux
- Python 3.11+
- Git
- ComfyUI (이미 설치됨)
- Ollama

## 🚀 빠른 시작

### 1. 저장소 클론

```bash
cd C:\Users\autop\project
cd nft-automation-project
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. Ollama 설치 및 Llama 다운로드

```bash
# Ollama 설치 (https://ollama.com/download)
ollama pull llama3.2:3b
```

### 4. 환경 변수 설정

```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일 편집 (API 키 입력)
```

### 5. ComfyUI 워크플로우 복사

```bash
# StabilityMatrix에서 워크플로우 복사
mkdir -p config/workflows
# 자동으로 복사됨
```

### 6. 실행

```bash
python main.py
```

## 📖 상세 설정 가이드

자세한 설정 방법은 [SETUP_GUIDE.md](SETUP_GUIDE.md)를 참고하세요.

## 💰 예상 비용

| 항목 | 비용 |
|------|------|
| ComfyUI | 무료 (로컬) |
| Llama | 무료 (로컬) |
| Solana Lazy Minting | ~$0 (구매자 부담) |
| Twitter API | 무료 |
| GitHub Pages | 무료 |
| 전기료 (N100 15W) | ~$3/월 |

**월 운영비: ~$3**

## 📊 성능

| 작업 | 소요 시간 (N100) |
|------|-----------------|
| 이미지 생성 (512x512) | 2-3분 |
| 메타데이터 생성 | 10-30초 |
| 트위터 포스팅 | 5-10초 |
| GitHub 동기화 | 5-10초 |
| **총 소요 시간** | **약 3-5분** |

## 🔐 보안 주의사항

- ⚠️ `.env` 파일을 절대 Git에 커밋하지 마세요
- ⚠️ `wallet.json` (Solana 지갑)을 안전하게 보관하세요
- ⚠️ Twitter API 키를 외부에 노출하지 마세요

## 📝 라이선스

MIT License

## 🤝 기여

Issue와 Pull Request는 언제나 환영합니다!

## 📧 문의

- GitHub Issues: [프로젝트 이슈](https://github.com/your-repo/issues)
- Twitter: [@YourHandle](https://twitter.com/YourHandle)

---

**Made with ❤️ on Intel N100 Mini PC (No GPU!)**
