import tkinter as tk

# Creamos la ventana principal
root = tk.Tk()

# Creamos el menú
menu = tk.Menu(root)

# Agregamos opciones al menú
archivo = tk.Menu(menu)
archivo.add_command(label="Abrir")
archivo.add_command(label="Guardar")
archivo.add_separator()
archivo.add_command(label="Salir", command=root.quit)

opciones = tk.Menu(menu)
opciones.add_command(label="Opción 1")
opciones.add_command(label="Opción 2")

# Agregamos los menús al menú principal
menu.add_cascade(label="Archivo", menu=archivo)
menu.add_cascade(label="Opciones", menu=opciones)

# Configuramos la ventana principal para que use el menú
root.config(menu=menu)

# Ejecutamos el bucle principal de la aplicación
root.mainloop()