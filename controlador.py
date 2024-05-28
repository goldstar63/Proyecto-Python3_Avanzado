#El módulo controlador.py permite lanzar la ventana de la aplicación y define el objeto que sera observado (funcion_imeb).

#La clase Control, mediante su constructor, permite pasar por parametro un objeto. 
#que instancia a la clase Tk() [la ventana] y lanza, mediante la clase Ventana, la aplicación.

#Importamos Tk de tkinter para definir el inicio-fin de la ventana.
#Importamos la clase Ventana del módulo vista que contiene toda la parte visual de la app.
#Importamos el modulo observador, el cual permite crear los 3 observadores concretos, que observan al objeto funcion_imeb
from tkinter import Tk
from vista import Ventana
import observador

class Control():
    
    def __init__(self, windows):
        self.windows_controler = windows
        self.objeto_vista = Ventana(self.windows_controler)
        self.el_observador_a = observador.ConcreteObserverA(self.objeto_vista.funcion_imeb)
        self.el_observador_b = observador.ConcreteObserverB(self.objeto_vista.funcion_imeb)
        self.el_observador_c = observador.ConcreteObserverC(self.objeto_vista.funcion_imeb)

#Se lanza la ventana principal de la aplicación.
if __name__ == "__main__":
    windows = Tk()
    almacen_ventana = Control(windows)
    windows.mainloop()