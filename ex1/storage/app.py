from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse
import os

app = FastAPI()
DATA_DIR = os.getenv("DATA_DIR")
LOG_PATH = os.path.join(DATA_DIR, "log.txt")

os.makedirs(DATA_DIR, exist_ok=True)
open(LOG_PATH, "a").close()

@app.post("/log")
async def append_log(body: bytes):
    with open(LOG_PATH, "ab") as f:
        f.write(body + b"\n")
    
    return {"ok": True}

@app.get("/log", response_class=PlainTextResponse)
async def get_log():
    with open(LOG_PATH, "rb") as f:
        content = f.read()
    
    return Response(content, media_type="text/plain")

# Cleanup function for the teacher's convenience
@app.delete("/log")
async def clear_log():
    open(LOG_PATH, "w").close()
    
    return {"cleared": True}