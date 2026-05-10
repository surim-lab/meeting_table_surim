# Time Table

여러 사람이 모이는 약속 시간을 정할 때 사용하는 간단한 웹앱입니다. 참가자들이 각자 가능한 날짜와 시간을 입력하면, 가장 많은 사람이 가능한 시간 후보 TOP 3를 자동으로 계산해서 보여줍니다. 인원 수에 제한은 없으며, 두세 명부터 수십 명까지 누구나 사용할 수 있습니다.

## 주요 기능

- **모임 이름으로 그룹 분리**: 친구들과 같은 모임 이름(예: `토요일 저녁 약속`)을 공유하면, 그 이름을 입력한 사람들의 일정끼리만 모아서 집계합니다. 다른 모임의 데이터와 섞이지 않습니다.
- **새로고침 후 모임 유지**: 모임 이름이 URL에 함께 저장되어 새로고침해도 같은 모임 데이터를 다시 불러옵니다.
- **10분 단위 시간 선택**: 시작 시간과 종료 시간을 각각 시(時)와 분(分)으로 따로 고를 수 있고, 분은 10분 단위(00, 10, 20, 30, 40, 50)로 세밀하게 설정할 수 있습니다.
- **자동 시간 조정**: 시작 시간을 종료 시간보다 뒤로 바꾸면 종료 시간이 자동으로 뒤로 밀려, 직접 다시 맞출 필요가 없습니다.
- **여러 날짜 한 번에 등록**: 한 번의 등록으로 여러 날짜를 선택해 동일한 시간 범위를 일괄 적용할 수 있습니다.
- **TOP 3 후보 표시**: 가장 많은 사람이 가능한 시간 3개를, 그 시간에 참여 가능한 참가자 이름과 함께 보여줍니다.
- **다크모드 대응**: 시스템 다크모드 환경에서도 글자가 잘 보이도록 색상을 자동 조정합니다.
- **모임별 초기화**: 한 모임만 처음부터 다시 시작할 수 있습니다(다른 모임 데이터는 영향을 받지 않습니다).

## 사용 흐름

1. 화면 좌측에서 **모임 이름**을 입력합니다. 친구들과 동일한 이름을 공유해야 같은 모임으로 묶입니다.
2. 본인 **이름**을 입력합니다.
3. **연도 / 월 / 일**과 **시작 시간(시·분) / 종료 시간(시·분)** 을 선택합니다. 여러 날짜를 한꺼번에 고를 수 있고, 모든 날짜에 같은 시간 범위가 적용됩니다.
4. **등록하기** 버튼을 누르면 화면 우측의 후보 시간 TOP 3가 즉시 갱신됩니다.
5. 새로고침하거나 URL을 공유해도 같은 모임 이름의 데이터가 다시 표시됩니다.
6. 모임 데이터를 비우고 다시 시작하려면 **이 모임 초기화** 버튼을 누릅니다.

## Docker-Compose 실행

```bash
docker-compose up --build
```

백그라운드 실행:

```bash
docker-compose up --build -d
```

백그라운드 실행 시 로그 출력:

```bash
docker-compose logs -f
```

종료:

```bash
docker-compose down
```

데이터까지 삭제하려면 named volume도 함께 지웁니다.

```bash
docker-compose down -v
```

Streamlit은 `http://localhost:8334`, FastAPI는 `http://localhost:8333`에서 실행됩니다.

웹 화면에서 먼저 모임 이름을 입력하세요. 예를 들어 `토요일 저녁 약속`을 입력한 사람들은 같은 모임의 참가자와 후보 시간만 볼 수 있습니다.

## 공개 배포

현재 공개 웹사이트는 Google Cloud VM에서 Docker Compose로 실행하고, DuckDNS와 Caddy를 이용해 HTTPS로 노출합니다.

- 공개 주소: `https://***.duckdns.org`
- DuckDNS: `***.duckdns.org`가 Google Cloud VM의 외부 IP를 가리키도록 갱신합니다.
- Caddy: `80`, `443` 포트를 받아 Streamlit 프론트엔드 컨테이너(`frontend:8501`)로 reverse proxy합니다.
- HTTPS 인증서: Caddy가 Let's Encrypt 인증서를 자동 발급하고 갱신합니다.
- 백엔드: 외부에 직접 공개하지 않고, 프론트엔드 컨테이너가 Docker 내부 네트워크에서 `http://backend:8000`으로 호출합니다.
- 데이터베이스: SQLite 파일은 `timetable_data` named volume의 `/app/data/time_table.db`에 저장됩니다.


