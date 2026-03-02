# Importamos las clases necesarias
from modelos.producto import Producto
from servicios.inventario import Inventario


def mostrar_menu():
    """
    Muestra las opciones disponibles del sistema.
    """
    print("\n--- SISTEMA DE INVENTARIO ---")
    print("1. Añadir producto")
    print("2. Eliminar producto")
    print("3. Actualizar producto")
    print("4. Buscar producto")
    print("5. Listar inventario")
    print("6. Salir")


def pedir_int(mensaje):
    """
    Pide un entero al usuario. Repite hasta que sea válido.
    """
    while True:
        valor = input(mensaje).strip()
        try:
            return int(valor)
        except ValueError:
            print("❌ Error: Debe introducir un número entero válido.")


def pedir_float(mensaje):
    """
    Pide un float al usuario. Repite hasta que sea válido.
    """
    while True:
        valor = input(mensaje).strip()
        try:
            return float(valor)
        except ValueError:
            print("❌ Error: Debe introducir un número válido (ej: 10.50).")


def main():
    """
    Función principal del programa.
    Aquí se ejecuta el menú interactivo.
    """

    # Creamos una instancia del inventario (carga automáticamente el archivo)
    inventario = Inventario()

    # Bucle infinito hasta que el usuario decida salir
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        # ------------------------------------------------
        # OPCIÓN 1: AÑADIR PRODUCTO
        # ------------------------------------------------
        if opcion == "1":
            id_producto = input("ID: ").strip()
            nombre = input("Nombre: ").strip()
            cantidad = pedir_int("Cantidad: ")
            precio = pedir_float("Precio: ")

            try:
                producto = Producto(id_producto, nombre, cantidad, precio)
                inventario.agregar_producto(producto)
            except Exception as e:
                print(f"❌ Error al crear el producto: {e}")

        # ------------------------------------------------
        # OPCIÓN 2: ELIMINAR PRODUCTO
        # ------------------------------------------------
        elif opcion == "2":
            id_producto = input("ID del producto a eliminar: ").strip()
            inventario.eliminar_producto(id_producto)

        # ------------------------------------------------
        # OPCIÓN 3: ACTUALIZAR PRODUCTO
        # ------------------------------------------------
        elif opcion == "3":
            id_producto = input("ID del producto a actualizar: ").strip()

            cantidad_txt = input("Nueva cantidad (dejar vacío si no desea cambiar): ").strip()
            precio_txt = input("Nuevo precio (dejar vacío si no desea cambiar): ").strip()

            # Convertimos solo si el usuario introduce valor
            cantidad = None
            precio = None

            try:
                if cantidad_txt != "":
                    cantidad = int(cantidad_txt)
                if precio_txt != "":
                    precio = float(precio_txt)

                # Si el usuario no cambió nada, avisamos
                if cantidad is None and precio is None:
                    print("⚠️ No ingresó cambios (cantidad ni precio).")
                else:
                    inventario.actualizar_producto(id_producto, cantidad, precio)

            except ValueError:
                print("❌ Error: valores inválidos. Ejemplo cantidad=5, precio=10.50")

        # ------------------------------------------------
        # OPCIÓN 4: BUSCAR PRODUCTO
        # ------------------------------------------------
        elif opcion == "4":
            nombre = input("Nombre a buscar: ").strip()
            resultados = inventario.buscar_por_nombre(nombre)

            if resultados:
                print("\n🔎 Resultados encontrados:")
                for p in resultados:
                    print(p)
            else:
                print("No se encontraron productos.")

        # ------------------------------------------------
        # OPCIÓN 5: MOSTRAR INVENTARIO
        # ------------------------------------------------
        elif opcion == "5":
            inventario.mostrar_inventario()

        # ------------------------------------------------
        # OPCIÓN 6: SALIR
        # ------------------------------------------------
        elif opcion == "6":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida.")


# Punto de entrada del programa
if __name__ == "__main__":
    main()