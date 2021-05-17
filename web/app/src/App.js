import React, { useState, useEffect } from 'react';
import api from './services/api';
import './App.css';
import BarChart from './components/BarChart'
import ScatterChart from './components/ScatterChart'



function App() {
  const [coefParams, setCoefParams] = useState([])
  const [dataset, setDataset] = useState([])
  

  useEffect(() => {
    async function loadCoefParams() {
      const response = await api.get('/coef_params/ibge_pernambuco');

      setCoefParams(response.data);
      // console.log(response.data)
    }

    async function loadDataset() {
      const response = await api.get('/dataset/ibge_pernambuco');

      setDataset(response.data.dataset);
      // console.log(response.data.index)
    }

    loadCoefParams();
    loadDataset();
  }, [])


  return (
    <div>
      <header>
        <nav>
          <ul>
            <li><a href="/">Semana da Computação UNICAP</a></li>
          </ul>
        </nav>
      </header>

      <main>
        <div className="content left">
          <BarChart coefParams={coefParams} />
        </div>
        <div className="content right">
          <ScatterChart coefParams={coefParams} dataset={dataset} />
        </div>
      </main>
      
    </div>
  );
}

export default App;
