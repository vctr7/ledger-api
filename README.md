# FastAPI + Supabase Ledger API

W4 SQL 워크북의 계좌, 거래, JOIN, 집계, 원자적 이체 실습을 기반으로 만든 FastAPI API입니다.

## 실행 방법

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Supabase의 PostgreSQL Session Pooler URL을 `.env`의 `DATABASE_URL`에 설정합니다.

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API

- `POST /accounts`
- `GET /accounts`
- `GET /accounts/{account_id}`
- `POST /transactions`
- `GET /accounts/{account_id}/detail`
- `GET /stats/by-category`
- `GET /health`

## Render 배포

1. GitHub 저장소에 `render.yaml`을 포함한 코드를 push합니다.
2. Render에서 **New Blueprint**를 선택합니다.
3. GitHub 저장소를 연결합니다.
4. `DATABASE_URL` 환경변수를 **Secret**로 추가합니다.
5. 배포를 실행합니다.

`render.yaml`은 Render의 Web Service 설정을 포함합니다.
