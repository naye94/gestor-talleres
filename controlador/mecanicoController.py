from modelo.mecanicoDao import MecanicoDao

class MecanicoController:
    def __init__(self):
        self.dao = MecanicoDao()

    def crear_mecanico(self, mecanico):
        # Validar teléfono único
        mecanicos = self.dao.obtener_todos()
        for m in mecanicos:
            if m[4] == mecanico.telefono:
                raise ValueError("Ya existe un mecánico con ese teléfono.")
        return self.dao.crear_mecanico(mecanico)

    def obtener_mecanico(self, id_mecanico):
        mecanicos = self.dao.obtener_todos()
        for m in mecanicos:
            if m[0] == id_mecanico:
                return m
        return None

    def obtener_todos(self):
        return self.dao.obtener_todos()

    def actualizar_mecanico(self, id_mecanico, nombre, apellido, especialidad, telefono):
        # Validar teléfono único al actualizar
        mecanicos = self.dao.obtener_todos()
        for m in mecanicos:
            if m[4] == telefono and m[0] != id_mecanico:
                raise ValueError("Ya existe un mecánico con ese teléfono.")
        return self.dao.actualizar_mecanico(id_mecanico, nombre, apellido, especialidad, telefono)

    def eliminar_mecanico(self, id_mecanico):
        return self.dao.eliminar_mecanico(id_mecanico)