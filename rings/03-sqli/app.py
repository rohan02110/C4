import os
import re
import sqlite3
import requests
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI(title="Drona Archive Vault", version="1.0.0")

FLAG_RING_3 = os.getenv("FLAG_RING_3", "DRONA_VAULT_QUERY_INJECTED_4471")
ASHWATTHAMA_UNLOCK_URL = os.getenv("ASHWATTHAMA_UNLOCK_URL", "http://ashwatthama-host:8081/unlock")

from pathlib import Path
DB_FILE = os.getenv("DB_FILE", str(Path(__file__).resolve().parent / "vyuha_vault.db"))

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY,
            case_id INTEGER,
            tag TEXT,
            classification TEXT,
            clearance_token TEXT,
            notes TEXT
        )
    """)
    c.execute("DELETE FROM cases")
    # Standard cases
    c.execute("INSERT INTO cases (case_id, tag, classification, clearance_token, notes) VALUES (1190, 'routine_sync', 'UNCLASSIFIED', 'TOKEN_ROUTINE_1190', 'Normal gateway ping')")
    c.execute("INSERT INTO cases (case_id, tag, classification, clearance_token, notes) VALUES (2201, 'node_reboot', 'RESTRICTED', 'TOKEN_REBOOT_2201', 'Perimeter restart log')")
    c.execute("INSERT INTO cases (case_id, tag, classification, clearance_token, notes) VALUES (3387, 'audit_report', 'CONFIDENTIAL', 'TOKEN_AUDIT_3387', 'Integrity hash review')")
    
    # Secret case 4471 (Target for Ring 3)
    c.execute(f"INSERT INTO cases (case_id, tag, classification, clearance_token, notes) VALUES (4471, 'ashwatthama_rage', 'TOP_SECRET_CORE', '{FLAG_RING_3}', 'Ashwatthama memory artifact unlocked. Dispatching webhook.')")
    conn.commit()
    conn.close()

init_db()

BLOCKED_PATTERNS = [
    r"\s+",              # Disallow standard whitespace (must use %0a / newlines or tabs)
    r"--",               # Disallow standard line comments
    r"/\*",              # Disallow standard block comments
    r"\bUNION\b",        # Disallow UNION injection
]

def sanitize_input(case_tag: str):
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, case_tag, re.IGNORECASE):
            raise HTTPException(status_code=400, detail="Security violation: malformed AST / forbidden delimiter detected")
    return case_tag

@app.get("/health")
def health():
    return {"status": "ok", "service": "drona-vault"}

@app.get("/api/v1/cases/lookup")
def lookup_case(case_tag: str = Query(...)):
    clean_tag = sanitize_input(case_tag)
    
    # VULNERABILITY: Raw SQL string concatenation
    query = f"SELECT case_id, tag, classification, clearance_token, notes FROM cases WHERE tag='{clean_tag}'"

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        # Executes query
        c.execute(query)
        rows = c.fetchall()
        
        results = []
        unlocked_case_4471 = False

        for r in rows:
            res = {
                "case_id": r[0],
                "tag": r[1],
                "classification": r[2],
                "clearance_token": r[3],
                "notes": r[4]
            }
            results.append(res)
            if r[0] == 4471:
                unlocked_case_4471 = True

        # If Case 4471 is returned by the SQLi, trigger the unlock webhook
        if unlocked_case_4471:
            try:
                requests.post(f"{ASHWATTHAMA_UNLOCK_URL}?case=4471", timeout=3)
            except Exception as e:
                pass # Continue returning results even if network test is offline

        return {"status": "success", "query_matched": len(results), "records": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database execution error: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
