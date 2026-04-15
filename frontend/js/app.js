/**
 * app.js — Advanced UI logic
 * Features: animated counters, ripple buttons, algo-tabs sync,
 *           randomize, section reveal, staggered table rows, history
 */

import { renderGantt, resetColors } from './gantt.js';
import { renderComparisonChart } from './charts.js';

const API_URL = '/schedule';
const HISTORY_URL = '/history';

// ─── DOM refs ────────────────────────────────
const algorithmSelect = document.getElementById('algorithm');
const quantumGroup = document.getElementById('quantum-group');
const quantumInput = document.getElementById('quantum');
const processTableBody = document.getElementById('process-tbody');
const addRowBtn = document.getElementById('add-row');
const clearBtn = document.getElementById('clear-btn');
const randomBtn = document.getElementById('random-btn');
const simulateBtn = document.getElementById('simulate-btn');
const spinner = document.getElementById('spinner');
const errorBanner = document.getElementById('error-banner');
const algoTabs = document.querySelectorAll('.algo-tab');
const ganttSection = document.getElementById('gantt-section');
const ganttTrack = document.getElementById('gantt-track');
const ganttTimeline = document.getElementById('gantt-timeline');
const ganttLegend = document.getElementById('gantt-legend');
const chartSection = document.getElementById('chart-section');
const chartCanvas = document.getElementById('comparison-chart');
const resultsSection = document.getElementById('results-section');
const resultsTbody = document.getElementById('results-tbody');
const avgTatEl = document.getElementById('avg-tat');
const avgWtEl = document.getElementById('avg-wt');
const algoLabelEl = document.getElementById('algo-label');
const statTat = document.getElementById('stat-tat');
const statWt = document.getElementById('stat-wt');
const historySection = document.getElementById('history-section');
const historyTbody = document.getElementById('history-tbody');
const refreshHistBtn = document.getElementById('refresh-history');

// ── Algorithm name map ────────────────────────
const ALGO_NAMES = {
    FCFS: 'First Come First Serve',
    SJF: 'Shortest Job First',
    SRTF: 'Shortest Remaining Time',
    PRIORITY: 'Priority Non-Preemptive',
    PRIORITY_P: 'Priority Preemptive',
    RR: 'Round Robin',
};

// ─── Algo Tabs ────────────────────────────────
algoTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        algorithmSelect.value = tab.dataset.value;
        syncTabs(tab.dataset.value);
        const isRR = tab.dataset.value === 'RR';
        quantumGroup.style.display = isRR ? 'flex' : 'none';
    });
});

algorithmSelect.addEventListener('change', () => {
    const v = algorithmSelect.value;
    syncTabs(v);
    quantumGroup.style.display = v === 'RR' ? 'flex' : 'none';
});

function syncTabs(value) {
    algoTabs.forEach(t => t.classList.toggle('active', t.dataset.value === value));
}

// Sync on load
syncTabs(algorithmSelect.value);

// ─── Ripple helper ────────────────────────────
function addRipple(btn, e) {
    const rect = btn.getBoundingClientRect();
    const r = document.createElement('span');
    r.className = 'ripple';
    const size = Math.max(rect.width, rect.height);
    r.style.cssText = `width:${size}px;height:${size}px;left:${e.clientX - rect.left - size / 2}px;top:${e.clientY - rect.top - size / 2}px;`;
    btn.appendChild(r);
    r.addEventListener('animationend', () => r.remove());
}
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', e => addRipple(btn, e));
});

// ─── Animated counter ────────────────────────
function animateCounter(el, target, duration = 900) {
    const start = performance.now();
    const from = parseFloat(el.textContent) || 0;

    function step(now) {
        const progress = Math.min((now - start) / duration, 1);
        // Ease-out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = (from + (target - from) * eased).toFixed(2);
        if (progress < 1) requestAnimationFrame(step);
        else el.textContent = target.toFixed(2);
    }
    requestAnimationFrame(step);
}

