import React, { useState, useEffect } from "react";
import { Timer, AlertTriangle, Play, Pause, RotateCcw } from "lucide-react";

export default function RekeyTimer() {
  const [secondsLeft, setSecondsLeft] = useState(600); // 10 minutes
  const [isRunning, setIsRunning] = useState(false);
  const totalSeconds = 600;

  useEffect(() => {
    let interval = null;
    if (isRunning && secondsLeft > 0) {
      interval = setInterval(() => {
        setSecondsLeft((prev) => prev - 1);
      }, 1000);
    } else if (secondsLeft === 0) {
      setIsRunning(false);
    }
    return () => clearInterval(interval);
  }, [isRunning, secondsLeft]);

  const formatTime = (total) => {
    const mins = Math.floor(total / 60);
    const secs = total % 60;
    return `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
  };

  const resetTimer = () => {
    setIsRunning(false);
    setSecondsLeft(600);
  };

  const progressPercent = ((totalSeconds - secondsLeft) / totalSeconds) * 100;
  const isCritical = secondsLeft < 180; // under 3 minutes

  return (
    <div className={`p-4 rounded-xl border backdrop-blur-md transition-all ${
      isCritical 
        ? "border-red-600/70 bg-red-950/30 shadow-[0_0_20px_rgba(239,68,68,0.25)]" 
        : "border-amber-900/50 bg-neutral-900/70 shadow-lg"
    }`}>
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className={`p-2.5 rounded-lg border ${
            isCritical 
              ? "bg-red-500/20 border-red-500/40 text-red-400 animate-pulse" 
              : "bg-amber-500/10 border-amber-500/30 text-amber-400"
          }`}>
            <Timer className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs uppercase font-tactical tracking-widest text-neutral-400">
                Ring 7 Rekey Monitor
              </span>
              {isRunning && (
                <span className="inline-flex items-center px-1.5 py-0.2 rounded text-[10px] font-bold bg-red-500/20 text-red-400 border border-red-500/30 animate-pulse">
                  COUNTDOWN ACTIVE
                </span>
              )}
            </div>
            <div className={`text-2xl font-black font-tactical tracking-wider ${
              isCritical ? "text-red-400" : "text-amber-400"
            }`}>
              {formatTime(secondsLeft)}
              <span className="text-xs text-neutral-500 font-normal ml-2">/ 10:00 (600s)</span>
            </div>
          </div>
        </div>

        {/* Timer Control Buttons */}
        <div className="flex items-center gap-1.5">
          <button
            onClick={() => setIsRunning(!isRunning)}
            className={`p-2 rounded-lg border text-xs font-tactical flex items-center gap-1.5 transition-all ${
              isRunning 
                ? "bg-amber-500/20 border-amber-500/40 text-amber-300 hover:bg-amber-500/30" 
                : "bg-emerald-500/20 border-emerald-500/40 text-emerald-300 hover:bg-emerald-500/30"
            }`}
            title={isRunning ? "Pause Timer" : "Start Live Alarm Simulation"}
          >
            {isRunning ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            <span className="hidden sm:inline">{isRunning ? "Pause" : "Arm Alarm"}</span>
          </button>
          <button
            onClick={resetTimer}
            className="p-2 rounded-lg border border-neutral-800 bg-neutral-900 text-neutral-400 hover:text-white hover:border-neutral-700 transition-all text-xs"
            title="Reset Rekey Clock"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-neutral-950 rounded-full h-1.5 mt-3 overflow-hidden border border-neutral-800">
        <div
          className={`h-full transition-all duration-1000 ${
            isCritical ? "bg-red-500 animate-pulse" : "bg-gradient-to-r from-amber-500 to-red-500"
          }`}
          style={{ width: `${progressPercent}%` }}
        />
      </div>

      <div className="flex items-center justify-between text-[11px] font-tactical text-neutral-500 mt-1.5">
        <span>Exploit Buffer: 10 Minute Rekey Countdown</span>
        <span>{Math.round(100 - progressPercent)}% Time Remaining</span>
      </div>
    </div>
  );
}
