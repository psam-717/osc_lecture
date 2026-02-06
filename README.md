# FastAPI Project

A FastAPI project for openclaw.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

- Swagger docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

- `GET /` - Hello World
- `GET /health` - Health check
