import os
import json
from tkinter import messagebox
import tkinter as tk

# Nombre del archivo JSON
ARCHIVO_INVENTARIO = "inventario.json"

# Nueva función para mostrar inventario en terminal


def mostrar_inventario_terminal():
    inventario = cargar_inventario()
    print("\n=== Inventario Actual ===")
    for item in inventario:
        print(
            f"ID: {item['id']}, Nombre: {item['nombre']}, Cantidad: {item['cantidad']}")
    print("=========================\n")

# Funciones CRUD con JSON


def cargar_inventario():
    """Carga el inventario desde el archivo JSON."""
    if os.path.exists(ARCHIVO_INVENTARIO):
        with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    else:
        with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as archivo:
            json.dump([], archivo)
        return []


def guardar_inventario(inventario):
    """Guarda el inventario en el archivo JSON."""
    with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as archivo:
        json.dump(inventario, archivo, indent=4, ensure_ascii=False)


def agregar_inventario(nombre, cantidad, ident):
    """Agrega un nuevo elemento al inventario."""
    inventario = cargar_inventario()
    for item in inventario:
        if item["id"] == ident:
            messagebox.showerror(
                title="Error", message=f"El ID '{ident}' ya existe en el inventario."
            )
            return
    inventario.append({"nombre": nombre, "cantidad": cantidad, "id": ident})
    guardar_inventario(inventario)
    mostrar_inventario_terminal()  # Actualiza terminal
    messagebox.showinfo(
        title="Agregar", message=f"Elemento '{nombre}' agregado al inventario."
    )


def modificar_inventario(nombre, cantidad, ident):
    """Modifica un elemento existente en el inventario."""
    inventario = cargar_inventario()
    for item in inventario:
        if item["id"] == ident:
            item["nombre"] = nombre
            item["cantidad"] = cantidad
            guardar_inventario(inventario)
            mostrar_inventario_terminal()  # Actualiza terminal
            messagebox.showinfo(
                title="Modificar", message=f"Elemento '{nombre}' modificado en el inventario."
            )
            return
    messagebox.showerror(
        title="Error", message=f"No se encontró ningún elemento con ID '{ident}'."
    )


def eliminar_inventario(ident):
    """Elimina un elemento del inventario."""
    inventario = cargar_inventario()
    for item in inventario:
        if item["id"] == ident:
            confirmacion = messagebox.askyesno(
                title="Confirmar eliminación",
                message=f"¿Estás seguro de eliminar el elemento con ID '{ident}'?"
            )
            if confirmacion:
                inventario.remove(item)
                guardar_inventario(inventario)
                mostrar_inventario_terminal()  # Actualiza terminal
                messagebox.showinfo(
                    title="Eliminar", message=f"Elemento con ID '{ident}' eliminado."
                )
            return
    messagebox.showerror(
        title="Error", message=f"No se encontró ningún elemento con ID '{ident}'."
    )


# Iniciar Interfaz gráfica
root = tk.Tk()
root.title("Control de inventario")
root.state('zoomed')
root.config(background="#2C3E50")

# Fuentes y colores
custom_font_1 = ("Consolas", 12)
custom_font_2 = ("Consolas", 16)
custom_font_3 = ("Consolas", 20)
custom_font_4 = ("Consolas", 10)
bg_color_1 = "palegreen"
bg_color_2 = "#ECF0F1"

# Labels y Entrys
label_nombre = tk.Label(root, text="Nombre: ",
                        font=custom_font_2, bg=bg_color_1)
entry_nombre = tk.Entry(root, font=custom_font_2)

label_cantidad = tk.Label(root, text="Cantidad: ",
                          font=custom_font_2, bg=bg_color_1)
entry_cantidad = tk.Entry(root, font=custom_font_2)

label_id = tk.Label(root, text="ID: ", font=custom_font_2, bg=bg_color_1)
entry_ident = tk.Entry(root, font=custom_font_2)

label_tip_1 = tk.Label(
    root, text="Recuerde revisar la terminal de Python", font=custom_font_4)

# Botones
btn_agregar = tk.Button(
    root,
    text="Agregar",
    command=lambda: procesar_formulario_inventario("agregar"),
    font=custom_font_3,
    bg=bg_color_2
)

btn_modificar = tk.Button(
    root,
    text="Modificar",
    command=lambda: procesar_formulario_inventario("modificar"),
    font=custom_font_3,
    bg=bg_color_2
)

btn_eliminar = tk.Button(
    root,
    text="Eliminar",
    command=lambda: procesar_formulario_inventario("eliminar"),
    font=custom_font_3,
    bg=bg_color_2
)

btn_limpiar = tk.Button(
    root,
    text="Limpiar campos",
    command=lambda: [entry_nombre.delete(0, tk.END), entry_cantidad.delete(
        0, tk.END), entry_ident.delete(0, tk.END)],
    font=custom_font_3,
    bg=bg_color_2
)

btn_salir = tk.Button(
    root,
    text="Salir de la aplicación",
    command=root.destroy,
    font=custom_font_3,
    bg=bg_color_1
)

# Empaquetado de widgets
label_tip_1.pack(pady=5)
label_nombre.pack(pady=10)
entry_nombre.pack(pady=10)

label_cantidad.pack(pady=10)
entry_cantidad.pack(pady=10)

label_id.pack(pady=10)
entry_ident.pack(pady=10)

btn_agregar.pack(fill="x", pady=10)
btn_modificar.pack(fill="x", pady=10)
btn_eliminar.pack(fill="x", pady=10)
btn_limpiar.pack(fill="x", pady=10)
btn_salir.pack(fill="x", pady=10)


# Procesamiento del formulario


def procesar_formulario_inventario(accion):
    nombre = entry_nombre.get().strip()
    cantidad = entry_cantidad.get().strip()
    ident = entry_ident.get().strip()

    # Validación de campos obligatorios
    if not nombre or not cantidad or not ident:
        messagebox.showwarning(
            title="Advertencia", message="Todos los campos son obligatorios"
        )
        return

    # Validación de tipo de datos
    try:
        cantidad = int(cantidad)
        if cantidad <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            title="Error", message="La cantidad debe ser un número entero positivo"
        )
        return

    # Ejecutar acción específica
    if accion == "agregar":
        agregar_inventario(nombre, cantidad, ident)
    elif accion == "modificar":
        modificar_inventario(nombre, cantidad, ident)
    elif accion == "eliminar":
        eliminar_inventario(ident)


# Mostrar inventario al iniciar la aplicación
mostrar_inventario_terminal()

# Ejecución de la aplicación
root.mainloop()
