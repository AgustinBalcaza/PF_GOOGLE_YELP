<H1 align="left">Diagrama Entidad Relación</H1>

<img src="../assets/Diagrama_ER.png" alt="Descripción de la imagen" width="1760" height="800">

EL diagrama está compuesto por 6 entidades: Category, Busines, Reviews, User, City y State mas una entidad de relación denominada Category_Business la cual relaciona las categorías con los negocios. Cada una de ellas posee los atributos relacionados a la característica de los datos que maneja junto con las notaciones de las llaves primarias y foráneas. 

El diagrama incluye todos los datos filtrados y combinados de las fuentes de Google Maps y Yelp.


<H1 align="left">Diccionario de datos</H1>

<img src="./assets/Dicc_datos.jpg" alt="Descripción de la imagen" width="707" height="431">

El diccionario de datos contiene todos los tipos de datos de la combinación de las fuentes de Google y Yelp.

A continuación se muestra un resumen por tipo de dato.


Business Name (Nombre del Negocio):
Tipo de Dato: String
Descripción: Nombre del negocio.
Ejemplo: Hotel Indigo Nashville
state (Nombre del Estado):

Tipo de Dato: String
Descripción: Nombre del estado.
Ejemplo: Nevada
city (Nombre de la Ciudad):

Tipo de Dato: String
Descripción: Nombre de la ciudad.
Ejemplo: Nashville
Latitude (Latitud):

Tipo de Dato: Decimal
Descripción: Coordenada de latitud.
Ejemplo: 36.152989
Longitude (Longitud):

Tipo de Dato: Decimal
Descripción: Coordenada de longitud.
Ejemplo: -86.795709
category (Categoría del Negocio):

Tipo de Dato: String
Descripción: Categoría a la que pertenece el negocio.
Ejemplo: Hotel
avg_ratings (Valoración Promedio):

Tipo de Dato: Float
Descripción: Valoración promedio del negocio.
Ejemplo: 3.0
sentiment analysis (Análisis de Sentimiento):

Tipo de Dato: Small Int
Descripción: Resultado del análisis de sentimiento.
Ejemplo: 2
year (Año de la Review):

Tipo de Dato: Small Int
Descripción: Año en que se realizó la reseña.
Ejemplo: 2009
month (Mes de la Review):

Tipo de Dato: Small Int
Descripción: Mes en que se realizó la reseña.
Ejemplo: 4
user_id (ID del Usuario):

Tipo de Dato: Int
Descripción: Identificación única del usuario.
Ejemplo: 21122
review_id (ID de la Reseña):

Tipo de Dato: Int
Descripción: Identificación única de la reseña.
Ejemplo: 68896
business_Id (ID del Negocio):

Tipo de Dato: Small Int
Descripción: Identificación única del negocio.
Ejemplo: 1571
state_id (ID del Estado):

Tipo de Dato: Small Int
Descripción: Identificación única del estado.
Ejemplo: 3
city_Id (ID de la Ciudad):

Tipo de Dato: Small Int
Descripción: Identificación única de la ciudad.
Ejemplo: 521
category_Id (ID de la Categoría):

Tipo de Dato: Small Int
Descripción: Identificación única de la categoría del negocio.
Ejemplo: 2
