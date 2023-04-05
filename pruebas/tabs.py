import tkinter as tk
from tkinter import ttk
from p1 import add_test_1
from p2 import add_test_2

root = tk.Tk()
root.title("Ejemplo de pestañas")

notebook = ttk.Notebook(root)

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

notebook.add(tab1, text="Pestaña 1")
notebook.add(tab2, text="Pestaña 2")

button_1 = add_test_1(tab1)
button_2 = add_test_2(tab2)
# Agregar widgets a cada pestaña
#tk.Label(tab1, text="Este es el contenido de la Pestaña 1").pack(padx=10, pady=10)
#tk.Label(tab2, text="Este es el contenido de la Pestaña 2").pack(padx=10, pady=10)

button_1.pack(padx=10, pady=10)
button_2.pack(padx=10, pady=10)

notebook.pack(expand=1, fill="both")
root.mainloop()