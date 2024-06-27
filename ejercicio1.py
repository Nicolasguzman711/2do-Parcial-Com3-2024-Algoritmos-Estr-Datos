import os
import pickle
import random
from datetime import date

class Fecha:
    def _init_(self, dd=None, mm=None, aaaa=None):
        if dd is None or mm is None or aaaa is None:
            hoy = date.today()
            self.dd = hoy.day
            self.mm = hoy.month
            self.aaaa = hoy.year
        else:
            self.dd = dd
            self.mm = mm
            self.aaaa = aaaa
    
    def _str_(self):
        return f"{self.dd:02d}/{self.mm:02d}/{self.aaaa}"
    
    def _eq_(self, other):
        return (self.dd == other.dd) and (self.mm == other.mm) and (self.aaaa == other.aaaa)
    
    def calcular_diferencia(self, otra_fecha):
        fecha_self = date(self.aaaa, self.mm, self.dd)
        fecha_otra = date(otra_fecha.aaaa, otra_fecha.mm, otra_fecha.dd)
        diferencia = abs(fecha_self - fecha_otra).days
        return diferencia

class Alumno:
    def _init_(self, nombre, dni, fecha_ingreso, carrera):
        self.nombre = nombre
        self.dni = dni
        self.fecha_ingreso = fecha_ingreso
        self.carrera = carrera
    
    def _str_(self):
        return f"Alumno: {self.nombre} - DNI: {self.dni} - Carrera: {self.carrera}"

    def obtener_fecha_ingreso(self):
        return self.fecha_ingreso

class Nodo:
    def _init_(self, alumno=None):
        self.alumno = alumno
        self.siguiente = None
        self.anterior = None

class ListaDoblementeEnlazada:
    def _init_(self):
        self.cabeza = None
        self.cola = None
        self.longitud = 0
    
    def esta_vacia(self):
        return self.longitud == 0
    
    def agregar_al_final(self, alumno):
        nuevo_nodo = Nodo(alumno)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo
        self.longitud += 1
    
    def lista_ejemplo(self, cantidad):
        for _ in range(cantidad):
            nombre = f"Alumno_{random.randint(1, 100)}"
            dni = random.randint(10000000, 99999999)
            fecha_ingreso = Fecha(random.randint(1, 28), random.randint(1, 12), random.randint(2000, 2023))
            carrera = random.choice(["Ingeniería Informática", "Medicina", "Derecho", "Arquitectura"])
            alumno = Alumno(nombre, dni, fecha_ingreso, carrera)
            self.agregar_al_final(alumno)
    
    def obtener_lista_alumnos(self):
        lista_alumnos = []
        current = self.cabeza
        while current is not None:
            alumno = current.alumno
            datos_alumno = {
                "nombre": alumno.nombre,
                "dni": alumno.dni,
                "fecha_ingreso": alumno.fecha_ingreso,
                "carrera": alumno.carrera
            }
            lista_alumnos.append(datos_alumno)
            current = current.siguiente
        return lista_alumnos
    
    def _iter_(self):
        return IteradorLista(self)
    
    def iterar_inicio(self):
        return IteradorLista(self, sentido="inicio")
    
    def iterar_fin(self):
        return IteradorLista(self, sentido="fin")
    
    def ordenar_por_fecha_ingreso(self):
        if self.longitud < 2:
            return
        
        current = self.cabeza.siguiente
        while current is not None:
            alumno_actual = current.alumno
            pos = current
            
            while pos.anterior is not None and alumno_actual.obtener_fecha_ingreso().calcular_diferencia(pos.anterior.alumno.obtener_fecha_ingreso()) < 0:
                pos.alumno = pos.anterior.alumno
                pos = pos.anterior
            
            pos.alumno = alumno_actual
            current = current.siguiente

class IteradorLista:
    def _init_(self, lista, sentido="inicio"):
        self.lista = lista
        if sentido == "inicio":
            self.actual = lista.cabeza
        else:
            self.actual = lista.cola
    
    def _iter_(self):
        return self
    
    def _next_(self):
        if self.actual is None:
            raise StopIteration
        else:
            alumno = self.actual.alumno
            if self.actual.anterior is not None:
                self.actual = self.actual.anterior
            else:
                self.actual = None
            return alumno

def crear_directorio_y_guardar(lista_alumnos, path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        
        datos_alumnos = lista_alumnos.obtener_lista_alumnos()
        
        with open(os.path.join(path, "lista_alumnos.dat"), "wb") as f:
            pickle.dump(datos_alumnos, f)
        
        print(f"Lista de alumnos guardada en {path}/lista_alumnos.dat")
    except Exception as e:
        print(f"Error al crear directorio y guardar archivo: {e}")

def mover_directorio_y_borrar(path_origen, path_destino):
    try:
        os.rename(path_origen, path_destino)
        print(f"Directorio movido de {path_origen} a {path_destino}")
        
        archivo_a_borrar = os.path.join(path_destino, "lista_alumnos.dat")
        os.remove(archivo_a_borrar)
        os.rmdir(path_destino)
        
        print(f"Archivo {archivo_a_borrar} y directorio {path_destino} eliminados.")
    except Exception as e:
        print(f"Error al mover directorio y borrar archivos: {e}")



        lista_alumnos = ListaDoblementeEnlazada()
lista_alumnos.lista_ejemplo(5)


print("Lista de alumnos antes de ordenar:")
for alumno in lista_alumnos:
    print(alumno)


lista_alumnos.ordenar_por_fecha_ingreso()


print("\nLista de alumnos después de ordenar:")
for alumno in lista_alumnos:
    print(alumno)


directorio_origen = "./directorio_origen"
directorio_destino = "./directorio_destino"


crear_directorio_y_guardar(lista_alumnos, directorio_origen)
mover_directorio_y_borrar(directorio_origen, directorio_destino)