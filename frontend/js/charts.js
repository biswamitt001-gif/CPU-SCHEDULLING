/**
 * charts.js — Chart.js comparison graph: TAT vs WT per process
 */

let comparisonChart = null;

/**
 * Render a grouped bar chart comparing TAT and WT for each process.
 * @param {HTMLCanvasElement} canvas
 * @param {Array} results — [{id, tat, wt}, ...]
 */
export function renderComparisonChart(canvas, results) {
    if (comparisonChart) {
        comparisonChart.destroy();
        comparisonChart = null;
    }

    const labels = results.map(r => r.id);
    const tatData = results.map(r => r.tat);
    const wtData = results.map(r => r.wt);

    comparisonChart = new Chart(canvas, {
        type: 'bar',
        data: {
            labels,
            datasets: [
                {
                    label: 'Turnaround Time (TAT)',
                    data: tatData,
                    backgroundColor: 'rgba(57, 213, 193, 0.75)',
                    borderColor: '#39d5c1',
                    borderWidth: 2,
                    borderRadius: 6,
                    borderSkipped: false,
                },
                {
                    label: 'Waiting Time (WT)',
                    data: wtData,
                    backgroundColor: 'rgba(124, 106, 255, 0.75)',
                    borderColor: '#7c6aff',
                    borderWidth: 2,
                    borderRadius: 6,
                    borderSkipped: false,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 700,
                easing: 'easeOutQuart',
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#a0a0c0',
                        font: { family: 'Inter', size: 12, weight: '600' },
                        boxWidth: 14,
                        boxHeight: 14,
                        borderRadius: 4,
                        useBorderRadius: true,
                    },
                },
                tooltip: {
                    backgroundColor: '#1a1a26',
                    borderColor: 'rgba(255,255,255,0.08)',
                    borderWidth: 1,
                    titleColor: '#e8e8f0',
                    bodyColor: '#a0a0c0',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: ctx => ` ${ctx.dataset.label}: ${ctx.parsed.y} units`,
                    },
                },
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#7a7a9a', font: { family: 'JetBrains Mono', size: 11 } },
                },
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#7a7a9a', font: { family: 'JetBrains Mono', size: 11 } },
                },
            },
        },
    });
}