// ─── Section reveal helper ────────────────────
function revealSection(section, delay = 0) {
    section.style.display = 'block';
    section.classList.remove('section-visible');
    // Trigger reflow
    void section.offsetHeight;
    setTimeout(() => {
        section.classList.remove('section-hidden');
        section.classList.add('section-visible');
    }, delay);
}

// ─── Row counter ──────────────────────────────
let rowCount = 0;

function createRow(pid = '', arrival = 0, burst = '', prio = 1) {
    rowCount++;
    const num = processTableBody.querySelectorAll('tr').length + 1;

    const tr = document.createElement('tr');
    tr.style.animationDelay = (rowCount * 0.04) + 's';
    tr.classList.add('result-row');

    const defaultPid = pid || `P${num}`;
    tr.innerHTML = `
    <td><div class="row-num">${num}</div></td>
    <td><input type="text"   class="pid-input"      value="${defaultPid}" placeholder="P${num}" /></td>
    <td><input type="number" class="arrival-input"  value="${arrival}"    min="0"  placeholder="0" /></td>
    <td><input type="number" class="burst-input"    value="${burst}"      min="1"  placeholder="e.g. 4" /></td>
    <td><input type="number" class="priority-input" value="${prio}"       min="1"  placeholder="1" /></td>
    <td>
      <button class="btn btn-danger remove-row" title="Remove">✕</button>
    </td>
  `;
    tr.querySelector('.remove-row').addEventListener('click', () => {
        if (processTableBody.querySelectorAll('tr').length > 1) {
            tr.remove();
            rebuildRowNumbers();
        }
    });

    processTableBody.appendChild(tr);
}

function rebuildRowNumbers() {
    processTableBody.querySelectorAll('tr').forEach((tr, i) => {
        const numEl = tr.querySelector('.row-num');
        if (numEl) numEl.textContent = i + 1;
    });
}

// ─── Default sample data ──────────────────────
[
    { pid: 'P1', arrival: 0, burst: 6, priority: 2 },
    { pid: 'P2', arrival: 1, burst: 4, priority: 1 },
    { pid: 'P3', arrival: 3, burst: 2, priority: 3 },
    { pid: 'P4', arrival: 5, burst: 5, priority: 2 },
].forEach(s => createRow(s.pid, s.arrival, s.burst, s.priority));

addRowBtn.addEventListener('click', () => createRow());

clearBtn.addEventListener('click', () => {
    processTableBody.innerHTML = '';
    rowCount = 0;
    [resultsSection, ganttSection, chartSection, historySection].forEach(s => {
        s.style.display = 'none';
        s.classList.remove('section-visible');
        s.classList.add('section-hidden');
    });
    hideError();
});

// ─── Randomize ────────────────────────────────
randomBtn.addEventListener('click', () => {
    processTableBody.innerHTML = '';
    rowCount = 0;
    const count = Math.floor(Math.random() * 4) + 3; // 3-6 processes
    let arrival = 0;
    for (let i = 0; i < count; i++) {
        const burst = Math.floor(Math.random() * 9) + 1;
        const priority = Math.floor(Math.random() * 5) + 1;
        createRow(`P${i + 1}`, arrival, burst, priority);
        arrival += Math.floor(Math.random() * 3);
    }
});

