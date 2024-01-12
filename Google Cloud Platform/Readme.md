# Google Cloud Platform

Para el presente proyecto se decidio trabajar con los servicios en la nube que proporciona GCP en la capa gratuita que brinda.

## Carga Inicial

Con la subida inicial de archivos al servicio de Google Cloud Storage, se activara disparador en Google cloud functions el cual extraera ese archivo para poder realizar una transformación separandolas y agrupandolas para poder construir el Data Warehouse y posteriormente este sera llevado a BigQuery con el esquema correspondiente definido en el archivo schema.yaml el cual se encuentra en la carpeta Cloud Functions y posteriormente se llenara todos los datos en BgiQuery provenientes de Google Cloud Storage.
El archivo main.py que usa Cloud Functions para que se encarga de realizar los procesos de ETL se encuentra en la carpeta Cloud Functions

## Carga Incremental

Para la carga incremental de la misma forma se uso las mismas tecnologias Google Cloud Storage, Cloud Functions y BigQuery, en donde el archivo que se sube debe tener por nombre la tabla en la cual se quiere realizar la carga incremental y si se subira varios archivos que hacen referencia a una tabla solamente se puede poner un guión y la fecha para no ocacionar conflictos, una vez subido los datos estos seran validados primeramente para poder ser enviados a BigQuery

Para ver el funcionamiento de ambos se realizo un video en donde se muestra todo el proceso el cual se encuentra en el siguiente enlace.
https://youtu.be/Trp1KBe-zFM

