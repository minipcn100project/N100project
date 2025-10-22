# Google Drive VSCode 연동 가이드

VSCode에서 Google Drive와 자동 동기화하는 완전 가이드

## ✅ 완료된 것

- [x] Google Drive VSCode 확장 프로그램 설치 완료
  - Extension ID: `GustavoASC.google-drive-vscode`
  - Version: 1.3.9

---

## 🔧 Google OAuth 인증 설정

### 1단계: Google Cloud Console 설정

1. **Google Cloud Console 접속**
   ```
   https://console.cloud.google.com/
   ```

2. **새 프로젝트 생성**
   - "프로젝트 선택" 클릭
   - "새 프로젝트" 클릭
   - 프로젝트 이름: "N100-NFT-VSCode"
   - 생성 클릭

3. **Google Drive API 활성화**
   - 왼쪽 메뉴 → "API 및 서비스" → "라이브러리"
   - "Google Drive API" 검색
   - "사용 설정" 클릭

4. **OAuth 동의 화면 구성**
   - "API 및 서비스" → "OAuth 동의 화면"
   - 사용자 유형: "외부" 선택
   - 앱 이름: "N100 NFT VSCode"
   - 사용자 지원 이메일: 본인 이메일
   - 범위 추가:
     - `https://www.googleapis.com/auth/drive`
     - `https://www.googleapis.com/auth/drive.file`
   - 저장 후 계속

5. **OAuth 클라이언트 ID 생성**
   - "사용자 인증 정보" → "사용자 인증 정보 만들기"
   - "OAuth 클라이언트 ID" 선택
   - 애플리케이션 유형: "데스크톱 앱"
   - 이름: "VSCode Google Drive"
   - 생성 클릭

6. **Client ID와 Secret 복사**
   - JSON 다운로드 클릭
   - 또는 Client ID와 Client Secret 복사

---

### 2단계: VSCode에서 Google Drive 인증

1. **VSCode에서 명령 팔레트 열기**
   - Windows: `Ctrl + Shift + P`
   - Mac: `Cmd + Shift + P`

2. **"Google Drive: Login" 명령 실행**
   - 명령 팔레트에 "Google Drive: Login" 입력
   - Enter

3. **인증 정보 입력**
   - Client ID 입력
   - Client Secret 입력

4. **Google 로그인**
   - 브라우저가 자동으로 열림
   - Google 계정 선택
   - 권한 허용 클릭
   - "인증이 완료되었습니다" 메시지 확인

5. **VSCode로 돌아가기**
   - 자동으로 연결 완료
   - 왼쪽 사이드바에 Google Drive 아이콘 표시

---

## 📤 프로젝트 Google Drive에 업로드

### 방법 1: VSCode 확장 프로그램 사용

1. **Google Drive 사이드바 열기**
   - 왼쪽 사이드바에서 Google Drive 아이콘 클릭

2. **폴더 생성**
   - "N100-NFT-Backup" 폴더 생성

3. **프로젝트 업로드**
   - 프로젝트 폴더 전체를 드래그 앤 드롭
   - 또는 우클릭 → "Upload to Google Drive"

### 방법 2: 자동 동기화 스크립트

**C:\Users\autop\project\nft-automation-project\sync_to_gdrive.bat 생성:**

```batch
@echo off
echo ======================================================================
echo   Syncing NFT Project to Google Drive
echo ======================================================================

REM Google Drive VSCode 명령 실행
code --command "googleDrive.uploadFolder" "C:\Users\autop\project\nft-automation-project"

echo.
echo Sync complete!
pause
```

**실행:**
```bash
sync_to_gdrive.bat
```

---

## 🔄 자동 백업 설정

### Windows Task Scheduler로 자동 백업

1. **Task Scheduler 열기**
   - Windows 검색 → "작업 스케줄러"

2. **작업 만들기**
   - "작업 만들기" 클릭
   - 이름: "N100 NFT Google Drive Backup"
   - 설명: "매일 자동 백업"

3. **트리거 설정**
   - "트리거" 탭 → "새로 만들기"
   - 매일: 오후 11:00
   - 반복 간격: 6시간 (선택사항)

4. **작업 설정**
   - "작업" 탭 → "새로 만들기"
   - 프로그램: `C:\Users\autop\project\nft-automation-project\sync_to_gdrive.bat`

5. **저장**
   - 확인 클릭

---

## 📊 백업 확인

### Google Drive 웹에서 확인

1. **Google Drive 접속**
   ```
   https://drive.google.com/
   ```

2. **폴더 확인**
   - "N100-NFT-Backup" 폴더 열기
   - 모든 파일이 동기화되었는지 확인

