from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import os

app = FastAPI()
LOG_PATH = os.getenv("LOG_PATH", "/data/log.txt")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
open(LOG_PATH, "a").close()

@app.post("/log")
async def append_log(body: str):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(body + "\n")
    return {"ok": True}

@app.get("/log", response_class=PlainTextResponse)
async def get_log():
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        return f.read()

@app.delete("/log")
async def clear_log():
    open(LOG_PATH, "w").close()
    return {"cleared": True}