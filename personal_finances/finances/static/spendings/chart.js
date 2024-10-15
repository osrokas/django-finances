
            function getRandomColor() {
                var letters = '0123456789ABCDEF'.split('');
                var color = '#';
                for (var i = 0; i < 6; i++ ) {
                    color += letters[Math.floor(Math.random() * 16)];
                }
                return color;
            }

            function chartHandler(e, legendItem, legend) {
                const index = legendItem.datasetIndex;
                const ci = legend.chart;
                if (ci.isDatasetVisible(index)) {
                    ci.hide(index);
                    legendItem.hidden = true;
                } else {
                    ci.show(index);
                    legendItem.hidden = false;
                }
            }


            var globalLabels = [{%for label in labels%}"{{label}}",{%endfor%}];
            var backgroundColors = [{%for color in values%} getRandomColor(),{%endfor%}];
            var data = [{%for value in values%}{{value}},{%endfor%}];

            const chart_data = globalLabels.map((x, i) => ({ 'Amount': data[i] }));
            console.log(chart_data);
                        
            let globalHidden = []
            for (let i = 0; i < globalLabels.length; i += 1) {
                globalHidden.push(false)
            }
            
            let dataset = []

            for (let i = 0; i < globalLabels.length; i += 1) {
                dataset.push({
                    label: globalLabels[i],
                    data: chart_data[i],
                    backgroundColor: backgroundColors[i],
                })
            }

            new Chart(document.getElementById('barChart'), {
                
                type: 'bar',
                labels: globalLabels,
                
                data: {
                           
                    datasets: dataset
                },

                options: {
                    plugins:{
                        chartArea: {
                            backgroundColor: backgroundColors
                        },
                        responsive: true,
                        legend: { 
                            display: true, 
                            position: 'right',
                            backgroundColors: backgroundColors,
                            onClick: chartHandler,
                            fontSize: 16,
                            labels: {
                                color: 'white',
                            },
                        },
                        title: {
                            display: true,
                            text: "Chart of spendings by category",
                            color: 'white',
                        },
                    },
                    scales: {
                        y: {
                            ticks: {
                                color: 'white',
                            },

                        },
                        x: {
                            ticks: {
                                color: 'white',
                            },
                    },
                },

                },
            },        
            );