var demo = {
  initDashboardPageCharts: function() {
    var ctx = document.getElementById('bigDashboardChart').getContext("2d");

    var chartData = {
      labels: Array.from({ length: 30 }, (_, i) => (i + 1) + " min"), // Fixed range from 1 to 30 minutes
      data: new Array(60).fill(0) // Initialize data array with zeros for 60 minutes
    };

    var myChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: chartData.labels,
        datasets: [{
          label: "Light Status",
          borderColor: "#4caf50",
          backgroundColor: "rgba(76, 175, 80, 0.2)",
          data: chartData.data,
          steppedLine: true // Use stepped line for sharp changes
        }]
      },
      options: {
        maintainAspectRatio: false,
        layout: {
          padding: {
            top: 10, // Top padding
            bottom: 10, // Bottom padding
            left: 30, // Left padding
            right: 30 // Right padding
          }
        },
        tooltips: {
          backgroundColor: '#fff',
          titleFontColor: '#333',
          bodyFontColor: '#666',
          bodySpacing: 4,
          xPadding: 12,
          mode: "nearest",
          intersect: 0,
          position: "nearest"
        },
        legend: {
          position: "bottom",
          fillStyle: "#FFF",
          display: true
        },
        scales: {
          yAxes: [{
            ticks: {
              fontColor: "#fff",
              fontStyle: "bold",
              beginAtZero: true,
              min: 0, // Minimum value for y-axis
              max: 1, // Maximum value for y-axis
              stepSize: 1, // Step size for y-axis
              callback: function(value, index, values) {
                return value; // Display only 0 and 1 on y-axis
              }
            },
            gridLines: {
              drawTicks: true,
              display: true,
              color: "rgba(255, 255, 255, 0.1)",
              zeroLineColor: "transparent"
            }
          }],
          xAxes: [{
            gridLines: {
              zeroLineColor: "transparent",
              display: true,
              color: "rgba(255, 255, 255, 0.1)"
            },
            ticks: {
              padding: 10,
              fontColor: "#fff",
              fontStyle: "bold"
            }
          }]
        }
      }
    });

    // Function to update chart data based on API responses
    function updateChartData(data) {
      // Get current time in minutes
      var currentTime = new Date();
      var currentMinute = currentTime.getMinutes();

      // Update data array based on current time and API response for person detection
      if (currentMinute < 30) {
        chartData.data[currentMinute] = data.person_detected == 'yes' ? 1 : 0; // Set data for current minute
      } else {
        chartData.data[currentMinute - 30] = data.person_detected == 'yes' ? 1 : 0; // Set data for current minute after 30 minutes
      }

      // Update the chart with new data
      myChart.update();
    }

    // Call the API update function initially and every 5 seconds
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

    // Call the function initially and set interval for periodic updates
    fetchDataAndUpdateChart();
    setInterval(fetchDataAndUpdateChart, 5000); // Update every 5 seconds
  }
};

demo.initDashboardPageCharts();

// var demo = {
//   initDashboardPageCharts: function() {

//     chartColor = "#FFFFFF";

//     // General configuration for the charts with Line gradientStroke
//     gradientChartOptionsConfiguration = {
//       maintainAspectRatio: false,
//       legend: {
//         display: false
//       },
//       tooltips: {
//         bodySpacing: 4,
//         mode: "nearest",
//         intersect: 0,
//         position: "nearest",
//         xPadding: 10,
//         yPadding: 10,
//         caretPadding: 10
//       },
//       responsive: 1,
//       scales: {
//         yAxes: [{
//           display: 0,
//           gridLines: 0,
//           ticks: {
//             display: false
//           },
//           gridLines: {
//             zeroLineColor: "transparent",
//             drawTicks: false,
//             display: false,
//             drawBorder: false
//           }
//         }],
//         xAxes: [{
//           display: 0,
//           gridLines: 0,
//           ticks: {
//             display: false
//           },
//           gridLines: {
//             zeroLineColor: "transparent",
//             drawTicks: false,
//             display: false,
//             drawBorder: false
//           }
//         }]
//       },
//       layout: {
//         padding: {
//           left: 0,
//           right: 0,
//           top: 15,
//           bottom: 15
//         }
//       }
//     };

