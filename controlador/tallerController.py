from modelo.tallerDao import TallerDao

class TallerController:
    def __init__(self):
        self.dao = TallerDao()

    def crear_taller(self, taller):
        # Validar nombre único
        talleres = self.dao.obtener_todos()
        for t in talleres:
            if t[1] == taller.nombre:
                raise ValueError("Ya existe un taller con ese nombre.")
        return self.dao.crear_taller(taller)

    def obtener_taller(self, id_taller):
        talleres = self.dao.obtener_todos()
        for t in talleres:
            if t[0] == id_taller:
                return t
        return None

    def obtener_todos(self):
        return self.dao.obtener_todos()

    def actualizar_taller(self, id_taller, nombre, direccion, telefono):
        # Validar nombre único al actualizar
        talleres = self.dao.obtener_todos()
        for t in talleres:
            if t[1] == nombre and t[0] != id_taller:
                raise ValueError("Ya existe un taller con ese nombre.")
        return self.dao.actualizar_taller(id_taller, nombre, direccion, telefono)

    def borrar_taller(self, id_taller):
        return self.dao.borrar_taller(id_taller)