import tensorflow as tf
import numpy as np
# import tensorflow_converter as tfc

celsius = np.array([-40,-10,0,8,15,22,38], dtype=float)
fahrenheit = np.array([-40,14,32,46,59,72,100], dtype=float)

# capa = tf.keras.layers.Dense(units=1,input_shape=[1])
# modelo = tf.keras.Sequential([capa])

oculta1 = tf.keras.layers.Dense(units=3,input_shape=[1]) 
oculta2 = tf.keras.layers.Dense(units=3)
oculta3 = tf.keras.layers.Dense(units=5)
salida = tf.keras.layers.Dense(units=1)
modelo = tf.keras.Sequential([oculta1,oculta2,oculta3,salida])


modelo.compile(
    optimizer = tf.keras.optimizers.Adam(0.1),
    loss = 'mean_squared_error'
)
print("comienzo");
historial = modelo.fit(celsius, fahrenheit,epochs = 1000, verbose=False)
print("Termino")

resultado = modelo.predict([125.0])
print("resultado" + str(resultado))

modelo.save('celsius_a_fahrenheit.h5');
