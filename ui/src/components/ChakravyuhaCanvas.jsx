import React, { useRef, useEffect, useState } from "react";

export default function ChakravyuhaCanvas({ rings, selectedRingId, onSelectRing, solvedRings }) {
  const canvasRef = useRef(null);
  const [hoveredRingId, setHoveredRingId] = useState(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let animationFrameId;

    // Canvas sizing with devicePixelRatio support
    const updateSize = () => {
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.scale(dpr, dpr);
    };
    updateSize();

    let rotationAngle = 0;

    // Particle system swirling through the spiral
    const particles = Array.from({ length: 65 }, () => ({
      angle: Math.random() * Math.PI * 2,
      radius: 40 + Math.random() * 210,
      speed: 0.003 + Math.random() * 0.008,
      size: 1 + Math.random() * 2.2,
      opacity: 0.2 + Math.random() * 0.7,
      color: Math.random() > 0.4 ? "#f59e0b" : "#ef4444"
    }));

    const render = () => {
      const width = canvas.clientWidth;
      const height = canvas.clientHeight;
      const centerX = width / 2;
      const centerY = height / 2;
      const maxRadius = Math.min(width, height) * 0.44;

      ctx.clearRect(0, 0, width, height);

      // Deep atmospheric background glow
      const radialGrad = ctx.createRadialGradient(centerX, centerY, 10, centerX, centerY, maxRadius * 1.2);
      radialGrad.addColorStop(0, "rgba(245, 158, 11, 0.08)");
      radialGrad.addColorStop(0.5, "rgba(239, 68, 68, 0.04)");
      radialGrad.addColorStop(1, "rgba(5, 5, 10, 0)");
      ctx.fillStyle = radialGrad;
      ctx.fillRect(0, 0, width, height);

      rotationAngle += 0.002;

      // Draw 7 concentric rings + 1 center sanctum core
      // Ring radii from center outward:
      // Ring 8 (Core): radius 32
      // Ring 7: 62, Ring 6: 92, Ring 5: 122, Ring 4: 152, Ring 3: 182, Ring 2: 212, Ring 1: 242
      const ringRadii = {
        8: maxRadius * 0.16, // Core
        7: maxRadius * 0.28,
        6: maxRadius * 0.40,
        5: maxRadius * 0.52,
        4: maxRadius * 0.64,
        3: maxRadius * 0.76,
        2: maxRadius * 0.88,
        1: maxRadius * 1.00  // Outer
      };

      // Draw particle trails
      particles.forEach((p) => {
        p.angle += p.speed;
        p.radius -= 0.08;
        if (p.radius < 25) {
          p.radius = maxRadius * (0.85 + Math.random() * 0.15);
        }
        const px = centerX + Math.cos(p.angle) * p.radius;
        const py = centerY + Math.sin(p.angle) * p.radius;

        ctx.beginPath();
        ctx.arc(px, py, p.size, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.opacity;
        ctx.shadowBlur = 8;
        ctx.shadowColor = p.color;
        ctx.fill();
        ctx.shadowBlur = 0;
        ctx.globalAlpha = 1.0;
      });

      // Render rings from outer to inner
      const ringOrder = [1, 2, 3, 4, 5, 6, 7, 8];

      ringOrder.forEach((rId) => {
        const radius = ringRadii[rId];
        const isSelected = selectedRingId === rId;
        const isHovered = hoveredRingId === rId;
        const isSolved = solvedRings.includes(`FLAG_RING_${rId}`) || (rId === 8 && solvedRings.includes("FLAG_FINAL"));
        const ringDir = rId % 2 === 0 ? 1 : -1;
        const currentRot = rotationAngle * ringDir * (1 + (8 - rId) * 0.15);

        // Styling based on state
        let strokeColor = "rgba(100, 116, 139, 0.25)";
        let glowColor = "transparent";
        let lineWidth = 1.5;

        if (isSolved) {
          strokeColor = "rgba(16, 185, 129, 0.85)"; // Emerald solved
          glowColor = "#10b981";
          lineWidth = 2.5;
        } else if (isSelected) {
          strokeColor = "rgba(245, 158, 11, 0.95)"; // Amber selected
          glowColor = "#f59e0b";
          lineWidth = 3.0;
        } else if (isHovered) {
          strokeColor = "rgba(239, 68, 68, 0.85)"; // Crimson hovered
          glowColor = "#ef4444";
          lineWidth = 2.5;
        } else if (rId === 8) {
          strokeColor = "rgba(234, 179, 8, 0.7)";
          glowColor = "#eab308";
        }

        // Draw Main Circle
        ctx.save();
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
        ctx.strokeStyle = strokeColor;
        ctx.lineWidth = lineWidth;
        if (glowColor !== "transparent") {
          ctx.shadowBlur = 12;
          ctx.shadowColor = glowColor;
        }
        ctx.stroke();
        ctx.restore();

        // Draw Tactical Dashes / Spoke Teeth on each ring
        const segments = 12 + rId * 4;
        for (let i = 0; i < segments; i++) {
          const tickAngle = currentRot + (i * (Math.PI * 2 / segments));
          const tickLen = (i % 4 === 0) ? 6 : 3;
          const x1 = centerX + Math.cos(tickAngle) * (radius - tickLen);
          const y1 = centerY + Math.sin(tickAngle) * (radius - tickLen);
          const x2 = centerX + Math.cos(tickAngle) * (radius + tickLen);
          const y2 = centerY + Math.sin(tickAngle) * (radius + tickLen);

          ctx.beginPath();
          ctx.moveTo(x1, y1);
          ctx.lineTo(x2, y2);
          ctx.strokeStyle = (isSelected || isHovered) ? strokeColor : "rgba(148, 163, 184, 0.3)";
          ctx.lineWidth = (i % 4 === 0) ? 1.5 : 0.8;
          ctx.stroke();
        }

        // Draw Guardian Marker Nodes
        const nodeAngle = currentRot + (rId * 0.85);
        const nodeX = centerX + Math.cos(nodeAngle) * radius;
        const nodeY = centerY + Math.sin(nodeAngle) * radius;

        ctx.save();
        ctx.beginPath();
        ctx.arc(nodeX, nodeY, isSelected ? 6 : 4, 0, Math.PI * 2);
        ctx.fillStyle = isSolved ? "#10b981" : (isSelected ? "#f59e0b" : (isHovered ? "#ef4444" : "#94a3b8"));
        ctx.shadowBlur = 10;
        ctx.shadowColor = ctx.fillStyle;
        ctx.fill();
        ctx.restore();
      });

      // Draw Center Sanctum Symbol (Abhimanyu's Exit Core)
      const coreRadius = ringRadii[8];
      const isCoreSelected = selectedRingId === 8;

      ctx.save();
      ctx.beginPath();
      ctx.arc(centerX, centerY, coreRadius * 0.7, 0, Math.PI * 2);
      ctx.fillStyle = isCoreSelected ? "rgba(234, 179, 8, 0.3)" : "rgba(239, 68, 68, 0.2)";
      ctx.strokeStyle = isCoreSelected ? "#f59e0b" : "#ef4444";
      ctx.lineWidth = 2;
      ctx.shadowBlur = 15;
      ctx.shadowColor = ctx.strokeStyle;
      ctx.fill();
      ctx.stroke();

      // Core Sanskrit text or emblem
      ctx.font = `700 ${Math.max(10, Math.floor(coreRadius * 0.4))}px 'Rajdhani', sans-serif`;
      ctx.fillStyle = "#fbbf24";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText("CORE", centerX, centerY);
      ctx.restore();

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    window.addEventListener("resize", updateSize);
    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener("resize", updateSize);
    };
  }, [selectedRingId, hoveredRingId, solvedRings]);

  // Handle Mouse Hover & Click to identify Ring Hit
  const handleMouseMove = (e) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const dist = Math.sqrt((x - centerX) ** 2 + (y - centerY) ** 2);
    const maxRadius = Math.min(rect.width, rect.height) * 0.44;

    const ringRadii = [
      { id: 8, r: maxRadius * 0.16 },
      { id: 7, r: maxRadius * 0.28 },
      { id: 6, r: maxRadius * 0.40 },
      { id: 5, r: maxRadius * 0.52 },
      { id: 4, r: maxRadius * 0.64 },
      { id: 3, r: maxRadius * 0.76 },
      { id: 2, r: maxRadius * 0.88 },
      { id: 1, r: maxRadius * 1.00 }
    ];

    let found = null;
    for (let i = 0; i < ringRadii.length; i++) {
      const ring = ringRadii[i];
      if (Math.abs(dist - ring.r) < 18) {
        found = ring.id;
        break;
      }
    }
    // Check inside center core
    if (!found && dist <= maxRadius * 0.18) {
      found = 8;
    }

    setHoveredRingId(found);
  };

  const handleClick = () => {
    if (hoveredRingId) {
      onSelectRing(hoveredRingId);
    }
  };

  const hoveredRing = rings.find((r) => r.id === hoveredRingId);

  return (
    <div className="relative w-full h-[480px] lg:h-[580px] flex items-center justify-center select-none overflow-hidden rounded-2xl border border-amber-950/40 bg-neutral-950/90 shadow-2xl backdrop-blur-xl">
      <canvas
        ref={canvasRef}
        onMouseMove={handleMouseMove}
        onMouseLeave={() => setHoveredRingId(null)}
        onClick={handleClick}
        className="w-full h-full cursor-crosshair"
      />

      {/* Floating HUD Tooltip when hovering rings */}
      {hoveredRing && (
        <div className="absolute top-4 left-4 pointer-events-none z-10 px-4 py-2.5 rounded-xl border border-amber-500/40 bg-neutral-950/90 shadow-xl backdrop-blur-md transition-all">
          <div className="text-[10px] tracking-widest text-amber-500 font-tactical uppercase">
            {hoveredRing.sanskritTitle}
          </div>
          <div className="text-base font-bold text-white font-title flex items-center gap-2">
            <span>{hoveredRing.name}</span>
            <span className="text-xs px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-tactical">
              {hoveredRing.guardian}
            </span>
          </div>
          <div className="text-xs text-neutral-400 font-tactical mt-0.5">
            {hoveredRing.domain}
          </div>
        </div>
      )}

      {/* Tactical Canvas Controls Overlay */}
      <div className="absolute bottom-4 right-4 z-10 flex items-center gap-2 px-3 py-1.5 rounded-lg border border-neutral-800 bg-neutral-950/80 text-[11px] font-tactical text-neutral-400 backdrop-blur-sm">
        <span className="w-2 h-2 rounded-full bg-amber-500 animate-ping inline-block" />
        <span>TOPOLOGY MAP</span>
      </div>
    </div>
  );
}
