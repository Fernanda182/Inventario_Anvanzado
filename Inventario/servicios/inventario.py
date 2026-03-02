# servicios/inventario.py
from modelos.producto import Producto


class Inventario:
    """
    Inventario con persistencia en archivo inventario.txt (formato CSV con ';').

    - Al iniciar: carga automáticamente el archivo.
    - Al agregar/actualizar/eliminar: guarda automáticamente los cambios.
    - Maneja excepciones: FileNotFoundError, PermissionError, OSError.
    - Tolera archivo "corrupto": ignora líneas inválidas y avisa.

    Colecciones usadas:
    - dict: productos {id: Producto} para acceso rápido por ID
    - set:  ids para verificar unicidad rápidamente
    - list: resultados en búsquedas por nombre
    """

    def __init__(self, ruta_archivo: str = "inventario.txt"):
        self.ruta_archivo = ruta_archivo
        self.productos = {}     # id_producto(str) -> Producto
        self.ids = set()        # set de IDs para unicidad rápida
        self._cargar_desde_archivo()

    # ---------------------------
    # Persistencia en archivo
    # ---------------------------
    def _cargar_desde_archivo(self):
        """
        Carga productos desde inventario.txt.
        Si no existe, lo crea vacío.
        Si hay líneas corruptas, las ignora y lo notifica.
        """
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                self.productos.clear()
                self.ids.clear()
                corruptas = 0
                duplicadas = 0

                for n_linea, linea in enumerate(f, start=1):
                    linea = linea.strip()
                    if not linea:
                        continue

                    try:
                        producto = Producto.from_linea(linea)
                        pid = producto.get_id()

                        # Evitar IDs duplicados dentro del archivo
                        if pid in self.ids:
                            duplicadas += 1
                            continue

                        self.productos[pid] = producto
                        self.ids.add(pid)

                    except Exception:
                        corruptas += 1
                        continue

                if corruptas > 0 or duplicadas > 0:
                    print(
                        f"⚠️ Inventario cargado con novedades: "
                        f"{corruptas} línea(s) corrupta(s) ignorada(s) y "
                        f"{duplicadas} ID(s) duplicado(s) ignorado(s)."
                    )
                else:
                    print("📁 Inventario cargado correctamente desde el archivo.")

        except FileNotFoundError:
            # Si no existe, lo creamos vacío
            try:
                with open(self.ruta_archivo, "w", encoding="utf-8") as f:
                    pass
                print("📁 El archivo no existía. Se creó inventario.txt vacío.")
            except PermissionError:
                print("❌ ERROR: No hay permisos para crear el archivo inventario.txt.")
            except OSError as e:
                print(f"❌ ERROR inesperado al crear el archivo: {e}")

        except PermissionError:
            print("❌ ERROR: No hay permisos para leer inventario.txt.")
        except OSError as e:
            print(f"❌ ERROR inesperado al leer el archivo: {e}")

    def _guardar_a_archivo(self) -> bool:
        """
        Guarda TODO el inventario reescribiendo inventario.txt.
        Retorna True si pudo guardar, False si falló.
        """
        try:
            with open(self.ruta_archivo, "w", encoding="utf-8") as f:
                for p in self.productos.values():
                    f.write(p.to_linea() + "\n")
            return True

        except PermissionError:
            print("❌ ERROR: No hay permisos para escribir en inventario.txt.")
            return False
        except OSError as e:
            print(f"❌ ERROR inesperado al escribir el archivo: {e}")
            return False

    # ---------------------------
    # Operaciones del inventario
    # ---------------------------
    def agregar_producto(self, producto: Producto) -> bool:
        """
        Agrega un producto y lo persiste en archivo.
        Si falla la escritura, revierte el cambio en memoria.
        """
        pid = producto.get_id().strip()

        if pid in self.ids:
            print("❌ Ya existe un producto con ese ID.")
            return False

        self.productos[pid] = producto
        self.ids.add(pid)

        if self._guardar_a_archivo():
            print("✅ Producto añadido y guardado en inventario.txt correctamente.")
            return True
        else:
            del self.productos[pid]
            self.ids.remove(pid)
            print("❌ No se pudo guardar en archivo. Operación revertida.")
            return False

    def eliminar_producto(self, id_producto: str) -> bool:
        """
        Elimina un producto y lo persiste en archivo.
        Si falla la escritura, revierte el cambio.
        """
        id_producto = id_producto.strip()

        if id_producto not in self.ids:
            print("❌ No existe un producto con ese ID.")
            return False

        respaldo = self.productos[id_producto]
        del self.productos[id_producto]
        self.ids.remove(id_producto)

        if self._guardar_a_archivo():
            print("✅ Producto eliminado y cambios guardados en inventario.txt.")
            return True
        else:
            self.productos[id_producto] = respaldo
            self.ids.add(id_producto)
            print("❌ No se pudo guardar en archivo. Operación revertida.")
            return False

    def actualizar_producto(self, id_producto: str, cantidad=None, precio=None) -> bool:
        """
        Actualiza cantidad y/o precio y guarda en archivo.
        Si falla la escritura, revierte a los valores anteriores.
        """
        id_producto = id_producto.strip()

        if id_producto not in self.ids:
            print("❌ No existe un producto con ese ID.")
            return False

        producto = self.productos[id_producto]

        # Respaldo
        cantidad_anterior = producto.get_cantidad()
        precio_anterior = producto.get_precio()

        # Cambios
        if cantidad is not None:
            producto.set_cantidad(cantidad)
        if precio is not None:
            producto.set_precio(precio)

        if self._guardar_a_archivo():
            print("✅ Producto actualizado y cambios guardados en inventario.txt.")
            return True
        else:
            # Revertimos
            producto.set_cantidad(cantidad_anterior)
            producto.set_precio(precio_anterior)
            print("❌ No se pudo guardar en archivo. Operación revertida.")
            return False

    def buscar_por_nombre(self, nombre: str):
        """
        Busca productos cuyo nombre contenga el texto indicado (no sensible a mayúsculas).
        Retorna una lista de Productos.
        """
        nombre = nombre.lower().strip()
        resultados = []

        if not nombre:
            return resultados

        for p in self.productos.values():
            if nombre in p.get_nombre().lower():
                resultados.append(p)

        return resultados

    def obtener_todos(self):
        """
        Devuelve una lista de tuplas para mostrar (id, nombre, cantidad, precio).
        Útil para imprimir en tabla desde main.py.
        """
        filas = []
        for p in self.productos.values():
            filas.append((p.get_id(), p.get_nombre(), p.get_cantidad(), p.get_precio()))
        return filas

    def mostrar_inventario(self):
        """
        Muestra todo el inventario en consola.
        """
        filas = self.obtener_todos()

        if not filas:
            print("📦 Inventario vacío.")
            return

        print("\n" + "-" * 60)
        print(f"{'ID':<10} {'NOMBRE':<25} {'CANT':<8} {'PRECIO':<10}")
        print("-" * 60)
        for (pid, nombre, cant, precio) in filas:
            print(f"{pid:<10} {nombre:<25} {cant:<8} $ {precio:<10.2f}")
        print("-" * 60 + "\n")