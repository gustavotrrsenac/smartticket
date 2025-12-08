// Configuração Global do Chart.js para Dark Mode
Chart.defaults.color = 'rgba(255, 255, 255, 0.7)';
Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.1)';
Chart.defaults.font.family = "'Quicksand', sans-serif";

// --- GRÁFICO 1: FLUXO DE ABERTURA (LINHA/ÁREA) ---
const ctxMain = document.getElementById('mainChart').getContext('2d');

// Gradiente Roxo para o preenchimento
const gradientPurple = ctxMain.createLinearGradient(0, 0, 0, 400);
gradientPurple.addColorStop(0, 'rgba(168, 85, 247, 0.5)'); // Roxo forte
gradientPurple.addColorStop(1, 'rgba(168, 85, 247, 0.0)'); // Transparente

const mainChart = new Chart(ctxMain, {
    type: 'line',
    data: {
        labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
        datasets: [{
            label: 'Novos Chamados',
            data: [12, 19, 15, 25, 22, 10, 8],
            backgroundColor: gradientPurple,
            borderColor: '#a855f7',
            borderWidth: 2,
            pointBackgroundColor: '#fff',
            fill: true, // Preencher área abaixo
            tension: 0.4 // Curva suave (spline)
        },
        {
            label: 'Solucionados',
            data: [10, 15, 18, 20, 24, 12, 9],
            borderColor: '#22c55e', // Verde
            borderWidth: 2,
            pointBackgroundColor: '#22c55e',
            borderDash: [5, 5], // Linha tracejada
            fill: false,
            tension: 0.4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                align: 'end',
                labels: { usePointStyle: true, boxWidth: 8 }
            }
        },
        scales: {
            y: { beginAtZero: true, grid: { borderDash: [2, 4] } },
            x: { grid: { display: false } }
        }
    }
});

// --- GRÁFICO 2: POR DEPARTAMENTO (DOUGHNUT) ---
const ctxDept = document.getElementById('deptChart').getContext('2d');

const deptChart = new Chart(ctxDept, {
    type: 'doughnut',
    data: {
        labels: ['TI', 'Jurídico', 'Arquitetura'],
        datasets: [{
            data: [45, 30, 25],
            backgroundColor: [
                '#a855f7', // Roxo (TI)
                '#3b82f6', // Azul (Jur)
                '#22c55e'  // Verde (Arq)
            ],
            borderWidth: 0,
            hoverOffset: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%', // Tamanho do buraco no meio
        plugins: {
            legend: { display: false } // Usamos nossa legenda HTML customizada
        }
    }
});