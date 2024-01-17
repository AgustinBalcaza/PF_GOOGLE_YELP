
## MVP/ Proof of Concept de producto de ML 

Un MVP (Minimum Viable Product) para un producto de machine learning (ML) generalmente implica la creación de una versión simplificada del producto que demuestra la viabilidad y funcionalidad básica de la solución.

### Performance del modelo

Desarrollar un sistema de recomendación que recoge los features de cada  Business name, y sugiere otros 4 negocios acorde a los features similares.

<p align="center">
  <img src="https://github.com/AgustinBalcaza/PF_GOOGLE_YELP/blob/main/ML_Recomendaci%C3%B3n/ML_RECOMEN.png">
</p>

# Informe del modelo de clasificación 
    
Este informe detalla el proceso y los resultados de un modelo de clasificación implementado utilizando redes neuronales con la biblioteca Keras. El objetivo del modelo es predecir las etiquetas de atributos a partir de características como la calificación (stars), la categoría (categoria) y el estado (state) de un conjunto de datos.

## 1. Preprocesamiento de los datos
En esta etapa, se realiza el preprocesamiento de los datos de entrada para prepararlos adecuadamente para el entrenamiento del modelo. Las siguientes acciones se llevan a cabo:

### 1.1. Selección de características

Se seleccionan las características relevantes para el modelo, que son la calificación (stars), la categoría (categoria) y el estado (state). Estas características se extraen del DataFrame original `df` y se almacenan en el DataFrame `X`.

### 1.2. Codificación de variables categóricas

Para poder utilizar las variables categóricas en el modelo, se realiza una codificación mediante la técnica de \"one-hot encoding\". Esto implica convertir las variables categóricas en variables numéricas binarias. En este caso, se aplica `pd.get_dummies(X)` para codificar las variables categóricas en columnas binarias correspondientes a cada categoría.

### 1.3. Codificación de etiquetas

Las etiquetas de atributos (y) se codifican utilizando el codificador de etiquetas (`LabelEncoder()`) de la biblioteca scikit-learn. Esto asigna un valor numérico a cada etiqueta de atributo, lo cual es necesario para el entrenamiento del modelo. Las etiquetas codificadas se almacenan en la variable `y_train_encoded`.
    
## 2. División del conjunto de datos
El conjunto de datos se divide en conjuntos de entrenamiento y prueba para evaluar el rendimiento del modelo. Se utiliza la función `train_test_split()` de scikit-learn para dividir los datos codificados (`X`) y las etiquetas codificadas (`y_train_encoded`) en conjuntos de entrenamiento (`X_train`, `y_train`) y prueba (`X_test`, `y_test`). En este caso, se asigna el 25% de los datos al conjunto de prueba y se utiliza una semilla aleatoria (`random_state`) para garantizar la reproducibilidad de los resultados.

## 3. Definición del modelo

El modelo se define como una secuencia de capas utilizando la API `Sequential` de Keras. El modelo consta de tres capas densas (totalmente conectadas) con funciones de activación ReLU, seguidas de una capa de salida con una función de activación softmax. La capa de entrada tiene una dimensión igual al número de características en los datos de entrenamiento (`X_train.shape[1]`), y la capa de salida tiene una dimensión igual al número máximo de etiquetas codificadas (`np.max(y_train) + 1`).

## 4. Compilación y entrenamiento del modelo

Antes de entrenar el modelo, se debe compilar especificando la función de pérdida (`loss`), el optimizador (`optimizer`) y las métricas que se utilizarán para evaluar el rendimiento del modelo (`metrics`). En este caso, se utiliza la función de pérdida `sparse_categorical_crossentropy` adecuada para problemas de clasificación con múltiples clases. El optimizador seleccionado es `adam`, que es un algoritmo de optimización popular en el aprendizaje profundo.

A continuación, se entrena el modelo utilizando el conjunto de entrenamiento (`X_train`, `y_train`) durante un número determinado de épocas (`epochs`) y un tamaño de lote (`batch_size`). Además, se utiliza una validación cruzada del 20% del conjunto de entrenamiento (`validation_split`) para monitorear el rendimiento del modelo durante el entrenamiento y evitar el sobreajuste.
  
## 5. Evaluación del modelo
   
Una vez finalizado el entrenamiento, se evalúa el rendimiento del modelo utilizando el conjunto de prueba (`X_test`, `y_test`). Se calcula la pérdida (`test_loss`) y la precisión (`test_acc`) del modelo en este conjunto de datos.

Se utilizan las características codificadas del conjunto de prueba (`X_test`) para realizar predicciones con el modelo entrenado. Las predicciones se almacenan en la variable `predictions` y representan las probabilidades de pertenencia a cada clase de atributo.\n",

Este informe describe el proceso de construcción, entrenamiento y evaluación de un modelo de clasificación utilizando redes neuronales. El modelo utiliza las características de calificación, categoría y estado para predecir las etiquetas de atributos. Los resultados obtenidos se basan en las métricas de pérdida y precisión del modelo en el conjunto de prueba.
