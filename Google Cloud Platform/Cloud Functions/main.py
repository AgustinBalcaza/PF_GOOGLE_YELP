import logging
import os
import traceback
import re

from google.cloud import bigquery
from google.cloud import storage

import yaml

with open("./schemas.yaml") as schema_file:
     config = yaml.load(schema_file, Loader=yaml.Loader)

# El id del proyecto
PROJECT_ID = os.getenv('cloudquicklab')
# el nombre de la base de datos dataset
BQ_DATASET = 'staging'
CS = storage.Client()
BQ = bigquery.Client()
job_config = bigquery.LoadJobConfig()


def streaming(data):
     bucketname = data['bucket'] 
     print("Bucket name",bucketname)
     filename = data['name']   
     print("File name",filename)  
     timeCreated = data['timeCreated']
     print("Time Created",timeCreated) 
     try:
          for table in config:
               tableName = table.get('name')
               if re.search(tableName.replace('_', '-'), filename) or re.search(tableName, filename):
                    tableSchema = table.get('schema')
                    _check_if_table_exists(tableName,tableSchema)
                    tableFormat = table.get('format')
                    if tableFormat == 'NEWLINE_DELIMITED_JSON':
                         _load_table_from_uri(data['bucket'], data['name'], tableSchema, tableName)
     except Exception:
          print('Error streaming file. Cause: %s' % (traceback.format_exc()))

def _check_if_table_exists(tableName,tableSchema):

     table_id = BQ.dataset(BQ_DATASET).table(tableName)

     try:
          BQ.get_table(table_id)
     except Exception:
          logging.warn('Creating table: %s' % (tableName))
          schema = create_schema_from_yaml(tableSchema)
          table = bigquery.Table(table_id, schema=schema)
          table = BQ.create_table(table)
          print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))

def _load_table_from_uri(bucket_name, file_name, tableSchema, tableName):

     uri = 'gs://%s/%s' % (bucket_name, file_name)
     table_id = BQ.dataset(BQ_DATASET).table(tableName)

     schema = create_schema_from_yaml(tableSchema) 
     print(schema)
     job_config.schema = schema

     job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
     job_config.write_disposition = 'WRITE_APPEND',

     load_job = BQ.load_table_from_uri(
     uri,
     table_id,
     job_config=job_config,
     ) 
          
     load_job.result()
     print("Job finished.")

def create_schema_from_yaml(table_schema):
     schema = []
     for column in table_schema:
          
          schemaField = bigquery.SchemaField(column['name'], column['type'], column['mode'])

          schema.append(schemaField)

          if column['type'] == 'RECORD':
               schemaField._fields = create_schema_from_yaml(column['fields'])
     return schema

streaming(data)



# ##3##############################
import logging
import os
import traceback
import re
import pandas as pd
import pyarrow.parquet as pq
from google.cloud import bigquery
from google.cloud import storage
import yaml

with open("./schemas.yaml") as schema_file:
    config = yaml.load(schema_file, Loader=yaml.Loader)

PROJECT_ID = os.getenv('onyx-park-409513')
BQ_DATASET = 'primera'
CS = storage.Client()
BQ = bigquery.Client()
job_config = bigquery.LoadJobConfig()

def streaming(data):
    bucketname = data['bucket']
    filename = data['name']
    timeCreated = data['timeCreated']
    try:
        for table in config:
            tableName = table.get('name')
            if re.search(tableName.replace('_', '-'), filename) or re.search(tableName, filename):
                tableSchema = table.get('schema')
                _check_if_table_exists(tableName, tableSchema)
                tableFormat = table.get('format')
                if tableFormat == 'PARQUET':
                    _load_table_from_uri(data['bucket'], data['name'], tableSchema, tableName)
    except Exception:
        print('Error streaming file. Cause: %s' % (traceback.format_exc()))

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

def _load_table_from_uri(bucket_name, file_name, tableSchema, tableName):
    uri = 'gs://%s/%s' % (bucket_name, file_name)
    table_id = BQ.dataset(BQ_DATASET).table(tableName)
    schema = create_schema_from_yaml(tableSchema)
    job_config.schema = schema

    # Cargar datos desde Parquet a DataFrame
    df = pd.read_parquet(uri, engine='pyarrow')

    # Cargar DataFrame a BigQuery
    job_config.source_format = bigquery.SourceFormat.PARQUET
    job_config.write_disposition = 'WRITE_APPEND'
    load_job = BQ.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config,
    )

    load_job.result()
    print("Job finished.")

def create_schema_from_yaml(table_schema):
    schema = []
    for column in table_schema:
        schemaField = bigquery.SchemaField(column['name'], column['type'], column['mode'])
        schema.append(schemaField)

        if column['type'] == 'RECORD':
            schemaField.fields = create_schema_from_yaml(column['fields'])
    return schema










# ##3##############################
import logging
import os
import traceback
import re
import pandas as pd
import pyarrow.parquet as pq
from google.cloud import bigquery
from google.cloud import storage
import yaml

