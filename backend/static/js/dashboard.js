document.addEventListener('DOMContentLoaded', function() {
  const ctx = document.getElementById('resourceChart');
  if (!ctx) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: chartLabels || [],
      datasets: [{
        label: 'Reservas por recurso',
        data: chartData || [],
        backgroundColor: '#107c49',
        borderRadius: 12,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: '#475569' }
        },
        y: {
          beginAtZero: true,
          ticks: { color: '#475569' },
          grid: { color: 'rgba(15, 23, 42, 0.08)' }
        }
      }
    }
  });
});
