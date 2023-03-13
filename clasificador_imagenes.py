import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
import math

datos, metadatos = tfds.load('fashion_mnist',as_supervised=True,with_info=True)

datos_entrenamiento, datos_prueba= datos['train'], datos['test']

nombre_clases = metadatos.features['label'].names

# normalizar los datos
# pasar de 0-255 a 0-1
def normalizar(imagenes, etiquetas):
    imagenes = tf.cast(imagenes,tf.float32)
    imagenes /= 255 #pasar de 0-255 a 0-1
    return imagenes, etiquetas


# normalizar los datos de entrenamiento y pruebas con la funcion
datos_entrenamiento = datos_entrenamiento.map(normalizar)
datos_prueba = datos_prueba.map(normalizar)

# Agregar a cache (usar la memoria en lugar de disco, entrenamiento más rápido)
datos_entrenamiento = datos_entrenamiento.cache();
datos_prueba = datos_prueba.cache()

# Mostrar una imagen de los datos de pruebas
for imagen, etiqueta in datos_entrenamiento.take(1):
    break
imagen = imagen.numpy().reshape((28,28))

# creacion del modelo
modelo = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28,28,1)), # 1 - blanco y negro capa de entrada
    tf.keras.layers.Dense(50,activation=tf.nn.relu), # capas ocultas densas
    tf.keras.layers.Dense(50,activation=tf.nn.relu),
    tf.keras.layers.Dense(10,activation=tf.nn.softmax) # capa de salida 
])

# compilar el modelo
modelo.compile(
    optimizer = 'adam',
    loss = tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics = ['accuracy']
)

LOTE = 32
num_entrenamiento = metadatos.splits['train'].num_examples
num_pruebas = metadatos.splits['test'].num_examples

datos_entrenamiento = datos_entrenamiento.repeat().shuffle(num_entrenamiento).batch(LOTE)

# entrenar el modelo
historial = modelo.fit(datos_entrenamiento, epochs=5,steps_per_epoch=math.ceil(num_entrenamiento/LOTE))

# tomar cualquier indice del set de pruebas para cver su prediccion 

imagen1 = imagen[5]
iamgen1 = np.array([imagen1])
prediccion = modelo.predict(imagen1)

print("prediccion: " + nombre_clases[np.argmax(prediccion[0])])
