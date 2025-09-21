from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import httpx
import os 
import time
import shutil
import datetime

app = FastAPI()
START = time.monotonic()

STORAGE_URL = os.getenv("STORAGE_URL", "http://storage:8080")
SERVICE2_URL = os.getenv("SERVICE2_URL", "http://service2:3000")
VSTORAGE_PATH = os.getenv("VSTORAGE_PATH", "/vstorage/log.txt")


def iso_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def uptime_hours() -> float:
    return round((time.monotonic() - START) / 3600, 3)


def free_disk_mb() -> int:
    _, _, free = shutil.disk_usage("/")
    return int(free / (1024 * 1024))


def my_record() -> str:
    timestamp = iso_utc()
    uptime = uptime_hours()
    free_disk = free_disk_mb()

    return f"{timestamp}: uptime {uptime} hours, free disk in root: {free_disk} MBytes"

async def append_vstorage(line: str) -> None:
    os.makedirs(os.path.dirname(VSTORAGE_PATH), exist_ok=True)
    with open(VSTORAGE_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")

@app.get("/status", response_class=PlainTextResponse)
async def status() -> str:
    rec1 = my_record()

    async with httpx.AsyncClient() as client:
        # send to Storage
        await client.post(f"{STORAGE_URL}/log", content=rec1, headers={"Content-Type": "text/plain"})
        await append_vstorage(rec1) # write to vStorage
        res = await client.get(f"{SERVICE2_URL}/status") # forward to Service2
        rec2 = res.text

    return rec1 + "\n" + rec2

@app.get("/log", response_class=PlainTextResponse)
async def log() -> str:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{STORAGE_URL}/log")
        return r.text

# For teacher's convenience
@app.delete("/log")
async def clear_log():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.delete(f"{STORAGE_URL}/log")
            r.raise_for_status()
            notes = "storage_cleared"
    except Exception as e:
        notes = f"storage_clear_error={e}"

    return {"cleared": True, "notes": notes}