### 파일 목록 확인

**백업되어야 할 주요 파일:**
- `main.py` ⭐
- `requirements.txt`
- `.env` (중요: API 키 포함)
- `polygon_wallet.json` ⚠️ **매우 중요!**
- `scripts/` 폴더 전체
- `config/workflows/` 폴더
- `output/images/` (생성된 NFT)
- `output/metadata/` (메타데이터)
- `NEW_PC_SETUP_GUIDE.md`
- `GOOGLE_DRIVE_SETUP.md`

---

## 🆘 문제 해결

### "인증 실패" 오류

**해결:**
1. Google Cloud Console에서 OAuth 동의 화면 상태 확인
2. Client ID와 Secret 다시 확인
3. VSCode 재시작
4. "Google Drive: Logout" 후 다시 로그인

### "권한 없음" 오류

**해결:**
1. Google Drive API가 활성화되어 있는지 확인
2. OAuth 범위에 다음이 포함되어 있는지 확인:
   - `https://www.googleapis.com/auth/drive`
   - `https://www.googleapis.com/auth/drive.file`

### "업로드 느림" 문제

**해결:**
1. `.gitignore`에 포함된 파일은 제외
2. `node_modules/` 폴더 제외
3. 대용량 파일(>100MB) 별도 업로드

---

## ⚡ 빠른 사용법

### 명령어 모음

**VSCode에서:**
- `Ctrl + Shift + P` → "Google Drive: Login" - 로그인
- `Ctrl + Shift + P` → "Google Drive: Upload File" - 파일 업로드
- `Ctrl + Shift + P` → "Google Drive: Upload Folder" - 폴더 업로드
- `Ctrl + Shift + P` → "Google Drive: Download File" - 파일 다운로드
- `Ctrl + Shift + P` → "Google Drive: Open File" - 파일 열기

**배치 파일:**
```bash
# 수동 백업
sync_to_gdrive.bat

# Google Drive 설정
setup_google_drive.bat
```

---

## 📱 다른 PC에서 복구하는 방법

### 새 PC에서:

1. **VSCode 설치**
2. **Google Drive 확장 프로그램 설치**
   ```bash
   code --install-extension GustavoASC.google-drive-vscode
   ```

3. **Google Drive 로그인**
   - VSCode에서 "Google Drive: Login"
   - 동일한 Google 계정으로 로그인

4. **프로젝트 다운로드**
   - Google Drive 사이드바 열기
   - "N100-NFT-Backup" 폴더 찾기
   - 우클릭 → "Download to Local"
   - 대상: `C:\Users\autop\project\`

5. **NEW_PC_SETUP_GUIDE.md 따라하기**
   - 모든 소프트웨어 설치
   - Python 패키지 설치
   - API 키 설정
   - 완료!

---

## 🔐 보안 주의사항

### ⚠️ 중요 파일 보호

**절대 공개하면 안 되는 파일:**
1. `polygon_wallet.json` - Polygon 지갑 Private Key
2. `.env` - 모든 API 키 포함
3. `wallet.json` - Solana 지갑 (사용 시)

**권장 사항:**
- Google Drive는 개인 계정만 사용
- 2단계 인증 활성화
- 민감한 파일은 암호화 후 업로드 (선택)

### Google Drive 공유 설정

**확인:**
1. Google Drive에서 "N100-NFT-Backup" 폴더 우클릭
2. "공유" 확인
3. "공유 대상" 목록이 **본인만** 있는지 확인
4. "링크가 있는 모든 사용자" 옵션 **비활성화**

---

## ✅ 완료 체크리스트

- [ ] Google Cloud Console 프로젝트 생성
- [ ] Google Drive API 활성화
- [ ] OAuth 클라이언트 ID 생성
- [ ] VSCode Google Drive 확장 설치 ✅ (완료!)
- [ ] VSCode에서 Google 로그인
- [ ] 프로젝트 전체 업로드
- [ ] 자동 백업 스케줄 설정
- [ ] Google Drive 웹에서 확인
- [ ] 보안 설정 확인

---

## 📍 파일 위치

**로컬:**
```
C:\Users\autop\project\nft-automation-project\
```

**Google Drive:**
```
내 드라이브/N100-NFT-Backup/
```

**GitHub (추가 백업):**
```
https://github.com/minipcn100project/N100project
```

---

**이제 3중 백업 시스템이 완성되었습니다!**
1. ✅ 로컬 저장소
2. ✅ GitHub (버전 관리)
3. ✅ Google Drive (클라우드 백업)

Generated with Claude Code