HTTPS 배포가 정상 동작하면 외부 방화벽에서는 `80`, `443`, 관리용 `22`만 열어두고, 초기 테스트용 포트인 `8334`는 닫는 것을 권장합니다. DuckDNS 토큰과 DB 백업 파일은 git에 올리지 않습니다.

## 로컬 실행

백엔드:

```bash
pip install -r requirements.back.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8333
```

프론트엔드:

```powershell
pip install -r requirements.frontend.txt
$env:API_BASE_URL = "http://localhost:8333"
streamlit run frontend/main.py --server.port 8334
```

Docker Compose와 동일하게 맞추려면 Streamlit은 `http://localhost:8334`, FastAPI는 `http://localhost:8333`에서 실행합니다.
Docker 컨테이너 내부에서는 FastAPI가 `8000`, Streamlit이 `8501` 포트를 사용하고, `docker-compose.yml`에서 각각 호스트의 `8333`, `8334`로 연결합니다.

## 구성

### 파일 구조

백엔드:

```text
backend/
├── main.py                 # FastAPI 앱 생성, CORS 설정, 라우터 등록
├── config.py               # 데이터베이스 경로와 기본 설정값
├── database.py             # SQLite 연결, 초기화, 테이블 스키마 생성
├── domain.py               # 모임 이름 정규화, 모임 key 생성 규칙
├── schemas.py              # Pydantic 요청·응답 스키마
├── routers/
│   ├── health.py           # 헬스 체크 API
│   ├── meetings.py         # 모임 생성·조회 API
│   ├── participants.py     # 참가자 등록·조회·초기화 API
│   ├── summary.py          # 후보 시간 TOP 3 API
│   └── errors.py           # 라우터 공통 에러 처리
└── services/
    ├── meetings.py         # 모임 생성·조회 비즈니스 로직
    ├── participants.py     # 참가자 등록·조회·초기화 로직
    └── summary.py          # 후보 시간 집계 로직
```

프론트엔드:

```text
frontend/
├── main.py                 # Streamlit 설정, 스타일 주입, 전체 화면 조립
├── api.py                  # FastAPI 백엔드 호출 함수
├── state.py                # URL 쿼리 파라미터와 세션 상태 동기화
├── styles.py               # Streamlit 커스텀 스타일
├── time_utils.py           # 날짜·시간 옵션, 시간 포맷, 슬롯 생성
├── components/
│   ├── layout.py           # 헤더, 푸터, 섹션 제목
│   ├── summary.py          # 후보 시간 요약 카드
│   └── time_form.py        # 시작·종료 시간 선택 폼
└── views/
    └── meeting_page.py     # 메인 페이지 흐름, 등록 폼, 참가자 목록
```

도커 및 실행 설정:

```text
Dockerfile.back             # 백엔드 도커 이미지 정의
Dockerfile.front            # 프론트엔드 도커 이미지 정의
docker-compose.yml          # 백엔드, 프론트엔드, SQLite 데이터 volume 구성
Caddyfile                   # 운영 서버에서 DuckDNS 도메인을 프론트엔드로 연결하는 Caddy reverse proxy 설정
```

`docker-compose.yml`은 개발 편의를 위해 `backend/`와 `frontend/`를 컨테이너에 바인드 마운트합니다. 코드 수정 시 자동 반영되며, 백엔드는 `uvicorn --reload`로 재시작됩니다.

### API 엔드포인트
- `GET /health`: 헬스 체크.
- `POST /meetings`: 모임 이름 등록(이미 존재하면 그대로 유지).
- `GET /meetings/{meeting_name}`: 특정 모임의 참가자 수와 총 슬롯 수 조회.
- `POST /participants`: 본인 이름과 가능 시간 슬롯 목록 등록.
- `GET /participants?meeting_name=...`: 특정 모임의 참가자 목록 조회.
- `GET /summary?meeting_name=...`: 특정 모임의 후보 시간 TOP 3 조회.
- `DELETE /reset?meeting_name=...`: 해당 모임의 참가자와 시간 데이터 전체 삭제.

프론트에서 다른 백엔드 주소를 쓰려면 `API_BASE_URL` 환경변수를 설정하세요.

## 라이선스

이 프로젝트는 MIT License를 따릅니다.

Copyright (c) 2026 Surim

소프트웨어를 사용, 복사, 수정, 병합, 게시, 배포, 재라이선스 및 판매할 수 있으며,
배포 시 저작권 고지와 라이선스 고지를 함께 포함해야 합니다.
자세한 내용은 `LICENSE` 파일을 확인하세요.
