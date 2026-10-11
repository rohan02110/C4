import React, { useState, useEffect } from "react";
import { 
  Shield, 
  Flame, 
  Volume2, 
  VolumeX, 
  Trophy, 
  Users, 
  Terminal, 
  Layers, 
  Key, 
  Check
} from "lucide-react";
import confetti from "canvas-confetti";
import ChakravyuhaCanvas from "./components/ChakravyuhaCanvas";
import RingDossier from "./components/RingDossier";
import RekeyTimer from "./components/RekeyTimer";
import FragmentAssembler from "./components/FragmentAssembler";
import { RINGS_DATA } from "./data/ringsData";

export default function App() {
  const [selectedRingId, setSelectedRingId] = useState(1);
  const [solvedRings, setSolvedRings] = useState([]);
  const [soundEnabled, setSoundEnabled] = useState(false);
  const [activeTab, setActiveTab] = useState("dossier"); // "dossier", "fragments"
  const [showVictoryModal, setShowVictoryModal] = useState(false);
  const [revealedFlag, setRevealedFlag] = useState(null);
  const [activeRole, setActiveRole] = useState("A");

  // Prevent developer tools inspection and source viewing
  useEffect(() => {
    const handleContextMenu = (e) => {
      e.preventDefault();
      return false;
    };

    const handleKeyDown = (e) => {
      // F12
      if (e.key === "F12" || e.keyCode === 123) {
        e.preventDefault();
        return false;
      }
      // Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C (Inspect / Console)
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && ["I", "i", "J", "j", "C", "c"].includes(e.key)) {
        e.preventDefault();
        return false;
      }
      // Ctrl+U (View Source)
      if ((e.ctrlKey || e.metaKey) && (e.key === "u" || e.key === "U")) {
        e.preventDefault();
        return false;
      }
      // Ctrl+S (Save)
      if ((e.ctrlKey || e.metaKey) && (e.key === "s" || e.key === "S")) {
        e.preventDefault();
        return false;
      }
    };

    window.addEventListener("contextmenu", handleContextMenu);
    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("contextmenu", handleContextMenu);
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, []);

  // Ambient sound drone
  useEffect(() => {
    let audioCtx = null;
    let osc1 = null;
    let osc2 = null;
    let gainNode = null;

    if (soundEnabled) {
      try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        audioCtx = new AudioContext();
        osc1 = audioCtx.createOscillator();
        osc2 = audioCtx.createOscillator();
        gainNode = audioCtx.createGain();

        osc1.type = "sawtooth";
        osc1.frequency.setValueAtTime(55, audioCtx.currentTime);
        osc2.type = "sine";
        osc2.frequency.setValueAtTime(110, audioCtx.currentTime);

        gainNode.gain.setValueAtTime(0.03, audioCtx.currentTime);

        osc1.connect(gainNode);
        osc2.connect(gainNode);
        gainNode.connect(audioCtx.destination);

        osc1.start();
        osc2.start();
      } catch (err) {
        console.warn("Audio unavailable", err);
      }
    }

    return () => {
      if (osc1) osc1.stop();
      if (osc2) osc2.stop();
      if (audioCtx) audioCtx.close();
    };
  }, [soundEnabled]);

  const handleFlagSubmit = (flagId) => {
    if (!solvedRings.includes(flagId)) {
      setSolvedRings([...solvedRings, flagId]);
    }
  };

  const selectedRing = RINGS_DATA.find((r) => r.id === selectedRingId) || RINGS_DATA[0];

  const teamRoles = [
    { id: "A", name: "Player A", title: "Reconnaissance", rings: [1, 2] },
    { id: "B", name: "Player B", title: "Web & Database", rings: [2, 3] },
    { id: "C", name: "Player C", title: "Forensics & Stego", rings: [4, 6, 5] },
    { id: "D", name: "Player D", title: "RE & Binary Systems", rings: [7, 8] },
  ];

  return (
    <div 
      onContextMenu={(e) => e.preventDefault()}
      className="min-h-screen bg-neutral-950 text-neutral-100 flex flex-col bg-grid-pattern selection:bg-amber-500 selection:text-black select-none"
    >
      {/* Top Navigation Bar */}
      <header className="sticky top-0 z-40 border-b border-neutral-800 bg-neutral-950/90 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
          {/* Logo & Title */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 via-red-600 to-amber-700 p-0.5 shadow-lg shadow-amber-500/20">
              <div className="w-full h-full bg-neutral-950 rounded-[10px] flex items-center justify-center">
                <Flame className="w-5 h-5 text-amber-400" />
              </div>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-mono text-base sm:text-lg font-bold tracking-wide text-white">
                  CHAKRAVYUHA
                </span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-red-500/20 border border-red-500/30 text-red-400 font-mono font-bold uppercase">
                  Ring 7
                </span>
              </div>
              <div className="text-[10px] text-neutral-500 font-mono hidden sm:block">
                Chakravyuha CTF • 7 Stage Infrastructure Defense
              </div>
            </div>
          </div>

          {/* Center Stats */}
          <div className="hidden md:flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl border border-neutral-800 bg-neutral-900/60 text-xs font-mono">
              <Shield className="w-4 h-4 text-emerald-400" />
              <span className="text-neutral-400">Stages Solved:</span>
              <span className="font-bold text-emerald-300">
                {solvedRings.length} / 6
              </span>
            </div>

            <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl border border-neutral-800 bg-neutral-900/60 text-xs font-mono">
              <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
              <span className="text-neutral-400">Final Stage:</span>
              <span className="text-amber-300">
                Admin Evaluation Only
              </span>
            </div>
          </div>

          {/* Audio Control */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => setSoundEnabled(!soundEnabled)}
              className={`p-2 rounded-xl border text-xs font-mono transition-all cursor-pointer ${
                soundEnabled 
                  ? "bg-amber-500/20 border-amber-500/50 text-amber-300" 
                  : "bg-neutral-900 border-neutral-800 text-neutral-400 hover:text-white"
              }`}
              title={soundEnabled ? "Mute Audio" : "Enable Ambient Sound"}
            >
              {soundEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </header>

      {/* Team Role Selector */}
      <div className="border-b border-neutral-900 bg-neutral-950/60 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2 flex items-center justify-between text-xs font-mono overflow-x-auto">
          <div className="flex items-center gap-1 text-neutral-500 whitespace-nowrap mr-3">
            <Users className="w-3.5 h-3.5 text-amber-500" />
            <span>Track:</span>
          </div>
          <div className="flex items-center gap-2">
            {teamRoles.map((role) => (
              <button
                key={role.id}
                onClick={() => {
                  setActiveRole(role.id);
                  setSelectedRingId(role.rings[0]);
                }}
                className={`px-2.5 py-1 rounded-lg border text-xs whitespace-nowrap transition-all cursor-pointer ${
                  activeRole === role.id
                    ? "bg-amber-500/20 border-amber-500/50 text-amber-300 font-bold"
                    : "border-neutral-800 bg-neutral-900/40 text-neutral-400 hover:text-white"
                }`}
              >
                <span>{role.name} ({role.title})</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 flex flex-col gap-6">
        {/* Rekey Timer */}
        <RekeyTimer />

        {/* Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Column: Canvas Topology */}
          <div className="lg:col-span-5 flex flex-col gap-4">
            <div className="flex items-center justify-between px-1">
              <h3 className="text-xs uppercase font-mono text-neutral-400 flex items-center gap-1.5">
                <Layers className="w-4 h-4 text-amber-500" />
                <span>Formation Topology</span>
              </h3>
              <span className="text-[11px] font-mono text-amber-400">
                Ring {selectedRing.id}
              </span>
            </div>

            <ChakravyuhaCanvas
              rings={RINGS_DATA}
              selectedRingId={selectedRingId}
              onSelectRing={setSelectedRingId}
              solvedRings={solvedRings}
            />

            {/* Ring Selectors */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {RINGS_DATA.map((ring) => {
                const isSelected = ring.id === selectedRingId;
                const isSolved = solvedRings.includes(ring.flagId);

                return (
                  <button
                    key={ring.id}
                    onClick={() => {
                      setSelectedRingId(ring.id);
                      if (ring.id === 8) setActiveTab("fragments");
                      else setActiveTab("dossier");
                    }}
                    className={`p-2.5 rounded-xl border text-left transition-all cursor-pointer flex flex-col justify-between ${
                      isSelected
                        ? "border-amber-500/60 bg-amber-500/10 shadow-lg shadow-amber-500/10"
                        : "border-neutral-800 bg-neutral-900/40 hover:border-neutral-700"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className={`text-[10px] font-mono font-bold ${
                        isSolved ? "text-emerald-400" : (isSelected ? "text-amber-400" : "text-neutral-500")
                      }`}>
                        {ring.id === 8 ? "CORE" : `RING 0${ring.id}`}
                      </span>
                      {isSolved && <Check className="w-3.5 h-3.5 text-emerald-400" />}
                    </div>
                    <div className="text-xs font-bold font-sans truncate text-neutral-200">
                      {ring.guardian}
                    </div>
                    <div className="text-[10px] font-mono text-neutral-500 truncate mt-0.5">
                      {ring.id <= 6 ? `STAGE 0${ring.id}` : "CORE"}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Right Column: Briefing / Assembler */}
          <div className="lg:col-span-7 flex flex-col gap-4">
            {/* Tabs */}
            <div className="flex items-center gap-2 border-b border-neutral-800 pb-2">
              <button
                onClick={() => setActiveTab("dossier")}
                className={`px-4 py-2 rounded-xl text-xs font-mono font-bold flex items-center gap-2 transition-all cursor-pointer ${
                  activeTab === "dossier"
                    ? "bg-amber-500 text-black shadow-lg shadow-amber-500/20"
                    : "text-neutral-400 hover:text-white bg-neutral-900 border border-neutral-800"
                }`}
              >
                <Terminal className="w-3.5 h-3.5" />
                <span>Stage Briefing</span>
              </button>

              <button
                onClick={() => setActiveTab("fragments")}
                className={`px-4 py-2 rounded-xl text-xs font-mono font-bold flex items-center gap-2 transition-all cursor-pointer ${
                  activeTab === "fragments"
                    ? "bg-amber-500 text-black shadow-lg shadow-amber-500/20"
                    : "text-neutral-400 hover:text-white bg-neutral-900 border border-neutral-800"
                }`}
              >
                <Key className="w-3.5 h-3.5" />
                <span>Fragment Assembler</span>
              </button>
            </div>

            {/* Tab Body */}
            {activeTab === "dossier" && (
              <RingDossier
                ring={selectedRing}
                isSolved={solvedRings.includes(selectedRing.flagId)}
                onFlagSubmit={handleFlagSubmit}
              />
            )}

            {activeTab === "fragments" && (
              <div className="flex flex-col gap-4">
                <FragmentAssembler
                  onFinalFlagRevealed={(flag) => {
                    setRevealedFlag(flag);
                    setShowVictoryModal(true);
                  }}
                />
                <RingDossier
                  ring={RINGS_DATA[6]} // Ring 7
                  isSolved={solvedRings.includes("FLAG_RING_7")}
                  onFlagSubmit={handleFlagSubmit}
                />
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Victory Modal */}
      {showVictoryModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="max-w-lg w-full p-6 sm:p-8 rounded-3xl border border-amber-500/60 bg-neutral-950 shadow-2xl text-center relative">
            <div className="w-14 h-14 rounded-2xl bg-amber-500/20 border border-amber-500/50 flex items-center justify-center mx-auto mb-4 text-amber-400">
              <Trophy className="w-7 h-7" />
            </div>

            <h2 className="text-2xl font-bold font-mono text-white mb-2">
              Sanctum Core Decrypted
            </h2>
            <p className="text-amber-400 font-mono text-xs uppercase mb-4">
              All fragments assembled and verified
            </p>

            {revealedFlag && (
              <div className="p-4 rounded-xl bg-neutral-900 border border-neutral-800 mb-6 font-mono text-xs text-emerald-400 select-all">
                {revealedFlag}
              </div>
            )}

            <div className="text-xs text-neutral-400 font-mono leading-relaxed mb-6">
              Submit this final flag directly to the CTF Administrator for manual evaluation.
            </div>

            <button
              onClick={() => setShowVictoryModal(false)}
              className="px-6 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-mono font-bold text-xs uppercase transition-all cursor-pointer shadow-lg shadow-amber-500/20"
            >
              Close
            </button>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="border-t border-neutral-900 py-4 text-center text-xs font-mono text-neutral-600">
        CHAKRAVYUHA CTF • DEFENSIVE INFRASTRUCTURE BENCHMARK
      </footer>
    </div>
  );
}
