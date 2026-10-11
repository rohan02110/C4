import React, { useState } from "react";
import { KeyRound, ShieldCheck, Lock, Unlock, Copy, Check } from "lucide-react";
import confetti from "canvas-confetti";

const IV_HEX = "6368616b726176797568615f32303236";
const CT_HEX = "eda1d5acc7dadb08451c96e1945c6409b7d2f694f13ad876402f93abc4db934435f3038616ef905c30912a7529daa427";

function hexToBytes(hex) {
  const bytes = new Uint8Array(hex.length / 2);
  for (let i = 0; i < hex.length; i += 2) {
    bytes[i / 2] = parseInt(hex.substr(i, 2), 16);
  }
  return bytes;
}

export default function FragmentAssembler({ onFinalFlagRevealed }) {
  const [f1, setF1] = useState("");
  const [f2, setF2] = useState("");
  const [f3, setF3] = useState("");
  const [decryptedPayload, setDecryptedPayload] = useState(null);
  const [copied, setCopied] = useState(false);

  const handleDecrypt = async () => {
    if (!f1.trim() || !f2.trim() || !f3.trim()) {
      setDecryptedPayload({
        success: false,
        message: "Missing fragments. Enter all 3 fragments to decrypt."
      });
      return;
    }

    try {
      const combined = f1.trim() + f2.trim() + f3.trim();
      const enc = new TextEncoder();
      const keyHash = await crypto.subtle.digest("SHA-256", enc.encode(combined));
      
      const cryptoKey = await crypto.subtle.importKey(
        "raw",
        keyHash,
        { name: "AES-CBC" },
        false,
        ["decrypt"]
      );

      const iv = hexToBytes(IV_HEX);
      const ct = hexToBytes(CT_HEX);

      const decrypted = await crypto.subtle.decrypt(
        { name: "AES-CBC", iv },
        cryptoKey,
        ct
      );

      const decStr = new TextDecoder().decode(decrypted);

      if (decStr && decStr.startsWith("KCTF{")) {
        setDecryptedPayload({
          success: true,
          finalFlag: decStr,
          message: "Payload decrypted successfully."
        });
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 }
        });
        if (onFinalFlagRevealed) {
          onFinalFlagRevealed(decStr);
        }
      } else {
        throw new Error("Invalid decryption");
      }
    } catch {
      setDecryptedPayload({
        success: false,
        message: "Decryption failed: Invalid fragment sequence."
      });
    }
  };

  const copyFlag = () => {
    if (decryptedPayload?.finalFlag) {
      navigator.clipboard.writeText(decryptedPayload.finalFlag);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="p-5 rounded-2xl border border-neutral-800 bg-neutral-900/60 backdrop-blur-xl shadow-xl">
      <div className="flex items-center justify-between pb-4 border-b border-neutral-800">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-400">
            <KeyRound className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-mono text-sm font-bold text-white">Cryptographic Fragment Assembler</h3>
            <p className="text-xs text-neutral-400 font-mono">Assemble Fragments 1, 2, and 3 to decrypt ring_core.enc</p>
          </div>
        </div>
        <span className="text-xs font-mono px-2 py-0.5 rounded bg-neutral-950 border border-neutral-800 text-amber-400">
          AES-256-CBC
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mt-4">
        {/* Fragment 1 */}
        <div className="p-3 rounded-xl border border-neutral-800 bg-neutral-950/80">
          <div className="flex items-center justify-between text-xs font-mono text-neutral-400 mb-1.5">
            <span className="text-amber-400 font-bold">Fragment 1</span>
            <span className="text-neutral-500">Stage 04</span>
          </div>
          <input
            type="text"
            value={f1}
            onChange={(e) => setF1(e.target.value)}
            className="w-full bg-neutral-900 border border-neutral-700/80 rounded-lg px-2.5 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-amber-500"
            placeholder=""
          />
        </div>

        {/* Fragment 2 */}
        <div className="p-3 rounded-xl border border-neutral-800 bg-neutral-950/80">
          <div className="flex items-center justify-between text-xs font-mono text-neutral-400 mb-1.5">
            <span className="text-amber-400 font-bold">Fragment 2</span>
            <span className="text-neutral-500">Stage 05</span>
          </div>
          <input
            type="text"
            value={f2}
            onChange={(e) => setF2(e.target.value)}
            className="w-full bg-neutral-900 border border-neutral-700/80 rounded-lg px-2.5 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-amber-500"
            placeholder=""
          />
        </div>

        {/* Fragment 3 */}
        <div className="p-3 rounded-xl border border-neutral-800 bg-neutral-950/80">
          <div className="flex items-center justify-between text-xs font-mono text-neutral-400 mb-1.5">
            <span className="text-amber-400 font-bold">Fragment 3</span>
            <span className="text-neutral-500">Stage 06</span>
          </div>
          <input
            type="text"
            value={f3}
            onChange={(e) => setF3(e.target.value)}
            className="w-full bg-neutral-900 border border-neutral-700/80 rounded-lg px-2.5 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-amber-500"
            placeholder=""
          />
        </div>
      </div>

      {/* Assembly Trigger Bar */}
      <div className="mt-4 p-3 rounded-xl bg-neutral-950 border border-neutral-800/80 font-mono text-xs text-neutral-400 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
        <div className="truncate">
          <span className="text-neutral-500">Mode: </span>
          <span className="text-amber-400">Multi-Fragment Key Assembly</span>
        </div>
        <button
          onClick={handleDecrypt}
          className="px-4 py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-black font-mono font-bold text-xs flex items-center gap-1.5 shadow-lg shadow-amber-500/20 transition-all cursor-pointer"
        >
          <Unlock className="w-3.5 h-3.5" />
          <span>Decrypt Core</span>
        </button>
      </div>

      {/* Decryption Result Panel */}
      {decryptedPayload && (
        <div className={`mt-4 p-4 rounded-xl border transition-all ${
          decryptedPayload.success 
            ? "border-emerald-600/60 bg-emerald-950/20" 
            : "border-red-600/60 bg-red-950/20"
        }`}>
          <div className="flex items-center gap-2">
            {decryptedPayload.success ? (
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
            ) : (
              <Lock className="w-4 h-4 text-red-400" />
            )}
            <span className={`text-xs font-mono ${
              decryptedPayload.success ? "text-emerald-400 font-bold" : "text-red-400"
            }`}>
              {decryptedPayload.message}
            </span>
          </div>

          {decryptedPayload.success && (
            <div className="mt-3 p-3 rounded-lg bg-neutral-950 border border-emerald-500/30 flex items-center justify-between gap-3">
              <div>
                <div className="text-[10px] font-mono text-neutral-500 uppercase">
                  Final Flag
                </div>
                <div className="font-mono text-sm font-bold text-emerald-300 select-all">
                  {decryptedPayload.finalFlag}
                </div>
                <div className="text-[10px] text-neutral-400 font-mono mt-1">
                  Submit this flag directly to the CTF Administrator.
                </div>
              </div>
              <button
                onClick={copyFlag}
                className="px-2.5 py-1.5 rounded bg-emerald-500/20 border border-emerald-500/40 text-emerald-300 hover:bg-emerald-500/30 text-xs font-mono flex items-center gap-1 transition-all cursor-pointer"
              >
                {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? "Copied" : "Copy"}</span>
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
