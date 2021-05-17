import React from 'react';
import { Scatter } from 'react-chartjs-2'

function linspace(start, stop, num) {
    const step = (stop - start) / (num - 1);
    return Array.from({ length: num }, (_, i) => start + step * i);
}


function ScatterChart(props) {
    const { dataset, coefParams } = props;

    const xAxis = "Mortalidade_Infantil"
    const yAxis = "Salário_médio_mensal_dos_trabalhadores_formais"

    
    const max = Math.max(...dataset.map(row => (row[xAxis])))
    const xline = linspace(0, max, 100)
    const yline = xline.map(x => (coefParams['Intercept'] + x*coefParams[xAxis]))
    
   
    return <div>
        <Scatter
            data={{
                labels: xline,
                datasets: [
                    {                       
                        type: 'scatter',
                        label: 'IBGE Pernambuco',
                        backgroundColor: 'blue',
                        data: dataset.map(row => ({ x: row[xAxis], y: row[yAxis] }))
                    },
                    {
                        type: 'line',
                        label: 'Regression line ',
                        borderColor: 'orange',
                        backgroundColor: 'orange',
                        pointRadius: 0,
                        data: yline,
                        
                    },

                ]
            }}
            height={260}
            options={{
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Regression line: '
                            + xAxis.replace(/_/g, ' ') 
                            + ' x '
                            + yAxis.replace(/_/g, ' '),
                        padding: {
                            top: 10,
                            bottom: 10
                        }
                    }
                }
            }}
        />
    </div>
}

export default ScatterChart