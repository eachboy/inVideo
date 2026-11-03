from fastapi import FastAPI

app = FastAPI()


@app.get("/api/v1/health")
def read_health():
    return {"status": "ok"}
