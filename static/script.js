// Theme Toggle with LocalStorage
const themeToggleButton = document.getElementById('theme-toggle');
const body = document.body;

// Apply saved theme preference
if (localStorage.getItem('dark-mode') === 'enabled') {
  body.classList.add('dark-mode');
}

themeToggleButton.addEventListener('click', function () {
  body.classList.toggle('dark-mode');

  // Save theme preference
  if (body.classList.contains('dark-mode')) {
    localStorage.setItem('dark-mode', 'enabled');
  } else {
    localStorage.setItem('dark-mode', 'disabled');
  }

  // Update Chart Colors
  updateChartColors();
});

// Chart Instances Storage
const charts = {};

// Render Chart using Chart.js
function renderChart(chartId, label, data) {
  const ctx = document.getElementById(chartId)?.getContext('2d');
  if (!ctx) {
    console.error(`Chart with ID '${chartId}' not found`);
    return;
  }

  const isDarkMode = body.classList.contains('dark-mode');

  const chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
      datasets: [{
        label: label,
        data: data,
        borderColor: isDarkMode ? '#ffffff' : '#007bff',
        backgroundColor: isDarkMode
          ? 'rgba(255, 255, 255, 0.2)'
          : 'rgba(0, 123, 255, 0.2)',
        fill: true
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: {
            color: isDarkMode ? '#ffffff' : '#000000'
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: isDarkMode ? '#ffffff' : '#000000'
          }
        },
        y: {
          ticks: {
            color: isDarkMode ? '#ffffff' : '#000000'
          }
        }
      }
    }
  });

  // Store Chart Instance for Updating
  charts[chartId] = chart;
}

// Update Chart Colors on Theme Change
function updateChartColors() {
  const isDarkMode = body.classList.contains('dark-mode');

  for (const chartId in charts) {
    const chart = charts[chartId];
    
    chart.data.datasets[0].borderColor = isDarkMode ? '#ffffff' : '#007bff';
    chart.data.datasets[0].backgroundColor = isDarkMode
      ? 'rgba(255, 255, 255, 0.2)'
      : 'rgba(0, 123, 255, 0.2)';

    chart.options.plugins.legend.labels.color = isDarkMode ? '#ffffff' : '#000000';
    chart.options.scales.x.ticks.color = isDarkMode ? '#ffffff' : '#000000';
    chart.options.scales.y.ticks.color = isDarkMode ? '#ffffff' : '#000000';

    chart.update();
  }
}

// Example Data
const caloriesData = [200, 400, 350, 500, 650];
const waterIntakeData = [2, 2.5, 3, 2.8, 3.2];
const exerciseData = [30, 45, 40, 50, 60];

// Render Charts
renderChart('caloriesChart', 'Calories Burned', caloriesData);
renderChart('waterIntakeChart', 'Water Intake (L)', waterIntakeData);
renderChart('exerciseChart', 'Exercise Time (min)', exerciseData);
