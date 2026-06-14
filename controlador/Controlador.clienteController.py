from controlador.clienteController import ClienteController

def mostrar_clientes():
    controller = ClienteController()
    clientes = controller.obtener_todos()
    print("Listado de clientes:")
    for cliente in clientes:
        # Suponiendo que el cliente es una tupla: (id, nombre, apellido, telefono, correo)
        print(f"ID: {cliente[0]}, Nombre: {cliente[1]}, Apellido: {cliente[2]}, Teléfono: {cliente[3]}, Correo: {cliente[4]}")

if __name__ == "__main__":
    mostrar_clientes()