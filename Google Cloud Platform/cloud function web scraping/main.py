import functions_framework

from bs4 import BeautifulSoup as bs
import requests as rq
import pandas as pd
import logging
import os
import traceback
import re
import pyarrow.parquet as pq
from google.cloud import bigquery
from google.cloud import storage
import yaml

with open("./schemas.yaml") as schema_file:
    config = yaml.load(schema_file, Loader=yaml.Loader)

PROJECT_ID = os.getenv('onyx-park-409513')
BQ_DATASET = 'finalsprint'
CS = storage.Client()
BQ = bigquery.Client()
job_config = bigquery.LoadJobConfig()


@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json()

    name = request_json.get("name")
    city = request_json.get("city")
    print("Person ", name, "lives in ", city)

    url = 'https://www.datosmundial.com/america/usa/turismo.php'
    page = rq.get(url).text
    soup = bs(page)

    table = soup.find('table')
    df = pd.DataFrame(columns = ['year', 'visitors', 'revenue'])

    df = pd.DataFrame(columns = ['year', 'visitors', 'revenue'])
    for row in table.find_all('tr')[1::]:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        anio = cols[0]
        visitante = cols[1]
        ing = cols[2]
        df = pd.concat([df, pd.DataFrame({'year': [anio], 'visitors': [visitante], 'revenue': [ing]})], ignore_index=True)

    # Limpiar la columna 'visitante'
    df['visitors'] = df['visitors'].str.replace(' ', '').str.replace('M', '').str.replace(',', '.')

    # Convertir la columna a tipo numérico y multiplicar por 1,000,000
    df['visitors'] = pd.to_numeric(df['visitors']) * 1000000

    # Limpiar la columna 'revenue'
    df['revenue'] = df['revenue'].str.replace(' ', '').str.replace('MM€', '').str.replace(',', '.')

    # Convertir la columna a tipo numérico y multiplicar por mil millones
    df['revenue'] = pd.to_numeric(df['revenue']) * 1e9

    df['state_id'] = df.apply(lambda row: [2, 4, 1, 3, 5], axis=1)
    df_presupuesto = df.explode('state_id')

    data = {'state_id': [2, 4, 1, 3, 5],
            'ponderado': [0.298, 0.298, 0.186, 0.072, 0.054]}

    df_ponderado = pd.DataFrame(data)

    df_presupuesto_estado = pd.merge(df_presupuesto, df_ponderado, on='state_id')

    df_presupuesto_estado['visitors_state'] = df_presupuesto_estado['visitors'] * df_presupuesto_estado['ponderado']
    df_presupuesto_estado['revenue_state'] = df_presupuesto_estado['revenue'] * df_presupuesto_estado['ponderado']
    
    # Redondear y convertir a enteros
    df_presupuesto_estado['visitors_state'] = df_presupuesto_estado['visitors_state'].round().astype(int)
    df_presupuesto_estado['revenue_state'] = df_presupuesto_estado['revenue_state'].round().astype(int)

    df_final = df_presupuesto_estado.drop(['visitors', 'revenue', 'ponderado'], axis=1)
    
    for tableNombre in config:
        tableName = tableNombre.get('name')
        tableSchema = tableNombre.get('schema')
    

    
        _check_if_table_exists(tableName, tableSchema)
        
        _load_table_from_uri_gen(df_final, 'no', tableSchema, tableName)


    return 'done'



def _load_table_from_uri_gen(bucket_n, file_name, tableSchema, tableName):
    table_id = BQ.dataset(BQ_DATASET).table(tableName)
    schema = create_schema_from_yaml(tableSchema)
    job_config.schema = schema
    # Cargar DataFrame a BigQuery
    job_config.source_format = bigquery.SourceFormat.PARQUET
    job_config.write_disposition = 'WRITE_APPEND'
    load_job = BQ.load_table_from_dataframe(
        bucket_n,
        table_id,
        job_config=job_config,
    )
    load_job.result()
    print("Job finished.")

def _check_if_table_exists(tableName, tableSchema):
    table_id = BQ.dataset(BQ_DATASET).table(tableName)
    try:
        BQ.get_table(table_id)
    except Exception:
        logging.warn('Creating table: %s' % (tableName))
        schema = create_schema_from_yaml(tableSchema)
        table = bigquery.Table(table_id, schema=schema)
        table = BQ.create_table(table)
        print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))

def create_schema_from_yaml(table_schema):
     schema = []
     for column in table_schema:
          
          schemaField = bigquery.SchemaField(column['name'], column['type'], column['mode'])

          schema.append(schemaField)

          if column['type'] == 'RECORD':
               schemaField._fields = create_schema_from_yaml(column['fields'])
     return schema
