from modelo.clienteDao import ClienteDao

class ClienteController:
    def __init__(self):
        self.dao = ClienteDao()

    def crear_cliente(self, cliente):
        # Validación: correo único (ejemplo)
        clientes = self.dao.obtener_todos()
        for c in clientes:
            if c[4] == cliente.correo:
                raise ValueError("El correo ya está registrado.")
        return self.dao.crear_cliente(cliente)

    def obtener_cliente(self, id_cliente):
        return self.dao.obtener_cliente(id_cliente)

    def obtener_todos(self):
        return self.dao.obtener_todos()

    def actualizar_cliente(self, id_cliente, nombre, apellido, telefono, correo):
        # Validación: correo único al actualizar
        clientes = self.dao.obtener_todos()
        for c in clientes:
            if c[4] == correo and c[0] != id_cliente:
                raise ValueError("El correo ya está registrado.")
        return self.dao.actualizar_cliente(id_cliente, nombre, apellido, telefono, correo)

    def borrar_cliente_taller(self, id_cliente, id_taller):
        return self.dao.borrar_cliente_taller(id_cliente, id_taller)
    def borrar_cliente(self, id_cliente):
        return self.dao.borrar_cliente(id_cliente)