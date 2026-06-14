from modelo.vehiculoDao import VehiculoDao

class VehiculoController:
    def __init__(self):
        self.dao = VehiculoDao()

    def crear_vehiculo(self, vehiculo):
        # Validar placa única
        vehiculos = self.dao.obtener_todos()
        for v in vehiculos:
            if v[1] == vehiculo.placa:
                raise ValueError("Ya existe un vehículo con esa placa.")
        return self.dao.crear_vehiculo(vehiculo)

    def obtener_vehiculo(self, id_vehiculo):
        return self.dao.obtener_vehiculo(id_vehiculo)

    def obtener_todos(self):
        return self.dao.obtener_todos()

    def actualizar_vehiculo(self, id_vehiculo, placa, marca, modelo, color, id_cliente, id_taller):
        # Validar placa única al actualizar
        vehiculos = self.dao.obtener_todos()
        for v in vehiculos:
            if v[1] == placa and v[0] != id_vehiculo:
                raise ValueError("Ya existe un vehículo con esa placa.")
        return self.dao.actualizar_vehiculo(id_vehiculo, placa, marca, modelo, color, id_cliente, id_taller)

    def borrar_vehiculo(self, id_vehiculo):
        return self.dao.borrar_vehiculo(id_vehiculo)