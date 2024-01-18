# Google Cloud Platform

Para el presente proyecto se decidio trabajar con los servicios en la nube que proporciona GCP en la capa gratuita que brinda.

## Carga Inicial

Con la subida inicial de archivos al servicio de Google Cloud Storage, se activara disparador en Google cloud functions el cual extraera ese archivo para poder realizar una transformación separandolas y agrupandolas para poder construir el Data Warehouse y posteriormente este sera llevado a BigQuery con el esquema correspondiente definido en el archivo schema.yaml el cual se encuentra en la carpeta Cloud Functions y posteriormente se llenara todos los datos en BgiQuery provenientes de Google Cloud Storage.
El archivo main.py que usa Cloud Functions se encarga de realizar los procesos de ETL se encuentra en la carpeta Cloud Functions.

## Carga Del Web Scraping

Para cumplir con los Kpi's se necesita información de diferentes páginas web como ser el **Sitio Oficial De Estados Unidos Del Comercio Internacional** y de **Datos Mundial**, por tanto, se realizo un web scraping automatizado el cual se encarga de obtener los datos de forma anual mediante un crom jobs establecido en Google Cloud Scheduler, el cual activa el cloud function para realizar todo este proceso.
Una ves finalizado el proceso Cloud Function se encargara de enviar los datos a BigQuery creando la tabla y agregando los datos en caso de que no exista o solo agregando los datos en caso de que la tabla exista.
El código utilizado para este proceso se encuentra dentro de la carpeta Web Scraping/main.py y además contiene el schema de la tabla en formato .yaml
El procedimiento se puede observar en el siguiente enlace https://www.youtube.com/watch?v=TAWDnpM6xTM

## Carga Incremental

Para la carga incremental de la misma forma se uso las mismas tecnologias Google Cloud Storage, Cloud Functions y BigQuery, en donde el archivo que se sube debe tener por nombre la tabla en la cual se quiere realizar la carga incremental y si se subira varios archivos que hacen referencia a una tabla solamente se puede poner un guión y la fecha para no ocacionar conflictos, una vez subido los datos estos seran validados primeramente para poder ser enviados a BigQuery

Para ver el funcionamiento de la carga inicial y carga incremental se realizo un video en donde se muestra todo el proceso y se encuentra en el siguiente enlace.
https://youtu.be/Trp1KBe-zFM

## Deployment

Para el deployment y puesta en producción el modelo de Machine Learning en GCP se usará las tecnologias de Cloud SDK y App Engine. Para ello se instalará el SDK de Google Cloud Platform donde se ejecutarán los comandos de GCP para dicho proceso. Luego de tener instalado el SDK proseguiremos con la ejecución de los siguientes comandos:

*   Instalar GoogleCloudSDK
    (https://cloud.google.com/sdk/docs/install)
*   Ejecutar en la terminal:

$ gcloud init
$ gcloud app deploy app.yaml --project "Nombre del proyecto"

Nota: Para este caso el "Nombre del Proyecto" es: onyx-park-409513

Una vez ejecutados los comandos se crea de manera automatica un instancia en App Engine y un bucket en Cloud Storage, donde uno mantendrá la puesta en marcha y las condiciones de la arquitectura de la aplicación y la otra guardará las llamadas o usos de la aplicación, respectivamente. En el siguiente link es de caracter público y podrán ver su producción mediante Streamlit https://apiproyectoyelp.uc.r.appspot.com/

