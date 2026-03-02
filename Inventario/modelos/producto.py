class Producto:
    """
    Clase que representa un producto dentro del sistema de inventario.

    Aplicamos encapsulamiento haciendo que los atributos sean privados
    (doble guion bajo __). De esta forma, solo se pueden modificar
    mediante métodos controlados (getters y setters).
    """

    def __init__(self, id_producto, nombre, cantidad, precio):
        """
        Constructor de la clase Producto.

        Parámetros:
        - id_producto: identificador único del producto.
        - nombre: nombre del producto.
        - cantidad: cantidad disponible en inventario (int >= 0).
        - precio: precio unitario del producto (float >= 0).
        """

        # Atributos privados
        self.__id = str(id_producto).strip()
        self.__nombre = str(nombre).strip()

        # Validaciones usando setters para centralizar control
        self.set_cantidad(cantidad)
        self.set_precio(precio)

        if not self.__id:
            raise ValueError("El ID del producto no puede estar vacío.")
        if not self.__nombre:
            raise ValueError("El nombre del producto no puede estar vacío.")

    # ---------------------------
    # MÉTODOS GETTERS
    # ---------------------------

    def get_id(self):
        """Devuelve el ID del producto."""
        return self.__id

    def get_nombre(self):
        """Devuelve el nombre del producto."""
        return self.__nombre

    def get_cantidad(self):
        """Devuelve la cantidad disponible."""
        return self.__cantidad

    def get_precio(self):
        """Devuelve el precio del producto."""
        return self.__precio

    # ---------------------------
    # MÉTODOS SETTERS
    # ---------------------------

    def set_nombre(self, nombre):
        """
        Modifica el nombre del producto.
        """
        nombre = str(nombre).strip()
        if nombre:
            self.__nombre = nombre
        else:
            print("El nombre no puede estar vacío.")

    def set_cantidad(self, cantidad):
        """
        Modifica la cantidad del producto.
        Se valida que la cantidad no sea negativa y sea entero.
        """
        try:
            cantidad = int(cantidad)
        except (ValueError, TypeError):
            print("La cantidad debe ser un número entero.")
            return

        if cantidad >= 0:
            self.__cantidad = cantidad
        else:
            print("La cantidad no puede ser negativa.")

    def set_precio(self, precio):
        """
        Modifica el precio del producto.
        Se valida que el precio no sea negativo y sea numérico.
        """
        try:
            precio = float(precio)
        except (ValueError, TypeError):
            print("El precio debe ser un número (ej: 10.50).")
            return

        if precio >= 0:
            self.__precio = precio
        else:
            print("El precio no puede ser negativo.")

    # ---------------------------
    # MÉTODOS PARA ARCHIVOS
    # ---------------------------

    def to_linea(self):
        """
        Convierte el producto a una línea para guardarlo en archivo.
        Formato: id;nombre;cantidad;precio
        """
        return f"{self.__id};{self.__nombre};{self.__cantidad};{self.__precio}"

    @staticmethod
    def from_linea(linea):
        """
        Crea un Producto desde una línea del archivo.
        Espera formato: id;nombre;cantidad;precio
        """
        partes = linea.strip().split(";")
        if len(partes) != 4:
            raise ValueError("Línea inválida: no tiene 4 campos (id;nombre;cantidad;precio).")

        id_producto = partes[0].strip()
        nombre = partes[1].strip()
        cantidad = int(partes[2].strip())
        precio = float(partes[3].strip())

        return Producto(id_producto, nombre, cantidad, precio)

    # ---------------------------
    # MÉTODO ESPECIAL
    # ---------------------------

    def __str__(self):
        """
        Método especial que define cómo se muestra el objeto
        cuando lo imprimimos con print().
        """
        return (
            f"ID: {self.__id} | Nombre: {self.__nombre} | "
            f"Cantidad: {self.__cantidad} | Precio: {self.__precio:.2f}€"
        )