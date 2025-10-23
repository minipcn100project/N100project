# N100 NFT Automation - Changelog

All notable changes to this project will be documented in this file.

---

## [2.0.0] - 2025-10-24 - 순차 듀얼 체인 민팅

### 🎯 주요 변경사항

#### 새로운 민팅 전략
- **이전**: 교대 민팅 (Polygon → 대기 → Solana → 대기)
- **현재**: 순차 민팅 (Polygon → 즉시 Solana → 대기)

#### 작동 방식
```
3시간마다:
1. Polygon에 NFT #N 민팅 (5분)
2. 바로 이어서 Solana에 NFT #N 민팅 (5분)
3. 3시간 대기
4. 반복 (NFT #N+1)
```

#### 이점
- ✅ 같은 스토리가 양쪽 체인에 동시 존재
- ✅ 컬렉터가 선호하는 체인 선택 가능
- ✅ Day 1, Day 2, Day 3... 순서 유지
- ✅ 크로스체인 컬렉션 완성도

### 📝 컨셉 변경

#### NFT 주제
- **귀여운 로봇 픽셀아트** - 모든 NFT 통일
- **100일 자동화 스토리** - 각 NFT가 하루를 기록
- **짧고 간결한 설명** - 단답형 스토리텔링

#### 예시
- NFT #0: "Day 0: The Idea" - "Got a crazy idea. Can a Mini PC make NFTs?"
- NFT #1: "Day 1: Hardware Arrives" - "Intel N100 unboxed. No GPU. Just hope."
- NFT #2: "Day 2: Installing ComfyUI" - "CPU-only Stable Diffusion. This will be slow."

### 🔧 기술 변경

#### 새 스크립트
- `sequential_dual_mint.py` - 순차 듀얼 민팅
- `story_metadata_generator.py` - 100일 스토리 시스템
- `story_auto_mint.py` - Polygon 스토리 민팅
- `story_auto_mint_solana.py` - Solana 스토리 민팅

#### 카운터 리셋
- Polygon: NFT #0부터 새로 시작
- Solana: NFT #0부터 시작
- 기존 NFT #1-8: 보관 처리

### 🎨 디자인 변경

#### 랜딩페이지
- **회로도 디자인** - 다크 그린/블루 테마
- **모바일 최적화** - 심플하고 반응형
- **이미지 + 스토리** - NFT 이미지와 설명 함께 표시
- **마켓플레이스 링크** - OpenSea, Rarible, Magic Eden, Solanart

#### 메타데이터
- 실험 프로젝트 경고문 추가
- 하드웨어 스펙 명시
- 가격 정보 ($10 USD) 포함

---

## [1.0.0] - 2025-10-23 - 초기 시스템

### 초기 구현
- ComfyUI CPU 전용 이미지 생성
- Ollama Llama 3.2 메타데이터 생성
- Polygon 스마트 컨트랙트 배포
- Pinata IPFS 통합
- 기본 자동화 (3시간 간격)

### 초기 NFT
- NFT #1-8 민팅 (5개 스타일 로테이션)
- OpenSea/Rarible 자동 인덱싱
- 랜딩 페이지 생성

---

## 앞으로의 계획

### 단기 (1주)
- [ ] 모바일 랜딩 페이지 최적화
- [ ] OpenSea 컬렉션 배너/설명 업데이트
- [ ] 트위터 자동 공지 봇
- [ ] Discord 커뮤니티 서버

### 중기 (1개월)
- [ ] 100개 NFT 완성
- [ ] 실시간 대시보드
- [ ] 커뮤니티 투표 시스템
- [ ] 특별 이벤트 NFT

### 장기 (프로젝트 종료 후)
- [ ] 전체 실험 리포트 발행
- [ ] 하드웨어 스트레스 테스트 결과
- [ ] 오픈소스 코드 공개
- [ ] 교육용 튜토리얼 제작

---

## 기술 세부사항

### 시스템 요구사항
- Intel N100 Mini PC (NO GPU!)
- 8 GB RAM
- Python 3.11+
- ComfyUI (CPU mode)
- Ollama (Llama 3.2 1B)

### 성능
- 이미지 생성: ~60초
- 메타데이터: ~10초
- IPFS 업로드: ~10초
- 블록체인 민팅: ~5-10초
- **총**: ~90초 per chain

### 비용
- Polygon: ~$0.04 per NFT
- Solana: ~$0.15 per NFT
- IPFS: 무료 (Pinata)
- 총: **~$0.19 per dual NFT**

---

## 버그 수정

### 2025-10-24
- 유니코드 인코딩 오류 수정 (emoji 제거)
- Web3 주소 체크섬 처리 추가
- Ollama 타임아웃 폴백 개선

### 2025-10-23
- ComfyUI workflow 변환 오류 수정
- Pinata 업로드 retry 로직 추가
- 가스 추정 로직 개선

---

## 알려진 이슈

### 현재
- OpenSea 자동 리스팅 불가 (수동 필요)
- Magic Eden Solana 실제 민팅 미구현 (mock)
- Twitter 봇 연동 미완성

### 해결 예정
- Metaplex 실제 통합
- 자동 리스팅 대안 탐색
- 소셜 미디어 자동화

---

**마지막 업데이트**: 2025-10-24
**버전**: 2.0.0
**상태**: ✅ 운영 중
