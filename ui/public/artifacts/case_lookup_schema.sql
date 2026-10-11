-- VYUHA Relational Vault Database Schema (Drona's Vault)
-- Target Engine: PostgreSQL 15 / SQLite3 Compatible

CREATE TABLE IF NOT EXISTS cases (
    case_id INTEGER PRIMARY KEY,
    case_tag VARCHAR(64) NOT NULL,
    classification VARCHAR(32) NOT NULL,
    clearance_token VARCHAR(128) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dispatch_triggers (
    trigger_id INTEGER PRIMARY KEY AUTOINCREMENT,
    action VARCHAR(32) NOT NULL,
    target_case INTEGER NOT NULL,
    status VARCHAR(16) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed Confidential Docket
INSERT INTO cases (case_id, case_tag, classification, clearance_token, description) VALUES
(1001, 'GATEWAY_TELEMETRY', 'PUBLIC', 'SEAL_PUBLIC_VIEW', 'Standard telemetry report'),
(2042, 'REKEY_AUDIT_LOG', 'RESTRICTED', 'SEAL_AUDIT_OK', 'Cryptographic rotation logs'),
(4471, 'DRONA_SACRED_VAULT', 'SOVEREIGN_TOP_SECRET', 'DRONA_VAULT_QUERY_INJECTED_4471', 'Classified operation logs linking Drona syntax breach to Ashwatthama memory unlock webhook');
