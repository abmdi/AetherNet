# AetherNet

Open-source multi-cloud network intelligence and security platform.

## Foundation preview
This is an intentionally small, testable architecture prototype, **not** the complete 2,005-file product.
It contains pure domain models, an application port, a credential-free demo adapter, and a FastAPI endpoint.

## Local setup (Python 3.12+)

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
ruff check .
pytest -q
uvicorn aethernet.api:app --reload
```

Try `http://127.0.0.1:8000/docs` and `http://127.0.0.1:8000/demo/inventory`.

## Publishing
Review code and tests before committing. Use an accurate author identity for automated contributions.
