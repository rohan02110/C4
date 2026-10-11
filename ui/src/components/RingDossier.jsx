import React, { useState } from "react";
import { 
  Terminal, 
  CheckCircle2, 
  AlertCircle, 
  Download, 
  ExternalLink, 
  BookOpen, 
  Cpu, 
  Database, 
  Eye, 
  Binary, 
  Key, 
  Flame, 
  ArrowRight 
} from "lucide-react";
import confetti from "canvas-confetti";

async function sha256(message) {
  const msgBuffer = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest("SHA-256", msgBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
}

export default function RingDossier({ ring, isSolved, onFlagSubmit }) {
  const [submission, setSubmission] = useState("");
  const [statusMessage, setStatusMessage] = useState(null);

  const getDomainIcon = (domain) => {
    if (domain.includes("OSINT")) return <Eye className="w-4 h-4 text-amber-400" />;
    if (domain.includes("Web")) return <ExternalLink className="w-4 h-4 text-orange-400" />;
    if (domain.includes("Database")) return <Database className="w-4 h-4 text-red-400" />;
    if (domain.includes("Forensics")) return <Terminal className="w-4 h-4 text-purple-400" />;
    if (domain.includes("Reverse")) return <Cpu className="w-4 h-4 text-blue-400" />;
    if (domain.includes("Steganography")) return <Flame className="w-4 h-4 text-emerald-400" />;
    if (domain.includes("Binary")) return <Binary className="w-4 h-4 text-rose-400" />;
    return <Key className="w-4 h-4 text-amber-400" />;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!submission.trim()) return;

    const trimmed = submission.trim();
    const hash = await sha256(trimmed);
    if (hash === ring.flagHash) {
      setStatusMessage({
        type: "success",
        text: "Flag accepted. Stage verified."
      });
      confetti({
        particleCount: 80,
        spread: 60,
        origin: { y: 0.7 }
      });
      onFlagSubmit(ring.flagId);
      setSubmission("");
    } else {
      setStatusMessage({
        type: "error",
        text: "Invalid flag."
      });
    }
  };

  return (
    <div className="p-6 rounded-2xl border border-neutral-800 bg-neutral-900/60 backdrop-blur-xl shadow-2xl flex flex-col gap-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-neutral-800">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono text-amber-400 uppercase">
            <span>{ring.sanskritTitle}</span>
            <span>•</span>
            <span className="px-2 py-0.5 rounded bg-neutral-800 text-neutral-300 font-mono text-[10px]">
              {ring.flagType}
            </span>
          </div>
          <h2 className="text-2xl font-bold font-title text-white mt-1 flex items-center gap-2.5">
            {ring.name}
            {isSolved && (
              <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-mono font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                <CheckCircle2 className="w-3.5 h-3.5" /> SOLVED
              </span>
            )}
          </h2>
          <div className="flex items-center gap-2 mt-1 text-xs text-neutral-400 font-mono">
            <span className="text-neutral-200">{ring.guardian}</span>
            <span>—</span>
            <span>{ring.domain}</span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="px-3.5 py-2 rounded-xl bg-neutral-950 border border-neutral-800 text-center">
            <div className="text-[10px] text-neutral-500 uppercase font-mono">Difficulty</div>
            <div className={`text-xs font-bold font-mono mt-1 ${
              ring.difficulty.includes("Master") ? "text-red-400" : (ring.difficulty.includes("Hard") ? "text-orange-400" : "text-amber-300")
            }`}>
              {ring.difficulty}
            </div>
          </div>
          <div className="px-3.5 py-2 rounded-xl bg-neutral-950 border border-neutral-800 text-center">
            <div className="text-[10px] text-neutral-500 uppercase font-mono">Stage</div>
            <div className="text-xs font-bold font-mono mt-1 text-emerald-400">
              {ring.id <= 6 ? `0${ring.id} / 06` : "CORE"}
            </div>
          </div>
        </div>
      </div>

      {/* Narrative Context */}
      <div className="p-4 rounded-xl border border-amber-950/40 bg-amber-950/10 text-xs leading-relaxed text-amber-200/90 font-mono">
        <div className="flex items-center gap-2 text-amber-400 font-bold mb-1.5 text-xs">
          <BookOpen className="w-4 h-4" />
          <span>Intelligence Briefing</span>
        </div>
        <p className="italic">"{ring.lore}"</p>
      </div>

      {/* Technical Objective & Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 rounded-xl border border-neutral-800 bg-neutral-950/60">
          <div className="text-xs font-mono text-neutral-400 uppercase mb-1 flex items-center gap-1.5">
            {getDomainIcon(ring.domain)}
            <span>Objective</span>
          </div>
          <p className="text-xs text-neutral-300 leading-relaxed font-sans">
            {ring.technicalBrief}
          </p>
        </div>

        <div className="p-4 rounded-xl border border-neutral-800 bg-neutral-950/60 flex flex-col justify-between">
          <div>
            <div className="text-xs font-mono text-neutral-400 uppercase mb-1">
              Category
            </div>
            <div className="text-xs font-mono text-amber-300 font-semibold mb-3">
              {ring.domain}
            </div>
          </div>

          <div>
            <div className="text-[10px] font-mono text-neutral-500 uppercase">
              Target Endpoint
            </div>
            <div className="text-xs font-mono text-emerald-400 bg-neutral-900 px-2.5 py-1.5 rounded-lg border border-neutral-800 select-all truncate mt-1">
              {ring.connectionTarget}
            </div>
          </div>
        </div>
      </div>

      {/* Artifacts & Fragments */}
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs font-mono text-neutral-500 mr-2">Artifacts:</span>
        {ring.artifacts.map((art, idx) => (
          <a 
            key={idx} 
            href={`/artifacts/${art}`}
            download={art}
            target="_blank"
            rel="noopener noreferrer"
            title={`Download ${art}`}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono bg-neutral-900 border border-neutral-700/80 text-amber-400 hover:text-amber-300 hover:border-amber-500 hover:bg-neutral-800 transition-all cursor-pointer group shadow-sm"
          >
            <Download className="w-3.5 h-3.5 text-amber-500 group-hover:translate-y-0.5 transition-transform" />
            <span>{art}</span>
          </a>
        ))}
        {ring.fragment && (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-mono font-bold bg-amber-500/10 border border-amber-500/30 text-amber-300 ml-auto">
            <Key className="w-3.5 h-3.5" />
            <span>Yields {ring.fragment.name}</span>
          </span>
        )}
      </div>

      {/* Flag Submission Box — ONLY FOR STAGES 1 TO 6 (NO TEXT BOX FOR LAST STAGE) */}
      {ring.id <= 6 ? (
        <form onSubmit={handleSubmit} className="mt-2 pt-4 border-t border-neutral-800">
          <label className="block text-xs font-mono uppercase text-neutral-400 mb-2">
            Submit Token (Stage 0{ring.id})
          </label>
          <div className="flex items-center gap-2">
            <input
              type="text"
              value={submission}
              onChange={(e) => setSubmission(e.target.value)}
              disabled={isSolved}
              placeholder=""
              className="flex-1 bg-neutral-950 border border-neutral-800 rounded-xl px-4 py-2.5 text-xs font-mono text-white focus:outline-none focus:border-amber-500 transition-all"
            />
            <button
              type="submit"
              disabled={isSolved}
              className={`px-5 py-2.5 rounded-xl text-xs font-mono font-bold flex items-center gap-1.5 transition-all ${
                isSolved 
                  ? "bg-neutral-800 text-neutral-500 cursor-not-allowed" 
                  : "bg-amber-500 hover:bg-amber-400 text-black shadow-lg shadow-amber-500/20 cursor-pointer"
              }`}
            >
              <span>Submit</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {statusMessage && (
            <div className={`mt-3 p-3 rounded-lg border text-xs font-mono flex items-center gap-2 ${
              statusMessage.type === "success" 
                ? "bg-emerald-950/30 border-emerald-500/40 text-emerald-300" 
                : "bg-red-950/30 border-red-500/40 text-red-300"
            }`}>
              {statusMessage.type === "success" ? <CheckCircle2 className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
              <span>{statusMessage.text}</span>
            </div>
          )}
        </form>
      ) : null}
    </div>
  );
}
