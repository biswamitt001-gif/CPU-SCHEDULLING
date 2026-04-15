/**
 * gantt.js — Advanced Gantt chart renderer
 * Features: proportional blocks, duration labels, animated stagger,
 *           sheen overlay, legend builder, colour map
 */

const PROCESS_COLORS = [
  '#7c6aff', '#00e5c8', '#ff7c5c', '#ffd166',
  '#06d6a0', '#ef476f', '#38b6ff', '#fd9e02',
  '#a8ff78', '#c77dff',
];

const colorMap = {};

export function resetColors() {
  Object.keys(colorMap).forEach(k => delete colorMap[k]);
}

function getColor(pid) {
  if (!(pid in colorMap)) {
    const idx = Object.keys(colorMap).length;
    colorMap[pid] = PROCESS_COLORS[idx % PROCESS_COLORS.length];
  }
  return colorMap[pid];
}

const SCALE = 46; // px per time unit

/**
 * @param {HTMLElement} container    - .gantt-track div
 * @param {HTMLElement} tickCont     - .gantt-timeline div
 * @param {HTMLElement} legendCont   - .gantt-legend div
 * @param {Array}       gantt        - [{pid, start, end}, ...]
 */
export function renderGantt(container, tickCont, legendCont, gantt) {
  container.innerHTML = '';
  tickCont.innerHTML = '';
  legendCont.innerHTML = '';

  if (!gantt || gantt.length === 0) return;

  const seen = new Set();

  // ── Blocks ────────────────────────────────
  gantt.forEach((seg, i) => {
    const duration = seg.end - seg.start;
    const width = Math.max(duration * SCALE, 36);
    const isIdle = seg.pid === 'IDLE';
    const color = isIdle ? null : getColor(seg.pid);

    const block = document.createElement('div');
    block.className = 'gantt-block' + (isIdle ? ' idle' : '');
    block.style.width = width + 'px';
    block.style.animationDelay = (i * 0.055) + 's';

    if (color) {
      block.style.background =
        `linear-gradient(160deg, ${color}ee 0%, ${color}88 100%)`;
      block.style.boxShadow = `0 3px 16px ${color}50, 0 1px 0 rgba(255,255,255,0.12) inset`;
    }

    // PID label
    const pidEl = document.createElement('span');
    pidEl.className = 'pid';
    pidEl.textContent = seg.pid;
    block.appendChild(pidEl);

    // Duration label (show only if block wide enough)
    if (width >= 60) {
      const durEl = document.createElement('span');
      durEl.className = 'dur';
      durEl.textContent = `${duration}u`;
      block.appendChild(durEl);
    }

    // Tooltip
    block.title = `${seg.pid}  ·  t${seg.start} → t${seg.end}  (${duration} units)`;

    container.appendChild(block);

    // Track for legend
    if (!isIdle && !seen.has(seg.pid)) {
      seen.add(seg.pid);
    }
  });

  // ── Timeline ticks ────────────────────────
  const times = new Set();
  gantt.forEach(s => { times.add(s.start); times.add(s.end); });
  const sortedTimes = [...times].sort((a, b) => a - b);

  tickCont.style.position = 'relative';
  tickCont.style.height = '22px';
  // Defer width measurement until after browser layout pass
  requestAnimationFrame(() => {
    tickCont.style.minWidth = (container.scrollWidth || container.offsetWidth) + 'px';
  });

  sortedTimes.forEach(t => {
    // Calculate pixel offset: sum widths of all segments that finish before t
    let offsetPx = 0;
    gantt.forEach((seg, idx) => {
      const segW = Math.max((seg.end - seg.start) * SCALE, 36) + 3; // 3 = gap
      if (seg.end <= t) {
        offsetPx += segW;
      } else if (seg.start < t && seg.end > t) {
        offsetPx += (t - seg.start) / (seg.end - seg.start) * segW;
      }
    });

    const tick = document.createElement('div');
    tick.className = 'gantt-tick';
    tick.textContent = t;
    tick.style.left = offsetPx + 'px';
    tickCont.appendChild(tick);
  });

  // ── Legend ────────────────────────────────
  seen.forEach(pid => {
    const item = document.createElement('div');
    item.className = 'legend-item';

    const dot = document.createElement('div');
    dot.className = 'legend-dot';
    dot.style.background = getColor(pid);
    dot.style.boxShadow = `0 0 8px ${getColor(pid)}80`;

    const label = document.createElement('span');
    label.textContent = pid;

    item.appendChild(dot);
    item.appendChild(label);
    legendCont.appendChild(item);
  });
}
