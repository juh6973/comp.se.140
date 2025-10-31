import express from "express";
import fs from "fs";
import path from "path";
import checkDiskSpace from "check-disk-space";
import fetch from "node-fetch";

const app = express();
const started = Date.now();
const STORAGE_URL = process.env.STORAGE_URL || "http://storage:8080";

function isoUtc(): string {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function uptimeHours(): number {
  return Math.round(((Date.now() - started) / 3600_000) * 1000) / 1000;
}

async function freeDiskMB(): Promise<number> {
  const { free } = await checkDiskSpace("/");
  return Math.floor(free / (1024 * 1024));
}

async function myRecord(): Promise<string> {
  const free = await freeDiskMB();
  return `${isoUtc()}: uptime ${uptimeHours()} hours, free disk in root: ${free} MBytes`;
}

app.get("/status", async (_req, res) => {
  const rec = await myRecord();
  try {
    await fetch(`${STORAGE_URL}/log`, {
      method: "POST",
      body: rec,
      headers: { "Content-Type": "text/plain" }
    });
  } catch (err) {
    console.error("Failed to send to storage:", err);
  }
  res.type("text/plain").send(rec);
});

//START THE SERVER HERE
const port = Number(process.env.PORT) || 3000;
app.listen(port, () => {
  console.log(`Service2 listening on port ${port}`);
});