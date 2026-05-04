# Time Table

10명 이상이 각자 가능한 날짜와 시간 슬롯을 입력하면 다수결 기준으로 약속 후보 시간 TOP 3를 보여주는 간단한 웹앱입니다.

모임 이름을 기준으로 데이터가 분리됩니다. 친구들에게 같은 모임 이름을 공유하면 해당 이름을 입력한 사람들의 일정만 함께 집계됩니다.

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

- `POST /meetings`: 모임 이름 등록
- `GET /meetings/{meeting_name}`: 특정 모임 현황 확인
- `backend/main.py`: FastAPI API와 SQLite 저장소, 모임 이름별 데이터 분리
- `frontend/main.py`: Streamlit 화면
- `frontend/styles.py`: `cdx_orchestrator` 팔레트를 참고한 Streamlit 스타일
- `Dockerfile.back`: FastAPI 백엔드 이미지
- `Dockerfile.front`: Streamlit 프론트엔드 이미지
- `docker-compose.yml`: 백엔드, 프론트엔드, SQLite 데이터 volume 구성

프론트에서 다른 백엔드 주소를 쓰려면 `API_BASE_URL` 환경변수를 설정하세요.

## 라이선스

이 프로젝트는 MIT License를 따릅니다.

Copyright (c) 2026 Surim

소프트웨어를 사용, 복사, 수정, 병합, 게시, 배포, 재라이선스 및 판매할 수 있으며,
배포 시 저작권 고지와 라이선스 고지를 함께 포함해야 합니다.
자세한 내용은 `LICENSE` 파일을 확인하세요.
