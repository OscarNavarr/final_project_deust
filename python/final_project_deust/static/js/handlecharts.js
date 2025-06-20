export function handleChart(instructionId, total, value) {

    const percentage = (value / total) * 100;

    var options = {
        chart: {
            height: 70,
            type: 'radialBar',
        },
        legend: {
            show: false
        },
        plotOptions: {
            radialBar: {
                dataLabels: {
                    name: {
                        show: false
                    },
                    value: {
                        show: true,
                        fontSize: '11px',
                        offsetY: 3.4,
                        padding: "0rem",
                        fontWeight: 700,
                        color: '#000',
                    }
                }
            }
        },  
        series: [percentage],

    }

    var chart = new ApexCharts(document.querySelector("#chart_" + instructionId), options);
    chart.render();
}

export function handleBarChart(data){

    const totalResult = [];

    for (const instruction of data) {
        const recovered_robot = instruction.recovered_robot || "0";


        // trnasform the recovered_robot to array of numbers
        const recoveredRobotArray = recovered_robot.split(',').map(Number);

        totalResult.push(recoveredRobotArray.length);

    }

    console.log('totalResult', totalResult);
    var options = {
          series: [{
          name: 'Cubes récupérés',
          data: [...totalResult]
        }],
          chart: {
          height: 350,
          type: 'bar',
        },
        plotOptions: {
          bar: {
            borderRadius: 10,
            dataLabels: {
              position: 'top', // top, center, bottom
            },
          }
        },
        dataLabels: {
          enabled: true,
          formatter: function (val) {
            return val ;
          },
          offsetY: -25,
          style: {
            fontSize: '12px',
            colors: ["#304758"],
            fontWeight: 700
          }
        },
        
        xaxis: {
          categories: ["GHOSTEYES", "O.S.R", "MAXENCE...", "PATHFINDER", "MR KRABS", "PASTA BOT"],
          position: 'bottom',
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false
          },
          crosshairs: {
            fill: {
              type: 'gradient',
              gradient: {
                colorFrom: '#D8E3F0',
                colorTo: '#BED1E6',
                stops: [0, 100],
                opacityFrom: 0.4,
                opacityTo: 0.5,
              }
            }
          },
          tooltip: {
            enabled: true,
          }
        },
        yaxis: {
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false,
          },
          labels: {
            show: false,
            formatter: function (val) {
              return val 
            }
          }
        
        },
        title: {
          text: 'Total des cubes recupérés par robot',
          floating: false, 
          offsetY: 0,
          align: 'center',
          style: {
            color: '#444',
            marginTop: '20px',
            marginBottom: '20px',
          }
        }
        };

        var chart = new ApexCharts(document.querySelector("#barChartResult"), options);
        chart.render();
      
}