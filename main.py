import requests
import flet as ft

# Función para consumir la API
def obtener_datos_api(endpoint):
    url = f"http://localhost:4000/api/{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print("Error al decodificar JSON")
            return None
    else:
        print("Error al obtener los datos:", response.status_code)
        return None

# Función para construir la lista de datos en formato de columnas
def construir_lista(datos, tipo):
    if tipo == 'estudiantes':
        headers = ["ID", "Nombre", "Apellido", "Dirección"]
        rows = [[str(item.get('id', 'N/A')), item.get('nombre', 'Nombre no disponible'),
                 item.get('apellido', 'Apellido no disponible'), item.get('direccion', 'Dirección no disponible')]
                for item in datos]
    elif tipo == 'profesores':
        headers = ["DNI", "Nombre", "Apellido", "Asignatura"]
        rows = [[item.get('dni', 'DNI no disponible'), item.get('nombre', 'Nombre no disponible'),
                 item.get('apellido', 'Apellido no disponible'), item.get('Asignatura', 'Asignatura no disponible')]
                for item in datos]
    else:
        headers = ["Error"]
        rows = [["Formato de datos inesperado"]]
    
    # Creo la cabecera
    lista_datos = [
        ft.Row([
            ft.Text(header, weight='bold', width=150) for header in headers
        ], alignment='center')
    ]

    # Creo las filas de datos
    for row in rows:
        lista_datos.append(
            ft.Row([
                ft.Text(celda, width=150) for celda in row
            ], alignment='center')
        )
    
    return lista_datos

# Función que se ejecuta al presionar los botones
def cargar_datos(page, endpoint):
    datos = obtener_datos_api(endpoint)
    print("Datos recibidos:", datos)  # Imprime los datos para inspeccionar
    
    # Limpiar el contenedor de datos antes de agregar nuevos datos
    page.controls[2].controls.clear()  # Limpiar el contenedor de datos
    
    if datos:
        if isinstance(datos, dict) and 'body' in datos:
            datos = datos['body']  
        if isinstance(datos, list):
            lista_datos = construir_lista(datos, endpoint)
            page.controls[2].controls.extend(lista_datos)
        else:
            page.controls[2].controls.append(ft.Text("Formato de datos inesperado: " + str(type(datos))))
    else:
        page.controls[2].controls.append(ft.Text("Error al cargar los datos"))

    page.update()

# Función principal de Flet
def main(page: ft.Page):
    page.title = "Consumo de API en Flet"

    # Crear el contenedor para los datos
    global datos_container
    datos_container = ft.Column()  # Contenedor vacío para los datos

    # Crear los botones
    btn_estudiantes = ft.ElevatedButton("Cargar Estudiantes", on_click=lambda _: cargar_datos(page, "estudiantes"))
    btn_profesores = ft.ElevatedButton("Cargar Profesores", on_click=lambda _: cargar_datos(page, "profesores"))

    # Agregar botones y contenedor a la página
    page.controls.extend([btn_estudiantes, btn_profesores, datos_container])
    page.update()

    # Mantener los botones fijos 
    page.scroll = True

# Ejecutar la aplicación Flet
ft.app(target=main)