// ─── Error / validation ───────────────────────
function showError(msg) {
    errorBanner.textContent = '⚠  ' + msg;
    errorBanner.style.display = 'block';
    errorBanner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
function hideError() { errorBanner.style.display = 'none'; }

function readProcesses() {
    const rows = processTableBody.querySelectorAll('tr');
    const processes = [], errors = [];

    rows.forEach((tr, i) => {
        const pid = tr.querySelector('.pid-input').value.trim() || `P${i + 1}`;
        const arrival = parseInt(tr.querySelector('.arrival-input').value);
        const burst = parseInt(tr.querySelector('.burst-input').value);
        const prio = parseInt(tr.querySelector('.priority-input').value) || 1;

        if (isNaN(burst) || burst < 1) { errors.push(`Row ${i + 1}: Burst time must be ≥ 1.`); return; }
        if (isNaN(arrival) || arrival < 0) { errors.push(`Row ${i + 1}: Arrival time must be ≥ 0.`); return; }

        processes.push({ id: pid, arrival, burst, priority: prio });
    });

    return { processes, errors };
}

// ─── Simulate ─────────────────────────────────
simulateBtn.addEventListener('click', async () => {
    hideError();

    const algorithm = algorithmSelect.value;
    const quantum = parseInt(quantumInput.value) || 2;
    const { processes, errors } = readProcesses();

    if (errors.length > 0) { showError(errors[0]); return; }
    if (!processes.length) { showError('Add at least one process.'); return; }

    // Loading state
    simulateBtn.disabled = true;
    spinner.style.display = 'block';
    simulateBtn.querySelector('.btn-text').style.opacity = '0';
    simulateBtn.querySelector('.btn-text').style.transform = 'translateY(-6px)';

    try {
        const resp = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ algorithm, processes, quantum }),
        });
        const data = await resp.json();

        if (!resp.ok) { showError(data.error || 'Server error.'); return; }

        renderResults(data);

    } catch (_err) {
        showError('Cannot connect to server. Make sure Flask is running on port 5000.');
    } finally {
        simulateBtn.disabled = false;
        spinner.style.display = 'none';
        simulateBtn.querySelector('.btn-text').style.opacity = '';
        simulateBtn.querySelector('.btn-text').style.transform = '';
    }
});

// ─── Render Results ───────────────────────────
function renderResults(data) {
    const { algorithm, results, gantt, avg_tat, avg_wt } = data;

    // Algorithm label
    let label = ALGO_NAMES[algorithm] || algorithm;
    if (algorithm === 'RR') label += ` (q=${data.quantum})`;
    algoLabelEl.textContent = label;

    // Animated stat counters — reset then re-trigger so animation replays every run
    statTat.classList.remove('animated');
    statWt.classList.remove('animated');
    void statTat.offsetHeight; // force reflow
    animateCounter(avgTatEl, avg_tat);
    animateCounter(avgWtEl, avg_wt);
    requestAnimationFrame(() => {
        statTat.classList.add('animated');
        statWt.classList.add('animated');
    });

    // Results table — staggered rows
    resultsTbody.innerHTML = '';
    results.forEach((r, i) => {
        const tr = document.createElement('tr');
        tr.className = 'result-row';
        tr.style.animationDelay = (i * 0.06) + 's';
        tr.innerHTML = `
      <td style="font-weight:700;">${r.id}</td>
      <td>${r.arrival}</td>
      <td>${r.burst}</td>
      <td class="col-ct">${r.ct}</td>
      <td class="col-tat">${r.tat}</td>
      <td class="col-wt">${r.wt}</td>
    `;
        resultsTbody.appendChild(tr);
    });

    // Reveal sections with stagger
    revealSection(resultsSection, 0);
    resetColors();
    renderGantt(ganttTrack, ganttTimeline, ganttLegend, gantt);
    revealSection(ganttSection, 120);

    renderComparisonChart(chartCanvas, results);
    revealSection(chartSection, 240);

    loadHistory().then(() => revealSection(historySection, 360));

    // Smooth scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 200);
}

// ─── History ──────────────────────────────────
async function loadHistory() {
    try {
        const resp = await fetch(HISTORY_URL);
        const rows = await resp.json();

        historyTbody.innerHTML = '';
        rows.forEach((r, i) => {
            const tr = document.createElement('tr');
            tr.className = 'result-row';
            tr.style.animationDelay = (i * 0.04) + 's';
            const date = new Date(r.created_at + 'Z').toLocaleString();
            tr.innerHTML = `
        <td style="color:var(--text-muted);">${r.id}</td>
        <td><span class="history-tag">${r.algorithm}</span></td>
        <td class="tat-cell">${parseFloat(r.avg_tat).toFixed(2)}</td>
        <td class="wt-cell">${parseFloat(r.avg_wt).toFixed(2)}</td>
        <td style="color:var(--text-dim);font-size:0.78rem;">${date}</td>
      `;
            historyTbody.appendChild(tr);
        });
    } catch { /* silent */ }
}

refreshHistBtn?.addEventListener('click', loadHistory);
