#El módulo observador.py permite definir un patrón observador, con el ánimo de notificar a las partes interesadas sobre los
    #distintos eventos que tienen lugar en el objeto funcion_imeb

from datetime import datetime
from os.path import exists
from os import system

#La clase Subject me permite atrapar el objeto a observar y notificar a los observadores acerca de su estado o 
    #comportamiento.
class Subject():

    observadora = []
    observadorb = []
    observadorc = []

    def agregar_a(self, obj):
        self.observadora.append(obj)
    
    def agregar_b(self, obj):
        self.observadorb.append(obj)
    
    def agregar_c(self, obj):
        self.observadorc.append(obj)
    
    def notificar_a(self, *args):
        for observador in self.observadora:
            observador.insertar_a(args)
    
    def notificar_b(self, *args):
        for observador in self.observadorb:
            observador.update_b(args)
    
    def notificar_c(self, *args):
        for observador in self.observadorc:
            observador.del_c(args)
    
#La clase Observador me permite lanzar una excepcion de tipo NotImplementedError
class Observador():
    
    def insertar_a(self, ):
        raise NotImplementedError("Error de no Implementacion")
    
    def update_b(self, ):
        raise NotImplementedError("Error de no Implementacion")
    
    def del_c(self, ):
        raise NotImplementedError("Error de no Implementacion")
    
#Se define concretamente la clase del observador A
class ConcreteObserverA(Observador):

    def __init__(self, obj):
        self.observado_a = obj
        self.observado_a.agregar_a(self)
    
    def insertar_a(self, *args):
        #Se captura la fecha y ahora del evento.
        #Se define el nombre del fichero .log
        d_t = datetime.now()
        observ_str = d_t.strftime('%Y%m%d_%H%M%S')
        file_observ_a = f'observador_a_{observ_str}_insert.log'

        #Si no existe el folder observador, se crea.
        if not exists('observador'):
            system('mkdir observador')
        
        #Se notifica al observador acerca del ingreso de un nuevo producto.
        with open(f'observador/{file_observ_a}','w') as observador_1:
            observador_1.write(f'{datetime.now()}: '"Nuevo registro insertado %s\n" %args)

#Se define concretamente la clase del observador B
class ConcreteObserverB(Observador):

    def __init__(self, obj):
        self.observado_b = obj
        self.observado_b.agregar_b(self)
    
    def update_b(self, *args):
        #Se captura la fecha y ahora del evento.
        #Se define el nombre del fichero .log
        d_t = datetime.now()
        observ_str = d_t.strftime('%Y%m%d_%H%M%S')
        file_observ_b = f'observador_b_{observ_str}_update.log'

        #Si no existe el folder observador, se crea.
        if not exists('observador'):
            system('mkdir observador')
        
        #Se notifica al observador acerca de la actualizacion de un producto existente.
        with open(f'observador/{file_observ_b}','w') as observador_2:
            observador_2.write(f'{datetime.now()}: '"Nuevos datos del registro modificado %s\n" %args)

#Se define concretamente la clase del observador C
class ConcreteObserverC(Observador):

    def __init__(self, obj):
        self.observado_c = obj
        self.observado_c.agregar_c(self)
    
    def del_c(self, *args):
        #Se captura la fecha y ahora del evento.
        #Se define el nombre del fichero .log
        d_t = datetime.now()
        observ_str = d_t.strftime('%Y%m%d_%H%M%S')
        file_observ_c = f'observador_c_{observ_str}_delete.log'

        #Si no existe el folder observador, se crea.
        if not exists('observador'):
            system('mkdir observador')
        
        #Se notifica al observador acerca de la eliminación de un producto.
        with open(f'observador/{file_observ_c}','w') as observador_3:
            observador_3.write(f'{datetime.now()}: '"Los datos del registro eliminado son: %s\n" %args)