from modelo.servicioDao import ServicioDao

class ServicioController:
    def __init__(self):
        self.dao = ServicioDao()

    def crear_servicio(self, servicio):
        # Validar nombre único por taller
        servicios = self.dao.obtener_todos()
        for s in servicios:
            if s[1] == servicio.nombre and s[4] == servicio.id_taller:
                raise ValueError("Ya existe un servicio con ese nombre en este taller.")
        return self.dao.crear_servicio(servicio)

    def obtener_servicio(self, id_servicio):
        servicios = self.dao.obtener_todos()
        for s in servicios:
            if s[0] == id_servicio:
                return s
        return None

    def obtener_todos(self):
        return self.dao.obtener_todos()

    def actualizar_servicio(self, id_servicio, nombre, descripcion, costo, id_taller):
        # Validar nombre único por taller al actualizar
        servicios = self.dao.obtener_todos()
        for s in servicios:
            if s[1] == nombre and s[4] == id_taller and s[0] != id_servicio:
                raise ValueError("Ya existe un servicio con ese nombre en este taller.")
        return self.dao.actualizar_servicio(id_servicio, nombre, descripcion, costo)

    def borrar_servicio(self, id_servicio):
        return self.dao.borrar_servicio(id_servicio)