from tkinter import *
import numpy as np

# Creamos la ventana
ventana = Tk()
click_counter = 0
# Definimos la función que se ejecutará al hacer click en la ventana
points = []

# Definimos la función para detectar clicks
def detectar_click(event):
    global click_counter, points
    
    # Si el contador es 0, creamos un nuevo punto
    if click_counter == 0:
        points.append([event.x, event.y])
        click_counter += 1
        
    # Si el contador es 1, actualizamos el primer punto
    elif click_counter == 1:
        points.append([event.x, event.y])
        click_counter += 1
        
    # Si el contador es 2, actualizamos el segundo punto
    elif click_counter == 2:
        points.append([event.x, event.y])
        click_counter += 1 
        
    # Si el contador es 3, actualizamos el tercer punto y mostramos los puntos
    elif click_counter == 3:
        points.append([event.x, event.y])
        
        return np.array(points)
        click_counter += 1 
        
    # Si el contador es mayor a 3, no hacemos nada
    else:
        pass
        


# Enlazamos la función con el evento de click de la ventana
ventana.bind("<Button-3>", detectar_click)

# Mostramos la ventana
ventana.mainloop()