//     gradientChartOptionsConfigurationWithNumbersAndGrid = {
//       maintainAspectRatio: false,
//       legend: {
//         display: false
//       },
//       tooltips: {
//         bodySpacing: 4,
//         mode: "nearest",
//         intersect: 0,
//         position: "nearest",
//         xPadding: 10,
//         yPadding: 10,
//         caretPadding: 10
//       },
//       responsive: true,
//       scales: {
//         yAxes: [{
//           gridLines: 0,
//           gridLines: {
//             zeroLineColor: "transparent",
//             drawBorder: false
//           }
//         }],
//         xAxes: [{
//           display: 0,
//           gridLines: 0,
//           ticks: {
//             display: false
//           },
//           gridLines: {
//             zeroLineColor: "transparent",
//             drawTicks: false,
//             display: false,
//             drawBorder: false
//           }
//         }]
//       },
//       layout: {
//         padding: {
//           left: 0,
//           right: 0,
//           top: 15,
//           bottom: 15
//         }
//       }
//     };

//     var ctx = document.getElementById('bigDashboardChart').getContext("2d");

//     var chartData = {
//       labels: Array.from({ length: 30 }, (_, i) => (i + 1) + " min"), // Fixed range from 1 to 30 minutes
//       data: new Array(60).fill(0) // Initialize data array with zeros for 60 minutes
//     };

//     var myChart = new Chart(ctx, {
//       type: 'line',
//       data: {
//         labels: chartData.labels,
//         datasets: [{
//           label: "Light Status",
//           borderColor: "#4caf50",
//           backgroundColor: "rgba(76, 175, 80, 0.2)",
//           data: chartData.data,
//           steppedLine: true // Use stepped line for sharp changes
//         }]
//       },
//       options: {
//         maintainAspectRatio: false,
//         layout: {
//           padding: {
//             top: 10, // Top padding
//             bottom: 10, // Bottom padding
//             left: 30, // Left padding
//             right: 30 // Right padding
//           }
//         },
//         tooltips: {
//           backgroundColor: '#fff',
//           titleFontColor: '#333',
//           bodyFontColor: '#666',
//           bodySpacing: 4,
//           xPadding: 12,
//           mode: "nearest",
//           intersect: 0,
//           position: "nearest"
//         },
//         legend: {
//           position: "bottom",
//           fillStyle: "#FFF",
//           display: false
//         },
//         scales: {
//           yAxes: [{
//             ticks: {
//               fontColor: "rgba(255,255,255,0.4)",
//               fontStyle: "bold",
//               beginAtZero: true,
//               maxTicksLimit: 5,
//               padding: 10
//             },
//             gridLines: {
//               drawTicks: true,
//               drawBorder: false,
//               display: true,
//               color: "rgba(255,255,255,0.1)",
//               zeroLineColor: "transparent"
//             }

//           }],
//           xAxes: [{
//             gridLines: {
//               zeroLineColor: "transparent",
//               display: false,

//             },
//             ticks: {
//               padding: 10,
//               fontColor: "rgba(255,255,255,0.4)",
//               fontStyle: "bold"
//             }
//           }]
//         }
//       }
//     });

//     var cardStatsMiniLineColor = "#fff",
//       cardStatsMiniDotColor = "#fff";

//     ctx = document.getElementById('lineChartExample').getContext("2d");

//     gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
//     gradientStroke.addColorStop(0, '#80b6f4');
//     gradientStroke.addColorStop(1, chartColor);

//     gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
//     gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
//     gradientFill.addColorStop(1, "rgba(249, 99, 59, 0.40)");
//   }
// };