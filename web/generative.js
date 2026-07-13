(() => {
  const canvas2dEl = document.querySelector("#visualCanvas");
  const shaderCanvas = document.querySelector("#shaderCanvas");
  const overlayCanvas = document.querySelector("#overlayCanvas");
  let canvas = canvas2dEl;
  const overlay = document.querySelector("#debugOverlay");
  const debugPreset = document.querySelector("#debugPreset");
  const debugStatus = document.querySelector("#debugStatus");
  const debugFps = document.querySelector("#debugFps");
  const debugTrack = document.querySelector("#debugTrack");

  const embedMode = new URLSearchParams(window.location.search).get("embed") === "1";
  const starterOrder = ["lissajous_orbit", "moire_grid", "superformula_mandala", "particle_vortex", "shader_plasma", "harmonic_tunnel", "vector_field", "crystal_rings", "wave_ribbons", "starfield_gate", "kaleido_mesh", "liquid_topo", "pulse_bars", "constellation_web", "scanline_bloom", "orbital_dust"];
  const qualityScale = { low: 0.58, medium: 0.78, high: 1 };
  const state = {
    bpm: 120,
    beat: 0,
    beatPhase: 0,
    bar: 0,
    phrase: 0,
    energy: 0.55,
    primaryHue: 0.5,
    secondaryHue: 0.83,
    accentHue: 0.08,
    trackTitle: "",
    artist: "",
    activeLook: "",
    activeShowStep: "",
    deck: "",
    section: "",
    beatPulse: 0,
    preset: "lissajous_orbit",
    intensity: 0.7,
    complexity: 0.5,
    motion: 0.6,
    beatResponse: 0.5,
    scale: 0.54,
    zoom: 0.5,
    rotation: 0.42,
    symmetry: 0.5,
    warp: 0.38,
    lineWidth: 0.42,
    trail: 0.56,
    automationEnabled: false,
    automationTarget: "warp",
    automationMode: "bpm",
    automationDivision: "1 bar",
    automationShape: "sine",
    automationDepth: 0.35,
    automationOffset: 0.5,
    layerEnabled: true,
    layerStyle: "glow_grid",
    layerMix: 0.32,
    layerSpeed: 0.4,
    phraseMorph: true,
    colorSource: "look",
    enabled: true,
    quality: "medium",
    opacity: 1,
    freeze: false,
    blackout: false,
    seed: 1,
    renderer: "canvas2d",
  };

  let activePreset = null;
  let activePresetId = "";
  let activeRenderer = "";
  let ctx2d = null;
  let overlayCtx = overlayCanvas.getContext("2d", { alpha: true });
  let gl = null;
  let lastFrame = performance.now();
  let lastPoll = 0;
  let connected = false;
  let showOverlay = !embedMode;
  let forcedFreeze = false;
  let fps = 60;
  let lowFpsSince = 0;
  let time = 0;

  const clamp = (value, low = 0, high = 1) => Math.max(low, Math.min(high, Number(value) || 0));
  const divisionMultipliers = {
    "1/64": 4 / 64,
    "1/32": 4 / 32,
    "1/16": 4 / 16,
    "1/8": 4 / 8,
    "1/4": 1,
    "1/2 bar": 2,
    "1 bar": 4,
    "2 bars": 8,
    "4 bars": 16,
    "8 bars": 32,
    "16 bars": 64,
    "32 bars": 128,
  };
  const automationKey = (key) => (
    key === "line_width" ? "lineWidth" :
    key === "beat_response" ? "beatResponse" :
    key
  );
  const automationPhase = (s) => {
    if (s.automationMode === "seconds") return (time / Math.max(0.1, divisionMultipliers[s.automationDivision] || 4)) % 1;
    const beats = time * Math.max(1, s.bpm) / 60;
    return (beats / Math.max(0.0625, divisionMultipliers[s.automationDivision] || 4)) % 1;
  };
  const automationWave = (phase, shape) => {
    if (shape === "triangle") return phase < 0.5 ? phase * 2 : 2 - phase * 2;
    if (shape === "saw") return phase;
    if (shape === "pulse") return phase < 0.5 ? 1 : 0;
    return 0.5 + Math.sin(phase * Math.PI * 2) * 0.5;
  };
  const effectiveState = (raw) => {
    const s = { ...raw };
    if (!s.automationEnabled) return s;
    const key = automationKey(s.automationTarget);
    if (!(key in s)) return s;
    const wave = automationWave(automationPhase(s), s.automationShape);
    const center = clamp(s.automationOffset ?? s[key]);
    s[key] = clamp(center + (wave - 0.5) * 2 * clamp(s.automationDepth));
    return s;
  };
  const hsl = (hue, saturation = 85, light = 58, alpha = 1) => `hsla(${Math.round(((hue % 1) + 1) % 1 * 360)}, ${saturation}%, ${light}%, ${alpha})`;
  const trailAlpha = (s, base = 0.18) => Math.max(0.035, base * (1.25 - clamp(s.trail)));
  const lineScale = (s, c) => Math.max(1, c.width / 1500) * (0.7 + clamp(s.lineWidth) * 3.8);
  const clear = (ctx, alpha = 0.18) => {
    ctx.globalCompositeOperation = "source-over";
    ctx.fillStyle = `rgba(0, 0, 0, ${alpha})`;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  };
  const clearOverlay = () => {
    overlayCtx.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);
  };
  const drawLayerOverlay = (s) => {
    clearOverlay();
    if (!s.layerEnabled || s.layerStyle === "none") return;
    const c = overlayCanvas;
    const ctx = overlayCtx;
    const mix = clamp(s.layerMix ?? 0.32);
    const speed = 0.12 + clamp(s.layerSpeed ?? 0.4) * 0.9;
    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    if (s.layerStyle === "scanlines") {
      const spacing = Math.max(5, 22 - s.symmetry * 10);
      ctx.strokeStyle = hsl(s.secondaryHue, 86, 64, 0.08 + mix * 0.28);
      ctx.lineWidth = Math.max(1, c.width / 1500) * (0.7 + s.lineWidth * 1.2);
      for (let y = -spacing; y < c.height + spacing; y += spacing) {
        const wobble = Math.sin(y * 0.025 + time * speed * 2) * s.warp * 28;
        ctx.beginPath();
        ctx.moveTo(0, y + wobble);
        ctx.lineTo(c.width, y - wobble);
        ctx.stroke();
      }
    } else if (s.layerStyle === "vignette") {
      const grad = ctx.createRadialGradient(c.width / 2, c.height / 2, c.height * 0.1, c.width / 2, c.height / 2, Math.max(c.width, c.height) * (0.42 + s.zoom * 0.18));
      grad.addColorStop(0, hsl(s.accentHue, 88, 62, 0.04 + mix * 0.15));
      grad.addColorStop(0.58, "rgba(0,0,0,0)");
      grad.addColorStop(1, `rgba(0,0,0,${0.18 + mix * 0.52})`);
      ctx.globalCompositeOperation = "source-over";
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, c.width, c.height);
    } else if (s.layerStyle === "echo") {
      ctx.translate(c.width / 2, c.height / 2);
      ctx.rotate((s.rotation - 0.5) * Math.PI * 2 + time * speed * 0.18);
      const rings = 3 + Math.floor(s.symmetry * 7);
      for (let i = 1; i <= rings; i += 1) {
        ctx.strokeStyle = hsl(i % 2 ? s.primaryHue : s.accentHue, 86, 62, mix * (0.05 + i / rings * 0.1));
        ctx.lineWidth = lineScale(s, c) * (0.35 + i / rings);
        ctx.beginPath();
        ctx.ellipse(0, 0, c.width * (0.08 + i * 0.055 + s.scale * 0.04), c.height * (0.05 + i * 0.035 + s.zoom * 0.035), 0, 0, Math.PI * 2);
        ctx.stroke();
      }
    } else if (s.layerStyle === "sparkle") {
      const count = 24 + Math.floor(s.complexity * 100);
      ctx.fillStyle = hsl(s.accentHue, 90, 68, 0.18 + mix * 0.45);
      for (let i = 0; i < count; i += 1) {
        const seed = Math.sin(i * 12.9898) * 43758.5453;
        const x = (((seed % 1) + 1) % 1) * c.width;
        const y = ((((seed * 1.37) % 1) + 1) % 1) * c.height;
        const pulse = 0.5 + Math.sin(time * speed * 5 + i) * 0.5;
        const size = (0.6 + s.lineWidth * 2.4) * (0.4 + pulse);
        ctx.fillRect(x, y, size, size);
      }
    } else {
      const spacing = Math.max(22, 72 - s.scale * 36);
      ctx.translate(c.width / 2, c.height / 2);
      ctx.rotate((s.rotation - 0.5) * 0.8 + time * speed * 0.12);
      ctx.strokeStyle = hsl(s.secondaryHue, 86, 62, 0.06 + mix * 0.18);
      ctx.lineWidth = lineScale(s, c) * 0.32;
      for (let x = -c.width; x <= c.width; x += spacing) {
        ctx.beginPath();
        ctx.moveTo(x, -c.height);
        ctx.lineTo(x + Math.sin(time + x * 0.01) * s.warp * 80, c.height);
        ctx.stroke();
      }
      ctx.strokeStyle = hsl(s.accentHue, 90, 64, 0.04 + mix * 0.16);
      for (let y = -c.height; y <= c.height; y += spacing) {
        ctx.beginPath();
        ctx.moveTo(-c.width, y);
        ctx.lineTo(c.width, y + Math.cos(time + y * 0.01) * s.warp * 80);
        ctx.stroke();
      }
    }
    ctx.restore();
  };
  const seeded = (seed) => {
    let value = (seed || 1) % 2147483647;
    return () => {
      value = (value * 16807) % 2147483647;
      return (value - 1) / 2147483646;
    };
  };

  function resize() {
    const scale = qualityScale[state.quality] || qualityScale.medium;
    const width = Math.max(320, Math.floor(window.innerWidth * devicePixelRatio * scale));
    const height = Math.max(180, Math.floor(window.innerHeight * devicePixelRatio * scale));
    if (canvas.width !== width || canvas.height !== height) {
      canvas.width = width;
      canvas.height = height;
      if (activePreset?.resize) activePreset.resize(canvas, state);
    }
    if (overlayCanvas.width !== width || overlayCanvas.height !== height) {
      overlayCanvas.width = width;
      overlayCanvas.height = height;
    }
    for (const other of [canvas2dEl, shaderCanvas]) {
      if (other !== canvas) {
        other.width = width;
        other.height = height;
      }
    }
  }

  const presets = {
    lissajous_orbit: {
      renderer: "canvas2d",
      init() {},
      update() {},
      draw(ctx, c, s) {
        clear(ctx, trailAlpha(s, 0.2));
        const cx = c.width / 2;
        const cy = c.height / 2;
        const radius = Math.min(c.width, c.height) * (0.12 + s.scale * 0.22 + s.zoom * 0.16 + s.intensity * 0.14 + s.beatPulse * s.beatResponse * 0.06);
        const density = Math.floor(380 + s.complexity * 900);
        const symmetry = Math.max(1, Math.floor(2 + s.symmetry * 8));
        const ax = 2 + Math.floor(s.complexity * 5) + (symmetry % 3);
        const ay = 3 + ((s.phrase || 0) % 5) + (symmetry % 4);
        ctx.save();
        ctx.globalCompositeOperation = "lighter";
        ctx.lineWidth = lineScale(s, c);
        ctx.translate(cx, cy);
        ctx.rotate((s.rotation - 0.5) * Math.PI * 2 + time * s.rotation * 0.12);
        for (let layer = 0; layer < 3; layer += 1) {
          ctx.beginPath();
          const phase = time * (0.2 + s.motion * 0.75) + layer * 0.72;
          for (let i = 0; i <= density; i += 1) {
            const t = (i / density) * Math.PI * 2;
            const warp = Math.sin(t * symmetry + time * (0.5 + s.motion)) * s.warp * radius * 0.18;
            const x = Math.sin(ax * t + phase) * (radius + warp) * (1 + layer * 0.08);
            const y = Math.cos(ay * t - phase * 0.8) * (radius - warp * 0.4) * (0.72 + layer * 0.12);
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
          }
          ctx.strokeStyle = hsl(layer === 1 ? s.secondaryHue : s.primaryHue, 88, 58 + layer * 8, 0.26 + s.energy * 0.3);
          ctx.shadowColor = hsl(layer === 2 ? s.accentHue : s.primaryHue, 90, 60, 0.5);
          ctx.shadowBlur = 24 + s.intensity * 28;
          ctx.stroke();
        }
        ctx.restore();
      },
    },
    moire_grid: {
      renderer: "canvas2d",
      draw(ctx, c, s) {
        clear(ctx, trailAlpha(s, 0.12));
        const spacing = Math.max(10, 72 - s.complexity * 38 - s.scale * 24 - s.beatPulse * s.beatResponse * 10);
        const layers = 3 + Math.floor(s.symmetry * 5);
        ctx.save();
        ctx.translate(c.width / 2, c.height / 2);
        ctx.scale(0.8 + s.zoom * 0.6, 0.8 + s.zoom * 0.6);
        ctx.globalCompositeOperation = "lighter";
        for (let layer = 0; layer < layers; layer += 1) {
          ctx.save();
          const direction = s.phraseMorph && s.phrase % 2 ? -1 : 1;
          ctx.rotate(direction * time * (0.035 + s.motion * 0.14) + layer * Math.PI / (5 + s.symmetry * 8) + (s.rotation - 0.5) * Math.PI);
          ctx.strokeStyle = hsl(layer % 2 ? s.secondaryHue : s.primaryHue, 78, 54 + layer * 4, 0.12 + s.intensity * 0.22);
          ctx.lineWidth = lineScale(s, c) * (0.55 + s.beatPulse * s.beatResponse * 0.8);
          for (let x = -c.width; x <= c.width; x += spacing) {
            ctx.beginPath();
            const wobble = Math.sin(x * 0.01 + time) * s.warp * 80;
            ctx.moveTo(x + wobble, -c.height);
            ctx.lineTo(x - wobble, c.height);
            ctx.stroke();
          }
          ctx.restore();
        }
        ctx.restore();
      },
    },
    superformula_mandala: {
      renderer: "canvas2d",
      draw(ctx, c, s) {
        clear(ctx, trailAlpha(s, 0.18));
        const cx = c.width / 2;
        const cy = c.height / 2;
        const base = Math.min(c.width, c.height) * (0.12 + s.scale * 0.18 + s.zoom * 0.14 + s.intensity * 0.08);
        const lobes = 3 + Math.floor(s.symmetry * 11) + ((s.phraseMorph ? s.phrase : 0) % 4) + Math.floor(s.complexity * 4);
        const points = 760;
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(time * (0.05 + s.motion * 0.18) + (s.rotation - 0.5) * Math.PI * 2);
        ctx.globalCompositeOperation = "lighter";
        for (let ring = 0; ring < 4; ring += 1) {
          ctx.beginPath();
          for (let i = 0; i <= points; i += 1) {
            const theta = (i / points) * Math.PI * 2;
            const wave = Math.pow(Math.abs(Math.cos(lobes * theta / 4)), 0.8 + s.warp * 0.8) + Math.pow(Math.abs(Math.sin(lobes * theta / 4)), 1.2 + s.warp);
            const r = base * (0.62 + ring * 0.18) * (1 + s.energy * 0.24 * Math.sin(lobes * theta + time)) / Math.max(0.3, wave);
            const pulse = 1 + s.beatPulse * s.beatResponse * 0.08;
            const x = Math.cos(theta) * r * pulse;
            const y = Math.sin(theta) * r * pulse;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
          }
          ctx.strokeStyle = hsl(ring % 2 ? s.primaryHue : s.accentHue, 86, 58 + ring * 5, 0.18 + s.intensity * 0.18);
          ctx.lineWidth = lineScale(s, c) * (0.62 + ring * 0.18);
          ctx.shadowColor = hsl(s.accentHue, 90, 62, 0.7);
          ctx.shadowBlur = 14 + s.intensity * 26;
          ctx.stroke();
        }
        ctx.restore();
      },
    },
    particle_vortex: {
      renderer: "canvas2d",
      init(_ctx, c, s) {
        this.seed = s.seed;
        this.build(c, s);
      },
      build(c, s) {
        const random = seeded(s.seed);
        const count = Math.floor((s.quality === "high" ? 1800 : s.quality === "low" ? 520 : 1050) * (0.55 + s.complexity));
        this.particles = Array.from({ length: count }, () => ({
          x: (random() - 0.5) * c.width,
          y: (random() - 0.5) * c.height,
          v: 0.4 + random() * 1.6,
        }));
      },
      update(_dt, s) {
        if (this.seed !== s.seed || !this.particles) {
          this.seed = s.seed;
          this.build(canvas, s);
        }
      },
      draw(ctx, c, s) {
        clear(ctx, trailAlpha(s, 0.1));
        ctx.save();
        ctx.translate(c.width / 2, c.height / 2);
        ctx.rotate((s.rotation - 0.5) * Math.PI * 2 + time * s.rotation * 0.08);
        ctx.scale(0.75 + s.zoom * 0.65, 0.75 + s.zoom * 0.65);
        ctx.globalCompositeOperation = "lighter";
        ctx.fillStyle = hsl(s.primaryHue, 88, 62, 0.34 + s.intensity * 0.24);
        const force = 0.4 + s.motion * 2.2 + s.beatPulse * s.beatResponse * 7;
        const limit = Math.max(c.width, c.height) * (0.35 + s.scale * 0.55);
        for (const p of this.particles || []) {
          const angle = Math.atan2(p.y, p.x);
          const radius = Math.hypot(p.x, p.y) || 1;
          const curl = Math.sin(radius * (0.006 + s.warp * 0.018) + time * 0.8) * (0.25 + s.warp * 1.1);
          p.x += Math.cos(angle + Math.PI / 2 + curl) * p.v * force + Math.cos(angle) * s.beatPulse * s.beatResponse * 3;
          p.y += Math.sin(angle + Math.PI / 2 + curl) * p.v * force + Math.sin(angle) * s.beatPulse * s.beatResponse * 3;
          if (Math.hypot(p.x, p.y) > limit) {
            p.x *= -0.12;
            p.y *= -0.12;
          }
          const size = 0.8 + s.lineWidth * 2.4 + s.beatPulse * s.beatResponse * 1.2;
          ctx.fillRect(p.x, p.y, size, size);
        }
        ctx.restore();
      },
    },
    harmonic_tunnel: {
      renderer: "canvas2d",
      draw(ctx, c, s) {
        clear(ctx, trailAlpha(s, 0.16));
        const cx = c.width / 2;
        const cy = c.height / 2;
        const ringCount = 10 + Math.floor(s.complexity * 28);
        const base = Math.min(c.width, c.height) * (0.04 + s.scale * 0.05);
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate((s.rotation - 0.5) * Math.PI * 2 + time * (0.03 + s.motion * 0.12));
        ctx.globalCompositeOperation = "lighter";
        for (let i = ringCount; i >= 0; i -= 1) {
          const depth = i / ringCount;
          const pulse = 1 + s.beatPulse * s.beatResponse * (0.18 + depth * 0.28);
          const radius = base + depth * Math.min(c.width, c.height) * (0.22 + s.zoom * 0.46) * pulse;
          const sides = 5 + Math.floor(s.symmetry * 10);
          ctx.beginPath();
          for (let p = 0; p <= sides; p += 1) {
            const a = (p / sides) * Math.PI * 2 + Math.sin(time + i * 0.4) * s.warp * 0.4;
            const wobble = 1 + Math.sin(a * (2 + s.complexity * 6) + time * (0.8 + s.motion)) * s.warp * 0.12;
            const x = Math.cos(a) * radius * wobble;
            const y = Math.sin(a) * radius * wobble;
            if (p === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
          }
          ctx.strokeStyle = hsl(i % 3 === 0 ? s.accentHue : i % 2 ? s.secondaryHue : s.primaryHue, 86, 52 + depth * 22, 0.08 + s.intensity * 0.22);
          ctx.lineWidth = lineScale(s, c) * (0.45 + depth * 0.9);
          ctx.shadowColor = hsl(s.accentHue, 90, 64, 0.45);
          ctx.shadowBlur = 10 + s.intensity * 24;
          ctx.stroke();
        }
        ctx.restore();
      },
    },
    vector_field: {
      renderer: "canvas2d",
      draw(ctx, c, s) {
        clear(ctx, trailAlpha(s, 0.13));
        const cols = 16 + Math.floor(s.complexity * 30);
        const rows = Math.max(8, Math.floor(cols * c.height / c.width));
        const stepX = c.width / cols;
        const stepY = c.height / rows;
        const length = Math.min(stepX, stepY) * (0.6 + s.scale * 1.3 + s.beatPulse * s.beatResponse);
        ctx.save();
        ctx.globalCompositeOperation = "lighter";
        ctx.lineWidth = lineScale(s, c) * 0.62;
        for (let y = 0; y <= rows; y += 1) {
          for (let x = 0; x <= cols; x += 1) {
            const px = x * stepX;
            const py = y * stepY;
            const nx = (px / c.width - 0.5) * (2.2 - s.zoom);
            const ny = (py / c.height - 0.5) * (2.2 - s.zoom);
            const angle = Math.sin(nx * (3 + s.complexity * 8) + time * s.motion) + Math.cos(ny * (4 + s.symmetry * 8) - time * (0.4 + s.motion)) + s.rotation * Math.PI * 2;
            const bend = Math.sin((nx * nx + ny * ny) * 8 + time) * s.warp;
            ctx.beginPath();
            ctx.moveTo(px - Math.cos(angle + bend) * length * 0.45, py - Math.sin(angle - bend) * length * 0.45);
            ctx.lineTo(px + Math.cos(angle + bend) * length, py + Math.sin(angle - bend) * length);
            ctx.strokeStyle = hsl((x + y) % 3 === 0 ? s.accentHue : x % 2 ? s.secondaryHue : s.primaryHue, 82, 58, 0.14 + s.intensity * 0.25);
            ctx.stroke();
          }
        }
        ctx.restore();
      },
    },
    crystal_rings: {
      renderer: "canvas2d",
      draw(ctx, c, s) {
        clear(ctx, trailAlpha(s, 0.17));
        const cx = c.width / 2;
        const cy = c.height / 2;
        const facets = 6 + Math.floor(s.symmetry * 18);
        const rings = 3 + Math.floor(s.complexity * 7);
        const maxRadius = Math.min(c.width, c.height) * (0.16 + s.zoom * 0.34 + s.scale * 0.12);
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate((s.rotation - 0.5) * Math.PI * 2 + time * (0.02 + s.motion * 0.07));
        ctx.globalCompositeOperation = "lighter";
        for (let r = 1; r <= rings; r += 1) {
          const radius = (r / rings) * maxRadius * (1 + s.beatPulse * s.beatResponse * 0.1);
          ctx.beginPath();
          for (let f = 0; f <= facets; f += 1) {
            const a = (f / facets) * Math.PI * 2;
            const facetWarp = 1 + Math.sin(a * facets * 0.5 + time + r) * s.warp * 0.14;
            const x = Math.cos(a) * radius * facetWarp;
            const y = Math.sin(a) * radius * facetWarp;
            if (f === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
          }
          ctx.strokeStyle = hsl(r % 3 === 0 ? s.accentHue : r % 2 ? s.primaryHue : s.secondaryHue, 88, 56 + r * 3, 0.16 + s.intensity * 0.22);
          ctx.lineWidth = lineScale(s, c) * (0.45 + r / rings);
          ctx.stroke();
        }
        for (let f = 0; f < facets; f += 1) {
          const a = (f / facets) * Math.PI * 2 + Math.sin(time * 0.4) * s.warp * 0.2;
          ctx.beginPath();
          ctx.moveTo(Math.cos(a) * maxRadius * 0.12, Math.sin(a) * maxRadius * 0.12);
          ctx.lineTo(Math.cos(a) * maxRadius, Math.sin(a) * maxRadius);
          ctx.strokeStyle = hsl(f % 2 ? s.secondaryHue : s.accentHue, 86, 62, 0.06 + s.intensity * 0.18);
          ctx.lineWidth = lineScale(s, c) * 0.42;
          ctx.stroke();
        }
        ctx.restore();
      },
    },
    wave_ribbons: {
      renderer: "canvas2d",
      draw(ctx, c, s) {
        clear(ctx, trailAlpha(s, 0.14));
        const bands = 5 + Math.floor(s.complexity * 8);
        const amp = c.height * (0.04 + s.warp * 0.12 + s.beatPulse * s.beatResponse * 0.03);
        ctx.save();
        ctx.globalCompositeOperation = "lighter";
        ctx.translate(c.width / 2, c.height * (0.1 + s.zoom * 0.18));
        ctx.rotate((s.rotation - 0.5) * 0.38);
        ctx.translate(-c.width / 2, 0);
        for (let band = 0; band < bands; band += 1) {
          ctx.beginPath();
          const yBase = (band + 0.5) * (c.height * 0.8 / bands);
          for (let x = -20; x <= c.width + 20; x += 8) {
            const y = yBase + Math.sin(x * (0.006 + s.complexity * 0.012) + time * (0.5 + s.motion) + band) * amp;
            const braid = Math.cos(x * 0.01 + time * 0.7 + band) * amp * s.symmetry * 0.35;
            if (x === -20) ctx.moveTo(x, y + braid);
            else ctx.lineTo(x, y + braid);
          }
          ctx.strokeStyle = hsl(band % 3 === 0 ? s.accentHue : band % 2 ? s.secondaryHue : s.primaryHue, 84, 58, 0.13 + s.intensity * 0.18);
          ctx.lineWidth = lineScale(s, c) * (0.8 + band / bands);
          ctx.shadowColor = hsl(s.accentHue, 90, 62, 0.35);
          ctx.shadowBlur = 12 + s.intensity * 20;
          ctx.stroke();
        }
        ctx.restore();
      },
    },
    starfield_gate: {
      renderer: "canvas2d",
      draw(ctx, c, s) {
        clear(ctx, trailAlpha(s, 0.2));
        const cx = c.width / 2;
        const cy = c.height / 2;
        const count = 90 + Math.floor(s.complexity * 220);
        ctx.save();
        ctx.globalCompositeOperation = "lighter";
        for (let i = 0; i < count; i += 1) {
          const seed = i * 12.9898;
          const lane = ((Math.sin(seed) * 43758.5453) % 1 + 1) % 1;
          const drift = (time * (0.08 + s.motion * 0.35) + lane) % 1;
          const angle = i * 2.399 + (s.rotation - 0.5) * Math.PI * 2;
          const depth = Math.pow(drift, 1.7);
          const radius = depth * Math.max(c.width, c.height) * (0.15 + s.zoom * 0.55);
          const x = cx + Math.cos(angle) * radius * (1 + s.warp * Math.sin(time + i));
          const y = cy + Math.sin(angle) * radius * (0.62 + s.scale * 0.38);
          const size = 0.8 + depth * 3.2 + s.beatPulse * s.beatResponse * 2;
          ctx.fillStyle = hsl(i % 3 === 0 ? s.accentHue : i % 2 ? s.secondaryHue : s.primaryHue, 86, 66, 0.24 + depth * 0.55);
          ctx.fillRect(x, y, size, size);
        }
        const sides = 4 + Math.floor(s.symmetry * 6);
        ctx.translate(cx, cy);
        ctx.rotate(time * (0.05 + s.motion * 0.1) + s.rotation * Math.PI * 2);
        for (let r = 1; r <= 4; r += 1) {
          ctx.beginPath();
          const radius = Math.min(c.width, c.height) * (0.08 + r * 0.075 + s.zoom * 0.04);
          for (let p = 0; p <= sides; p += 1) {
            const a = (p / sides) * Math.PI * 2;
            const x = Math.cos(a) * radius;
            const y = Math.sin(a) * radius;
            if (!p) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
          }
          ctx.strokeStyle = hsl(r % 2 ? s.primaryHue : s.accentHue, 84, 58, 0.16 + s.intensity * 0.16);
          ctx.lineWidth = lineScale(s, c) * 0.7;
          ctx.stroke();
        }
        ctx.restore();
      },
    },
    kaleido_mesh: {
      renderer: "canvas2d",
      draw(ctx, c, s) {
        clear(ctx, trailAlpha(s, 0.18));
        const cx = c.width / 2;
        const cy = c.height / 2;
        const spokes = 6 + Math.floor(s.symmetry * 18);
        const rings = 3 + Math.floor(s.complexity * 6);
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(time * (0.04 + s.motion * 0.12) + s.rotation * Math.PI * 2);
        ctx.scale(0.75 + s.zoom * 0.6, 0.75 + s.zoom * 0.6);
        ctx.globalCompositeOperation = "lighter";
        for (let r = 1; r <= rings; r += 1) {
          const radius = Math.min(c.width, c.height) * (0.045 + r * 0.045 + s.scale * 0.05);
          for (let spoke = 0; spoke < spokes; spoke += 1) {
            const a1 = (spoke / spokes) * Math.PI * 2;
            const a2 = ((spoke + 1) / spokes) * Math.PI * 2;
            ctx.beginPath();
            ctx.moveTo(Math.cos(a1) * radius, Math.sin(a1) * radius);
            ctx.lineTo(Math.cos(a2) * radius * (1 + s.warp * 0.22), Math.sin(a2) * radius * (1 - s.warp * 0.12));
            ctx.lineTo(Math.cos(a1) * radius * 0.58, Math.sin(a1) * radius * 0.58);
            ctx.closePath();
            ctx.fillStyle = hsl(spoke % 3 === 0 ? s.accentHue : spoke % 2 ? s.secondaryHue : s.primaryHue, 88, 56 + r * 3, 0.035 + s.intensity * 0.08 + s.beatPulse * s.beatResponse * 0.08);
            ctx.strokeStyle = hsl(spoke % 2 ? s.primaryHue : s.accentHue, 88, 62, 0.08 + s.intensity * 0.14);
            ctx.lineWidth = lineScale(s, c) * 0.38;
            ctx.fill();
            ctx.stroke();
          }
        }
        ctx.restore();
      },
    },
    liquid_topo: {
      renderer: "canvas2d",
      draw(ctx, c, s) {
        clear(ctx, trailAlpha(s, 0.12));
        const lines = 8 + Math.floor(s.complexity * 18);
        ctx.save();
        ctx.translate(c.width / 2, c.height / 2);
        ctx.rotate((s.rotation - 0.5) * 0.42);
        ctx.scale(0.82 + s.zoom * 0.36, 0.82 + s.zoom * 0.36);
        ctx.translate(-c.width / 2, -c.height / 2);
        ctx.globalCompositeOperation = "lighter";
        for (let line = 0; line < lines; line += 1) {
          ctx.beginPath();
          const yBase = (line + 0.5) * c.height / lines;
          for (let x = -10; x <= c.width + 10; x += 7) {
            const nx = (x / c.width - 0.5) * (2 + s.zoom);
            const wave = Math.sin(nx * (4 + s.symmetry * 8) + time * (0.25 + s.motion) + line * 0.62);
            const detail = Math.sin(nx * (10 + s.complexity * 20) - time * 0.45 + line) * s.warp;
            const y = yBase + (wave + detail) * c.height * (0.018 + s.scale * 0.035) * (1 + s.beatPulse * s.beatResponse * 0.4);
            if (x === -10) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
          }
          ctx.strokeStyle = hsl(line % 3 === 0 ? s.accentHue : line % 2 ? s.primaryHue : s.secondaryHue, 76, 58, 0.1 + s.intensity * 0.2);
          ctx.lineWidth = lineScale(s, c) * 0.58;
          ctx.stroke();
        }
        ctx.restore();
      },
    },
    pulse_bars: {
      renderer: "canvas2d",
      draw(ctx, c, s) {
        clear(ctx, trailAlpha(s, 0.24));
        const bars = 8 + Math.floor(s.complexity * 24);
        const gap = c.width / bars;
        ctx.save();
        ctx.translate(c.width / 2, c.height / 2);
        ctx.rotate((s.rotation - 0.5) * 0.45);
        ctx.translate(-c.width / 2, -c.height / 2);
        ctx.globalCompositeOperation = "lighter";
        for (let i = 0; i < bars; i += 1) {
          const phase = i / bars;
          const wave = 0.5 + Math.sin(time * (1 + s.motion * 3) + i * (0.6 + s.symmetry)) * 0.5;
          const pulse = s.beatPulse * s.beatResponse;
          const height = c.height * (0.12 + wave * (0.2 + s.scale * 0.34) + pulse * 0.28);
          const x = i * gap + gap * 0.16;
          const y = c.height / 2 - height / 2 + Math.sin(i + time) * s.warp * 18;
          const width = Math.max(3, gap * (0.32 + s.zoom * 0.38));
          ctx.fillStyle = hsl(i % 3 === 0 ? s.accentHue : i % 2 ? s.primaryHue : s.secondaryHue, 88, 58, 0.16 + s.intensity * 0.38);
          ctx.shadowColor = hsl(s.accentHue, 90, 62, 0.5);
          ctx.shadowBlur = 14 + pulse * 20;
          ctx.fillRect(x, y, width, height);
          ctx.strokeStyle = hsl(i % 2 ? s.secondaryHue : s.primaryHue, 82, 70, 0.12 + s.intensity * 0.16);
          ctx.lineWidth = lineScale(s, c) * 0.45;
          ctx.strokeRect(x, y, width, height);
        }
        ctx.restore();
      },
    },
    constellation_web: {
      renderer: "canvas2d",
      draw(ctx, c, s) {
        clear(ctx, trailAlpha(s, 0.16));
        const count = 24 + Math.floor(s.complexity * 80);
        const points = [];
        for (let i = 0; i < count; i += 1) {
          const a = i * 2.399 + time * (0.04 + s.motion * 0.1) + s.rotation * Math.PI * 2;
          const r = Math.sqrt(i / count) * Math.min(c.width, c.height) * (0.18 + s.zoom * 0.38);
          points.push({
            x: c.width / 2 + Math.cos(a) * r * (1 + s.warp * Math.sin(time + i)),
            y: c.height / 2 + Math.sin(a) * r * (0.72 + s.scale * 0.34),
          });
        }
        ctx.save();
        ctx.globalCompositeOperation = "lighter";
        const threshold = Math.min(c.width, c.height) * (0.08 + s.symmetry * 0.12);
        for (let i = 0; i < points.length; i += 1) {
          for (let j = i + 1; j < Math.min(points.length, i + 8); j += 1) {
            const dx = points[i].x - points[j].x;
            const dy = points[i].y - points[j].y;
            const d = Math.hypot(dx, dy);
            if (d > threshold) continue;
            ctx.strokeStyle = hsl(i % 2 ? s.secondaryHue : s.primaryHue, 82, 60, (1 - d / threshold) * (0.06 + s.intensity * 0.18));
            ctx.lineWidth = lineScale(s, c) * 0.28;
            ctx.beginPath();
            ctx.moveTo(points[i].x, points[i].y);
            ctx.lineTo(points[j].x, points[j].y);
            ctx.stroke();
          }
        }
        for (let i = 0; i < points.length; i += 1) {
          ctx.fillStyle = hsl(i % 3 === 0 ? s.accentHue : s.primaryHue, 88, 66, 0.32 + s.intensity * 0.34);
          ctx.beginPath();
          ctx.arc(points[i].x, points[i].y, 1.4 + s.beatPulse * s.beatResponse * 2.8, 0, Math.PI * 2);
          ctx.fill();
        }
        ctx.restore();
      },
    },
    scanline_bloom: {
      renderer: "canvas2d",
      draw(ctx, c, s) {
        clear(ctx, trailAlpha(s, 0.18));
        ctx.save();
        ctx.translate(c.width / 2, c.height / 2);
        ctx.rotate((s.rotation - 0.5) * 0.35);
        ctx.scale(0.82 + s.scale * 0.22, 0.82 + s.scale * 0.22);
        ctx.translate(-c.width / 2, -c.height / 2);
        ctx.globalCompositeOperation = "lighter";
        const grad = ctx.createRadialGradient(c.width / 2, c.height / 2, 0, c.width / 2, c.height / 2, Math.max(c.width, c.height) * (0.18 + s.scale * 0.12 + s.zoom * 0.45));
        grad.addColorStop(0, hsl(s.accentHue, 90, 62, 0.18 + s.intensity * 0.34 + s.beatPulse * s.beatResponse * 0.2));
        grad.addColorStop(0.45, hsl(s.primaryHue, 86, 54, 0.08 + s.intensity * 0.18));
        grad.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, c.width, c.height);
        const spacing = Math.max(5, 28 - s.complexity * 13 - s.symmetry * 7);
        for (let y = -spacing; y < c.height + spacing; y += spacing) {
          const wobble = Math.sin(y * 0.02 + time * (0.8 + s.motion)) * s.warp * 35;
          ctx.strokeStyle = hsl(y % 2 ? s.secondaryHue : s.primaryHue, 82, 60, 0.08 + s.intensity * 0.16);
          ctx.lineWidth = lineScale(s, c) * (0.32 + s.lineWidth * 0.34);
          ctx.beginPath();
          ctx.moveTo(0, y + wobble);
          ctx.lineTo(c.width, y - wobble);
          ctx.stroke();
        }
        ctx.restore();
      },
    },
    orbital_dust: {
      renderer: "canvas2d",
      draw(ctx, c, s) {
        clear(ctx, trailAlpha(s, 0.08));
        const count = 320 + Math.floor(s.complexity * 850);
        ctx.save();
        ctx.translate(c.width / 2, c.height / 2);
        ctx.rotate(s.rotation * Math.PI * 2 + time * (0.03 + s.motion * 0.08));
        ctx.scale(0.76 + s.zoom * 0.58, 0.76 + s.zoom * 0.58);
        ctx.globalCompositeOperation = "lighter";
        for (let i = 0; i < count; i += 1) {
          const lane = 1 + (i % (3 + Math.floor(s.symmetry * 8)));
          const a = i * 0.37 + time * (0.1 + s.motion * 0.35) / lane;
          const r = Math.min(c.width, c.height) * (0.04 + lane * 0.018 + s.scale * 0.14) + Math.sin(i + time) * s.warp * 18;
          const x = Math.cos(a) * r * (1.2 + lane * 0.04);
          const y = Math.sin(a) * r * (0.48 + lane * 0.025);
          ctx.fillStyle = hsl(i % 3 === 0 ? s.accentHue : i % 2 ? s.secondaryHue : s.primaryHue, 86, 64, 0.12 + s.intensity * 0.24);
          const size = 0.7 + s.lineWidth * 2.2 + s.beatPulse * s.beatResponse * 1.4;
          ctx.fillRect(x, y, size, size);
        }
        ctx.restore();
      },
    },
    shader_plasma: {
      renderer: "webgl-shader",
      init(glCtx) {
        const vertex = "attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}";
        const fragment = `precision mediump float;uniform vec2 r;uniform float t,bpm,e,pulse,ph,sh,ah,complexity,intensity,zoom,warp,rotation,scale,symmetry,lineWidth,trail;vec3 hue(float h){return .55+.45*cos(6.28318*(vec3(.0,.33,.67)+h));}void main(){vec2 uv=(gl_FragCoord.xy*2.-r)/min(r.x,r.y);float a=rotation*6.28318+t*.04;uv=mat2(cos(a),-sin(a),sin(a),cos(a))*uv*(1.45-zoom*.72);float ang=atan(uv.y,uv.x);float rad=length(uv);float spokes=sin(ang*(3.+symmetry*14.)+t*(.2+rotation));float v=0.;for(int i=0;i<6;i++){float fi=float(i)+1.;vec2 q=uv+sin(vec2(uv.y,uv.x)*fi+t*.2)*warp*.35;v+=sin((q.x*cos(t*.08+fi)+q.y*sin(t*.07-fi))*fi*(1.8+complexity*5.5+scale*2.)+t*(.4+e)+pulse*2.);}v=(v/6.)+spokes*warp*.22;float edge=smoothstep(.12+lineWidth*.34,.9,v*.5+.5);vec3 aa=hue(ph),b=hue(sh),c=hue(ah);vec3 col=mix(aa,b,.5+.5*sin(v*3.14+t*.2));col+=c*(pow(max(0.,v),2.)*(.3+pulse*.4+warp*.24)+edge*(.15+trail*.35));col*=1.+(trail*.35)/(1.+rad*rad*2.);gl_FragColor=vec4(col*intensity,1.);}`;
        const compile = (type, src) => {
          const shader = glCtx.createShader(type);
          glCtx.shaderSource(shader, src);
          glCtx.compileShader(shader);
          if (!glCtx.getShaderParameter(shader, glCtx.COMPILE_STATUS)) throw new Error(glCtx.getShaderInfoLog(shader));
          return shader;
        };
        const program = glCtx.createProgram();
        glCtx.attachShader(program, compile(glCtx.VERTEX_SHADER, vertex));
        glCtx.attachShader(program, compile(glCtx.FRAGMENT_SHADER, fragment));
        glCtx.linkProgram(program);
        if (!glCtx.getProgramParameter(program, glCtx.LINK_STATUS)) throw new Error(glCtx.getProgramInfoLog(program));
        const buffer = glCtx.createBuffer();
        glCtx.bindBuffer(glCtx.ARRAY_BUFFER, buffer);
        glCtx.bufferData(glCtx.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), glCtx.STATIC_DRAW);
        this.program = program;
        this.locations = Object.fromEntries(["r", "t", "bpm", "e", "pulse", "ph", "sh", "ah", "complexity", "intensity", "zoom", "warp", "rotation", "scale", "symmetry", "lineWidth", "trail"].map((name) => [name, glCtx.getUniformLocation(program, name)]));
        this.position = glCtx.getAttribLocation(program, "p");
      },
      draw(glCtx, c, s) {
        glCtx.viewport(0, 0, c.width, c.height);
        glCtx.useProgram(this.program);
        glCtx.enableVertexAttribArray(this.position);
        glCtx.vertexAttribPointer(this.position, 2, glCtx.FLOAT, false, 0, 0);
        glCtx.uniform2f(this.locations.r, c.width, c.height);
        glCtx.uniform1f(this.locations.t, time);
        glCtx.uniform1f(this.locations.bpm, s.bpm);
        glCtx.uniform1f(this.locations.e, s.energy);
        glCtx.uniform1f(this.locations.pulse, s.beatPulse * s.beatResponse);
        glCtx.uniform1f(this.locations.ph, s.primaryHue);
        glCtx.uniform1f(this.locations.sh, s.secondaryHue);
        glCtx.uniform1f(this.locations.ah, s.accentHue);
        glCtx.uniform1f(this.locations.complexity, s.complexity);
        glCtx.uniform1f(this.locations.intensity, s.intensity);
        glCtx.uniform1f(this.locations.zoom, s.zoom);
        glCtx.uniform1f(this.locations.warp, s.warp);
        glCtx.uniform1f(this.locations.rotation, s.rotation);
        glCtx.uniform1f(this.locations.scale, s.scale);
        glCtx.uniform1f(this.locations.symmetry, s.symmetry);
        glCtx.uniform1f(this.locations.lineWidth, s.lineWidth);
        glCtx.uniform1f(this.locations.trail, s.trail);
        glCtx.drawArrays(glCtx.TRIANGLE_STRIP, 0, 4);
      },
      dispose() {},
    },
  };

  function setPreset(id) {
    const nextId = presets[id] ? id : "lissajous_orbit";
    const renderer = presets[nextId].renderer || "canvas2d";
    if (activePreset?.dispose) activePreset.dispose();
    activePresetId = nextId;
    activeRenderer = renderer;
    activePreset = Object.create(presets[nextId]);
    if (renderer === "webgl-shader") {
      canvas = shaderCanvas;
      shaderCanvas.classList.remove("hidden");
      canvas2dEl.classList.add("hidden");
      gl = shaderCanvas.getContext("webgl", { antialias: false, alpha: false });
      if (!gl) throw new Error("WebGL unavailable");
      activePreset.init?.(gl, shaderCanvas, state);
    } else {
      canvas = canvas2dEl;
      canvas2dEl.classList.remove("hidden");
      shaderCanvas.classList.add("hidden");
      ctx2d = canvas2dEl.getContext("2d", { alpha: false });
      activePreset.init?.(ctx2d, canvas2dEl, state);
    }
    resize();
  }

  async function pollState() {
    try {
      const response = await fetch(`/api/generative/state?ts=${Date.now()}`, { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const payload = await response.json();
      Object.assign(state, payload.visualState || {});
      connected = true;
      if (state.preset !== activePresetId) setPreset(state.preset);
    } catch (_error) {
      connected = false;
    }
  }

  function updateDebug() {
    overlay.classList.toggle("hidden", !showOverlay);
    debugPreset.textContent = state.blackout ? "Blackout" : activePresetId.replaceAll("_", " ");
    debugStatus.textContent = connected ? "Connected" : "Offline - using last state";
    debugStatus.className = connected ? "online" : "offline";
    debugFps.textContent = `FPS ${Math.round(fps)} - ${state.quality}`;
    debugTrack.textContent = [state.artist, state.trackTitle, state.activeLook].filter(Boolean).join(" - ") || "No track metadata";
  }

  function draw(now) {
    const dt = Math.min(0.1, Math.max(0.001, (now - lastFrame) / 1000));
    lastFrame = now;
    fps = fps * 0.92 + (1 / dt) * 0.08;
    if (!state.freeze && !forcedFreeze) time += dt;
    if (now - lastPoll > 250) {
      lastPoll = now;
      pollState();
    }
    if (fps < 25) {
      if (!lowFpsSince) lowFpsSince = now;
      if (now - lowFpsSince > 5000 && state.quality !== "low") {
        state.quality = state.quality === "high" ? "medium" : "low";
        lowFpsSince = 0;
        resize();
      }
    } else {
      lowFpsSince = 0;
    }
    try {
      resize();
      canvas2dEl.style.opacity = String(clamp(state.opacity ?? 1));
      shaderCanvas.style.opacity = String(clamp(state.opacity ?? 1));
      if (state.blackout || !state.enabled) {
        clearOverlay();
        if (activeRenderer === "webgl-shader" && gl) {
          gl.clearColor(0, 0, 0, 1);
          gl.clear(gl.COLOR_BUFFER_BIT);
        } else if (ctx2d) {
          ctx2d.fillStyle = "#000";
          ctx2d.fillRect(0, 0, canvas.width, canvas.height);
        }
      } else {
        const renderState = effectiveState(state);
        activePreset?.update?.(dt, renderState);
        activePreset?.draw?.(activeRenderer === "webgl-shader" ? gl : ctx2d, canvas, renderState);
        drawLayerOverlay(renderState);
      }
    } catch (_error) {
      state.preset = "lissajous_orbit";
      setPreset("lissajous_orbit");
    }
    updateDebug();
    requestAnimationFrame(draw);
  }

  window.addEventListener("resize", resize);
  window.addEventListener("keydown", (event) => {
    const index = Number(event.key);
    if (index >= 1 && index <= starterOrder.length) state.preset = starterOrder[index - 1];
    if (event.key.toLowerCase() === "h") showOverlay = !showOverlay;
    if (event.key.toLowerCase() === "f") document.documentElement.requestFullscreen?.();
    if (event.key.toLowerCase() === "q") state.quality = state.quality === "low" ? "medium" : state.quality === "medium" ? "high" : "low";
    if (event.code === "Space") {
      event.preventDefault();
      forcedFreeze = !forcedFreeze;
    }
    if (event.key === "0") state.blackout = !state.blackout;
    if (presets[state.preset] && state.preset !== activePresetId) setPreset(state.preset);
    resize();
  });

  setPreset(state.preset);
  pollState();
  requestAnimationFrame(draw);
})();
