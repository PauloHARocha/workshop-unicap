# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

import json
import pandas as pd
import numpy as np
import statsmodels.api as sm


# [START default_args]
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
}
# [END default_args]

# [START instantiate_dag]
with DAG(
    'workshop_data_pipeline',
    default_args=default_args,
    description='Workshop data pipeline',
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['workshop'],
) as dag:
    # [END instantiate_dag]

    # [START extract_function]
    def extract(**kwargs):
        ti = kwargs['ti']
        dataset_name = kwargs['dataset']['name']
        dataset_index = kwargs['dataset']['index']
        dataset_columns = kwargs['dataset']['columns']

        df = pd.read_csv(f'data/raw/{dataset_name}.csv')

        df.columns = list(
            map(
                lambda x: x.replace('\"', '').strip().replace(' ', '_'),
                df.columns.values))

        df = df.replace(' undefined', np.nan)

        df = df.set_index(dataset_index)

        df = df.loc[:, dataset_columns]

        for col in df.columns.values:
            df[col] = df[col].astype(float)
            df[col] = df[col].fillna((df[col].mean()))

        df.to_csv(f'data/transformed/{dataset_name}_transformed.csv')

        ti.xcom_push('dataset_name', dataset_name)
        ti.xcom_push('dataset_index', dataset_index)

    # [END extract_function]

    # [START regression_analysis_function]
    def regression_analysis(**kwargs):
        ti = kwargs['ti']
        dataset_name = ti.xcom_pull(task_ids='extract', key='dataset_name')
        dataset_index = ti.xcom_pull(task_ids='extract', key='dataset_index')

        df = pd.read_csv(f'data/transformed/{dataset_name}_transformed.csv',
                        index_col=dataset_index)

        y = kwargs['y']
        cols = df.drop(columns=y).columns
        formula = f"{y} ~ " + ' + '.join(cols)

        model = sm.OLS.from_formula(formula=formula, data=df)

        res = model.fit()

        ti.xcom_push('coef_params', res.params.to_json(force_ascii=False))

    # [END regression_analysis_function]

    # [START load_function]
    def load_coef_params(**kwargs):
        ti = kwargs['ti']
        dataset_name = ti.xcom_pull(task_ids='extract', key='dataset_name')

        coef_params = ti.xcom_pull(task_ids='regression_analysis', key='coef_params')
        coef_params = json.loads(coef_params)

        print(coef_params)

        with open(f'data/load/{dataset_name}_coef_params.json', 'w', encoding='utf-8') as f:
            json.dump(coef_params, f, ensure_ascii=False)
    
    def load_dataset(**kwargs):
        ti = kwargs['ti']
        dataset_name = ti.xcom_pull(task_ids='extract', key='dataset_name')
        dataset_index = ti.xcom_pull(task_ids='extract', key='dataset_index')

        df = pd.read_csv(f'data/transformed/{dataset_name}_transformed.csv',
                        index_col=dataset_index)

        dataset = {}

        dataset['index'] = df.index.values.tolist()
        dataset['dataset'] = []
        df.apply(lambda x: dataset['dataset'].append(x.to_dict()), axis=1)

        with open(f'data/load/{dataset_name}_transformed.json', 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False)

    # [END load_function]

    # [START main_flow]
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
        op_kwargs={
            'dataset': {
                'name': 'ibge_pernambuco',
                'index': 'Local',
                'columns': ['Densidade_demográfica', 'Salário_médio_mensal_dos_trabalhadores_formais',
                            'População_ocupada', 'Taxa_de_escolarização_de_6_a_14_anos_de_idade', 
                            'Mortalidade_Infantil', 'Esgotamento_sanitário_adequado'],
            }
        }
    )
  

    regression_analysis_task = PythonOperator(
        task_id='regression_analysis',
        python_callable=regression_analysis,
        op_kwargs={
            'y': 'Salário_médio_mensal_dos_trabalhadores_formais'
        }
    )


    load_coef_params_task = PythonOperator(
        task_id='load_coef_params',
        python_callable=load_coef_params,
    )

    load_dataset_task = PythonOperator(
        task_id='load_dataset',
        python_callable=load_dataset,
    )

    extract_task >> regression_analysis_task >> [load_coef_params_task, load_dataset_task]

# [END main_flow]

# [END tutorial]