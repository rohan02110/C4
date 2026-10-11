import os
import hashlib
import time
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Chakravyuha Scoring Engine", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Literal target flags from specification
FLAG_CONFIG = {
    "FLAG_RING_1": {
        "ring": 1,
        "guardian": "Jayadratha",
        "domain": "OSINT",
        "points": 150,
        "value": os.getenv("FLAG_RING_1", "JAYADRATHA_GATE_BYPASS_9a8f27c3e510")
    },
    "FLAG_RING_2": {
        "ring": 2,
        "guardian": "Kripacharya",
        "domain": "Web Application Security",
        "points": 200,
        "value": os.getenv("FLAG_RING_2", "KRIPACHARYA_ADMIN_SEAM_EXPOSED_55d1")
    },
    "FLAG_RING_3": {
        "ring": 3,
        "guardian": "Drona",
        "domain": "SQL Injection",
        "points": 250,
        "value": os.getenv("FLAG_RING_3", "DRONA_VAULT_QUERY_INJECTED_4471")
    },
    "FLAG_RING_4": {
        "ring": 4,
        "guardian": "Ashwatthama",
        "domain": "Memory Forensics",
        "points": 250,
        "value": os.getenv("FLAG_RING_4", "ASHWATTHAMA_MEMORY_VAD_CARVED_77c2")
    },
    "FLAG_RING_5": {
        "ring": 5,
        "guardian": "Shalya",
        "domain": "Reverse Engineering",
        "points": 300,
        "value": os.getenv("FLAG_RING_5", "SHALYA_DISPATCHER_RESOLVED_66a1")
    },
    "FLAG_RING_6": {
        "ring": 6,
        "guardian": "Karna",
        "domain": "Steganography",
        "points": 200,
        "value": os.getenv("FLAG_RING_6", "KARNA_ARMOR_POLYGLOT_EXTRACTED_11e9")
    },
    "FLAG_RING_7": {
        "ring": 7,
        "guardian": "Brihadbala",
        "domain": "Binary Exploitation",
        "points": 350,
        "value": os.getenv("FLAG_RING_7", "BRIHADBALA_SANCTUM_COMPROMISED_7714")
    },
    "FLAG_FINAL": {
        "ring": 8,
        "guardian": "Abhimanyu's Exit",
        "domain": "Cryptographic Escape",
        "points": 500,
        "value": os.getenv("FLAG_FINAL", "KCTF{4\\x42HIM4NYU_F0UND_7H3_3XI7_88}")
    }
}

# Hints disabled for sovereign competition
HINTS = {}

# In-memory storage for demonstration / event run
TEAMS: Dict[str, Dict[str, Any]] = {}
AUDIT_LOG: List[Dict[str, Any]] = []

def get_team_state(team_id: str):
    if team_id not in TEAMS:
        TEAMS[team_id] = {
            "team_id": team_id,
            "score": 0,
            "solved": [],
            "hints_purchased": [],
            "start_time": time.time(),
            "final_escaped": False
        }
    return TEAMS[team_id]

class SubmitRequest(BaseModel):
    team_id: str
    flag: str

class HintRequest(BaseModel):
    team_id: str
    hint_id: int

@app.get("/health")
def health():
    return {"status": "ok", "service": "chakravyuha-scoring-engine"}

@app.get("/scoreboard")
def get_scoreboard():
    leaderboard = []
    for team_id, data in TEAMS.items():
        leaderboard.append({
            "team_id": team_id,
            "score": data["score"],
            "solved_count": len(data["solved"]),
            "solved_rings": data["solved"],
            "final_escaped": data["final_escaped"]
        })
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    return {"scoreboard": leaderboard}

@app.post("/submit")
def submit_flag(req: SubmitRequest):
    team = get_team_state(req.team_id)
    submitted = req.flag.strip()
    
    # Audit logging: Never store plain flag, store hash
    flag_hash = hashlib.sha256(submitted.encode()).hexdigest()
    AUDIT_LOG.append({
        "timestamp": time.time(),
        "team_id": req.team_id,
        "flag_hash": flag_hash
    })

    for flag_id, info in FLAG_CONFIG.items():
        expected = info["value"].strip()
        if submitted == expected:
            # Enforce restriction: Automated submissions only for stages 1 to second-last (Stage 6)
            # Ring 7 / Final submissions must be evaluated and added by the Admin directly
            if info["ring"] >= 7:
                return {
                    "status": "restricted",
                    "message": "Manual Administrator Evaluation Required: Automated submissions are only accepted for stages 1 through 6. The final stage must be submitted directly to the CTF Administrator.",
                    "score": team["score"]
                }

            if flag_id in team["solved"]:
                return {
                    "status": "already_solved",
                    "message": f"Ring {info['ring']} ({info['guardian']}) already completed by your team.",
                    "score": team["score"]
                }
            
            team["solved"].append(flag_id)
            team["score"] += info["points"]

            return {
                "status": "correct",
                "flag_id": flag_id,
                "ring": info["ring"],
                "guardian": info["guardian"],
                "points_awarded": info["points"],
                "current_score": team["score"],
                "message": f"Breach verified: {info['guardian']} defeated! Stage 0{info['ring']} authenticated."
            }

    return {
        "status": "incorrect",
        "message": "Flag validation failed. Integrity monitor rejected the submission.",
        "score": team["score"]
    }

@app.post("/hints/purchase")
def purchase_hint(req: HintRequest):
    raise HTTPException(status_code=403, detail="Hints are completely disabled for this competition.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
