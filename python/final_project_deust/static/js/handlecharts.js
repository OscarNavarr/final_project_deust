/* var options = {
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
    series: [25],
}

var chart = new ApexCharts(document.querySelector("#chart_intruction_id"), options);
chart.render(); */


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