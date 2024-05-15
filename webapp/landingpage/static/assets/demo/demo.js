var demo = {
  initDashboardPageCharts: function() {
    var ctx = document.getElementById('bigDashboardChart').getContext("2d");

    var chartData = {
      labels: Array.from({ length: 30 }, (_, i) => (i + 1) + " min"),
      data: new Array(30).fill(0), // Data now holds person detected state for 30 minutes
      energyConsumed: new Array(30).fill(0) // Array to hold energy consumed per minute
    };

    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: chartData.labels,
        datasets: [
          {
            label: "Light Status",
            borderColor: "#4caf50",
            backgroundColor: "rgba(76, 175, 80, 0.2)",
            data: chartData.data,
            steppedLine: true
          },
          {
            label: "Energy Consumed (Wh)",
            borderColor: "#f44336",
            backgroundColor: "rgba(244, 67, 54, 0.2)",
            data: chartData.energyConsumed,
            yAxisID: 'y-axis-energy'
          }
        ]
      },
      options: {
        maintainAspectRatio: false,
        tooltips: {...},
        legend: {...},
        scales: {
          yAxes: [
            {...}, // existing y-axis config for light status
            {
              id: 'y-axis-energy',
              type: 'linear',
              position: 'right',
              ticks: {
                beginAtZero: true
              }
            }
          ],
          xAxes: [...]
        }
      }
    });

    function updateChartData(data) {
      var currentTime = new Date();
      var currentMinute = currentTime.getMinutes() % 30; // Cycle through 30 minutes

      // Update data for person detected state and energy consumed
      chartData.data[currentMinute] = data.person_detected === 'yes' ? 1 : 0;
      chartData.energyConsumed[currentMinute] = data.number_of_bulbs_on * 5 / 60; // 5W per bulb, divide by 60 for watt-hours

      myChart.update();
    }

    function fetchDataAndUpdateChart() {
      $.ajax({
        url: '{% url "ajax_update_data" %}',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
          updateChartData(data);
        },
        error: function(xhr, status, error) {
          console.log('Error updating data:', error);
        }
      });
    }

    fetchDataAndUpdateChart();
    setInterval(fetchDataAndUpdateChart, 5000);
  }
};

demo.initDashboardPageCharts();