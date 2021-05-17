import React from 'react';
import { Bar } from 'react-chartjs-2'

function BarChart(props) {
    const { coefParams } = props;

    return <div>
        <Bar
            data={{
                labels: Object.keys(coefParams).map(x => x.replace(/_/g, ' ')),
                datasets: [
                    {   
                        label: 'Coefficient',
                        backgroundColor: 'rgb(255, 99, 132)',
                        borderColor: 'rgb(255, 99, 132)',
                        borderWidth: 4,
                        barPercentage: 0.4,
                        data: Object.values(coefParams),
                    }
                ]
            }}
            height={260}
            options={{
                indexAxis: 'y',
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Regression coefficients',
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

export default BarChart