with open("./schemas.yaml") as schema_file:
    config = yaml.load(schema_file, Loader=yaml.Loader)

PROJECT_ID = os.getenv('onyx-park-409513')
BQ_DATASET = 'primera'
CS = storage.Client()
BQ = bigquery.Client()
job_config = bigquery.LoadJobConfig()

def streaming(data):
     bucketname = data['bucket']
     filename = data['name']
     timeCreated = data['timeCreated']
     
     try:
          uri = 'gs://%s/%s' % (data['bucket'], data['name'])
          if re.search('creado', filename):
               df_user = filtrarPorColumnaYGroupBy('creado.parquet',['user_id'], ['user_id'])
               df_state = filtrarPorColumnaYGroupBy('creado.parquet',['state_id', 'state'], ['state_id'])
               df_city = filtrarPorColumnaYGroupBy('creado.parquet',['city_id', 'city', 'state_id'], ['city_id', 'state_id'])
               df_category = filtrarPorColumnaYGroupBy('creado.parquet',['category_id', 'category'], ['category_id'])
               df_business = filtrarPorColumnaYGroupBy('creado.parquet',['business_id', 'business_name', 'city_id', 'longitude', 'latitude', 'avg_rating'], ['business_id'])
               df_reviews = filtrarPorColumnaYGroupBy('creado.parquet',['review_id','business_id', 'user_id', 'sentiment_analysis', 'month', 'year'], ['review_id'])
               df_business_category = filtrarPorColumnaYGroupBy('creado.parquet', ['business_id', 'category_id'], ['business_id', 'category_id'])
               
               for tableNombre in config:
                    tableName = tableNombre.get('name')
                    tableSchema = tableNombre.get('schema')
                    _check_if_table_exists(tableName, tableSchema)
                    tableFormat = tableNombre.get('format')
                    if tableFormat == 'PARQUET':
                         if(tableName == 'users'):
                              _load_table_from_uri_gen(df_user, data['name'], tableSchema, tableName)
                         if(tableName == 'state'):
                              _load_table_from_uri_gen(df_state, data['name'], tableSchema, tableName)
                         if(tableName == 'city'):
                              _load_table_from_uri_gen(df_city, data['name'], tableSchema, tableName)
                         if(tableName == 'category'):
                              _load_table_from_uri_gen(df_category, data['name'], tableSchema, tableName)
                         if(tableName == 'business'):
                              _load_table_from_uri_gen(df_business, data['name'], tableSchema, tableName)
                         if(tableName == 'reviews'):
                              _load_table_from_uri_gen(df_reviews, data['name'], tableSchema, tableName)
                         if(tableName == 'intermediaCatBus'):
                              _load_table_from_uri_gen(df_business_category, data['name'], tableSchema, tableName)
                         
     
          for table in config:
               tableName = table.get('name')
               
               
               if re.search(tableName.replace('_', '-'), filename) or re.search(tableName, filename):
                    tableSchema = table.get('schema')
                    _check_if_table_exists(tableName, tableSchema)
                    tableFormat = table.get('format')
                    if tableFormat == 'PARQUET':
                         _load_table_from_uri(data['bucket'], data['name'], tableSchema, tableName)
     except Exception:
          print('Error streaming file. Cause: %s' % (traceback.format_exc()))


def filtrarPorColumnaYGroupBy(archivo, columnasFiltrar, columnasGroupBy):
     df = pd.read_parquet(archivo, engine='pyarrow')
     grouped_df = df.groupby(columnasGroupBy, as_index=False)[columnasFiltrar].first()
     return grouped_df



          
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

def _load_table_from_uri(bucket_name, file_name, tableSchema, tableName):
    uri = 'gs://%s/%s' % (bucket_name, file_name)
    table_id = BQ.dataset(BQ_DATASET).table(tableName)
    schema = create_schema_from_yaml(tableSchema)
    job_config.schema = schema

    # Cargar datos desde Parquet a DataFrame
    df = pd.read_parquet(uri, engine='pyarrow')
    
    # Eliminar filas duplicadas
    df_sin_duplicados = df.drop_duplicates()

    # Eliminar filas que contienen valores nulos
    df_limpio = df_sin_duplicados.dropna()
    


    # Cargar DataFrame a BigQuery
    job_config.source_format = bigquery.SourceFormat.PARQUET
    job_config.write_disposition = 'WRITE_APPEND'
    load_job = BQ.load_table_from_dataframe(
        df_limpio,
        table_id,
        job_config=job_config,
    )

    load_job.result()
    print("Job finished.")

def create_schema_from_yaml(table_schema):
    schema = []
    for column in table_schema:
        schemaField = bigquery.SchemaField(column['name'], column['type'], column['mode'])
        schema.append(schemaField)

        if column['type'] == 'RECORD':
            schemaField.fields = create_schema_from_yaml(column['fields'])
    return schema

