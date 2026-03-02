# Sistema Avanzado de Gestión de Inventario 

## Autor: Fernanda Vaca

## Descripción
Sistema en consola para gestionar productos de una tienda usando Programación Orientada a Objetos (POO),
colecciones de Python y persistencia en archivos.

Permite:
- Añadir productos
- Eliminar productos por ID
- Actualizar cantidad y/o precio
- Buscar productos por nombre
- Listar todo el inventario

## Estructura del proyecto
- `modelos/` contiene la clase `Producto`
- `servicios/` contiene la lógica del `Inventario`
- `inventario.txt` almacena la información de forma persistente
- `main.py` contiene el menú interactivo

## Colecciones utilizadas
- `dict`: almacena productos por ID para acceso rápido.
- `set`: controla IDs únicos.
- `list`: se usa para devolver resultados en búsquedas por nombre.
- `tuple`: se usa para devolver filas de datos para impresión ordenada.

## Persistencia en archivos
El inventario se guarda en `inventario.txt` con el formato:
`id;nombre;cantidad;precio`

Se implementa:
- **Serialización**: convertir un producto a texto para guardarlo.
- **Deserialización**: reconstruir el producto desde el archivo al iniciar el programa.

## Ejecución
En la terminal, dentro de la carpeta del proyecto:
