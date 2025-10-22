# Python 설치 가이드

Python 설치가 백그라운드에서 완료되지 않았습니다. 수동으로 설치해주세요.

---

## ⚡ 가장 빠른 방법 (2분)

### 1️⃣ 설치 파일 실행

**경로:** `C:\Users\autop\Downloads\python-installer.exe`

**방법 A: 파일 탐색기로**
1. `Windows 키 + E` (파일 탐색기 열기)
2. 주소창에 입력: `C:\Users\autop\Downloads`
3. `python-installer.exe` 더블클릭
4. ✅ **"Add Python to PATH"** 체크박스 클릭 (중요!)
5. **Install Now** 클릭
6. 완료 대기 (2-3분)

**방법 B: PowerShell에서 직접 실행**
```powershell
# 현재 열려있는 PowerShell에서 실행
Start-Process -FilePath "C:\Users\autop\Downloads\python-installer.exe"
```

설치 창이 뜨면:
- ✅ **"Add Python to PATH"** 체크
- **Install Now** 클릭

---

### 2️⃣ 설치 확인

**새 PowerShell 창**을 열고 (현재 창은 닫기):

```powershell
python --version
```

**예상 출력:**
```
Python 3.11.9
```

---

### 3️⃣ 자동 스크립트 실행

Python이 정상 설치되면 다음 명령어 실행:

```powershell
cd C:\Users\autop\project\nft-automation-project
Set-ExecutionPolicy Bypass -Scope Process -Force
.\quick-setup.ps1
```

이 스크립트가 **나머지 모든 것을 자동으로** 설치합니다:
- ✅ pip 업그레이드
- ✅ Python 패키지 15개 (tweepy, solana, playwright 등)
- ✅ Playwright 브라우저
- ✅ Solana CLI
- ✅ Solana 지갑 생성 및 Devnet SOL 받기
- ✅ ComfyUI 워크플로우 복사

**소요 시간:** 약 10-15분 (자동)

---

## 🔧 문제 해결

### python-installer.exe 파일이 없어요

다시 다운로드:
```powershell
curl -L https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe -o C:\Users\autop\Downloads\python-installer.exe
```

### "Add Python to PATH"를 체크 안했어요

**방법 1: Python 재설치**
- 제어판 → 프로그램 제거 → Python 3.11.9 제거
- 다시 설치하면서 "Add Python to PATH" 체크

**방법 2: 수동으로 PATH 추가**
1. Windows 설정
2. 시스템 → 정보 → 고급 시스템 설정
3. 환경 변수
4. 시스템 변수 → Path → 편집
5. 새로 만들기 → `C:\Program Files\Python311` 추가
6. 새로 만들기 → `C:\Program Files\Python311\Scripts` 추가
7. 확인 → PowerShell 재시작

### Python 버전이 3.11이 아니에요

3.11.9 설치 파일 직접 다운로드:
👉 https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe

---

## 🚀 설치 후 다음 단계

### 1. Python 패키지 설치

```powershell
cd C:\Users\autop\project\nft-automation-project
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Playwright 브라우저 설치

```powershell
playwright install chromium
```

### 3. ComfyUI 워크플로우 복사

```powershell
mkdir config\workflows
copy "C:\StabilityMatrix\Data\Packages\ComfyUI\user\default\workflows\sd15_*.json" "config\workflows\"
```

### 4. 테스트 실행

```powershell
# ComfyUI가 실행 중인지 확인
# Stability Matrix → ComfyUI → Launch

# 테스트 실행
python main.py --test
```

---

## 📊 설치 체크리스트

설치가 완료되면 다음을 확인하세요:

```powershell
# Python 확인
python --version                    # Python 3.11.9

# pip 확인
pip --version                       # pip 24.x

# 패키지 확인
pip list | Select-String "tweepy"   # tweepy 4.14.0
pip list | Select-String "solana"   # solana 0.30.2

# Playwright 확인
playwright --version                # Version 1.40.0

# Ollama 확인
C:\Users\autop\AppData\Local\Programs\Ollama\ollama.exe list
# llama3.2:3b 가 보여야 함
```

---

## ✅ 모두 완료되면

```powershell
cd C:\Users\autop\project\nft-automation-project

# 단일 NFT 생성 테스트
python main.py --test

# 자동화 시작 (1시간마다)
python main.py
```

---

**Python만 설치하면 나머지는 quick-setup.ps1이 자동으로 처리합니다!** 🚀
