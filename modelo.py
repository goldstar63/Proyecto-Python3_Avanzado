#El módulo modelo.py contiene la lógica de la aplicación, o sea, se definen decoradores y la clase Imeb que contiene
    #todos los metodos encargados de realizar las distintas operaciones de insertar, eliminar, modificar y buscar registros.

#Adicional, el objeto que instancie a la clase Imeb, sera observado, con el animo de notificar a su observador sobre
    #los distintos eventos que ocurren en el mismo.

#Se importan los módulos que permiten operar con BD, expresiones regulares, mensajes, sistema operativo,
# fecha-hora y observaciones.
import sqlite3
import re
from tkinter.messagebox import *
import os.path
from datetime import datetime
from os.path import exists
from os import system
from observador import Subject
import sys
import subprocess
import threading
from pathlib import Path

serverproc = ''
clientproc = ''

# ##############################
#MODELO
# ##############################

#Decorador insertar
def notif_insertar(funcion):
    #funcion envoltura
    def insert_env(*args):
        var = funcion(*args)
        if var == 'True':
            showinfo('Alta', 'Registro Insertado')
        else:
            showinfo('Error', 'Para ingresar el registro debe completar todos los datos')

    return insert_env


#Decorador modificar
def notif_modif(funcion):
    #funcion envoltura
    def modif_env(*args):
        var = funcion(*args)
        if var == 'True':
            showinfo('Actualizar', 'Registro Modificado')
        else:
            showinfo('Error', 'Para modificar el registro debe completar todos los datos')
    return modif_env


#Decorador eliminar
def notif_del(funcion):
    #funcion envoltura
    def del_env(*args):
        funcion(*args)
        showinfo('Baja', 'Registro Eliminado')
    return del_env



class Imeb(Subject):

    #El constructor de la clase garantiza la conexion a la BD Sqlite y la creación de la estructura
    #de la tabla si no existe.
    def __init__(self, ):

        try:
            query = 'CREATE TABLE IF NOT EXISTS "registroprod" ("id"	INTEGER NOT NULL, "producto"	TEXT NOT NULL, "proveedor"	TEXT NOT NULL, "cantidad"	INTEGER NOT NULL, "precio"	REAL NOT NULL, "ubicacion"	TEXT NOT NULL, "total"	REAL NOT NULL, PRIMARY KEY("id" AUTOINCREMENT))'

            self.run_query(query)

        except:
            showinfo('Error', 'Error de creacion de la tabla')

    #Definimos una funcion para ejecutar consultas a la BD.
    def run_query(self, query, parametros=()):
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "almacen.db")
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parametros)
            conn.commit()
        return result

    #Definimos una función que permite actualizar la lista en la aplicación.
    def get_info(self, tree):
        
        #cleaning table
        records = tree.get_children()
        for i in records:
            tree.delete(i)
        
        #Consultamos la BD y actualizamos la lista en la aplicación.
        query = 'SELECT * FROM registroprod ORDER BY id DESC'
        db_rows = self.run_query(query)
        for r in db_rows:
            tree.insert('', 0, text=r[0], values=(r[1], r[2], r[3], r[4], r[5], r[6]))
    
    
    #Definimos una función que valida si el registro tiene todos sus datos completos, para después insertarlo en la BD.
    #Mediante un decorador adicionamos al metodo func_insertar, la posibilidad de notificar al usuario cuando un registro
        #es insertado de manera correcta o cuando el ingreso no es posible.
    @notif_insertar
    def func_insertar(self, tree, nprod, nprov, cantp, precp, ubicp, valop):

        var_insert = ''

        #Se copian los datos del registro a ingresar en las variables definidas.
        l_prod = nprod.get()
        l_prov = nprov.get()
        l_cantp = cantp.get()
        l_precp = precp.get()
        l_ubicp = ubicp.get()
        l_vtot = valop.get()

        #Se determina la longitud de los datos a ingresar.
        l_prod = len(l_prod)
        l_prov = len(l_prov)
        l_cantp = len(l_cantp)
        l_precp = len(l_precp)
        l_ubicp = len(l_ubicp)
        l_vtot = len(l_vtot)

        #Si los valores del cálculo de la longitud, son distintos de 0, se procede a insertar el registro en la BD.
        #Se actualiza la lista de registros en la app.
        if l_prod != 0 and l_prov != 0 and l_cantp != 0 and l_precp != 0 and l_ubicp != 0 and l_vtot != 0:
            
            query = 'INSERT INTO registroprod(id, producto, proveedor, cantidad, precio, ubicacion, total) VALUES(NULL, ?, ?, ?, ?, ?, ?)'
            parametros = (nprod.get(), nprov.get(), cantp.get(), precp.get(), ubicp.get(), valop.get())
            self.run_query(query, parametros)
            self.get_info(tree)

            #Se notifica al observador a del objeto funcion_imeb, acerca del ingreso del nuevo registro
            self.notificar_a(nprod.get(), nprov.get(), cantp.get(), precp.get(), ubicp.get(), valop.get())

            nprod.set("")
            nprov.set("")
            cantp.set("")
            precp.set("")
            ubicp.set("")
            valop.set("")
            
            var_insert = 'True'

            return var_insert
        else:
            var_insert = 'False'

            return var_insert


    #Definimos una función para eliminar registros.
    #Mediante un decorador adicionamos al metodo func_eliminar, la posibilidad de notificar al usuario cuando un registro
        #es eliminado
    @notif_del
    def func_eliminar(self, tree):

        #Se capturan los datos del registro a eliminar
        prod_old = tree.item(tree.selection())['values'][0]
        prov_old = tree.item(tree.selection())['values'][1]
        cant_old = tree.item(tree.selection())['values'][2]
        prec_old = tree.item(tree.selection())['values'][3]
        ubic_old = tree.item(tree.selection())['values'][4]
        tota_old = tree.item(tree.selection())['values'][5]

        #Se captura el id del producto a eliminar y se procede a su eliminación
        id = tree.item(tree.selection())['text']
        query = 'DELETE FROM registroprod WHERE id = ?'
        self.run_query(query, (id, ))
        
        #Se actualiza la lista de productos en la aplicación
        self.get_info(tree)

        #Se notifica al observador c, acerca de la eliminación del registro
        self.notificar_c(prod_old, prov_old, cant_old, prec_old, ubic_old, tota_old)


    #Definimos una función para buscar registros de interés.
    def func_buscar(self, busc, tree):

        #Definimos un patrón que solo permite letras minúsculas. No mayúsculas, no números, no caracteres especiales.
        patron = "^[a-z]*$"

        #Si el nombre del producto coincide con el patrón, procedemos con la búsqueda del mismo en la BD.
        if (re.match(patron, busc.get())):

            #Blanqueamos la lista de la aplicación.
            records = tree.get_children()
            for i in records:
                tree.delete(i)
        
            #Consultamos a la BD para verificar si el producto está y actualizamos la lista de productos en la aplicación.
            query = 'SELECT * FROM registroprod WHERE producto = ?'
            db_rows = self.run_query(query, (busc.get(), ))
            for r in db_rows:
                tree.insert('', 0, text=r[0], values=(r[1], r[2], r[3], r[4], r[5], r[6]))

            #Blanqueamos la caja de datos en la aplicación.
            busc.set("")

    
    #Se define una funcion para modificar los datos de los registros.
    #Mediante un decorador adicionamos al metodo func_modificar, la posibilidad de notificar al usuario cuando un registro
        #es actualizado de manera correcta o cuando la modificacion no es posible.
    @notif_modif
    def func_modificar(self, tree, nd, nv, cp, pp, up, vp):

        #Se copian los datos nuevos del registro a modificar en las variables definidas.
        l_new_nomb = nd.get()
        l_new_prov = nv.get()
        l_new_cant = cp.get()
        l_new_prec = pp.get()
        l_new_ubic = up.get()
        l_new_tot = vp.get()

        #Se determina la longitud de los datos nuevos, del registro a modificar.
        l_new_nomb = len(l_new_nomb)
        l_new_prov = len(l_new_prov)
        l_new_cant = len(l_new_cant)
        l_new_prec = len(l_new_prec)
        l_new_ubic = len(l_new_ubic)
        l_new_tot = len(l_new_tot)

        #Si los valores del cálculo de la longitud, son distintos de 0, se procede a modificar el registro en la BD.
        #Se actualiza la lista de registros en la app.
        if l_new_nomb != 0 and l_new_prov != 0 and l_new_cant != 0 and l_new_prec != 0 and l_new_ubic != 0 and l_new_tot != 0:

            #Se copian los datos viejos del registro a modificar.
            prod_old = tree.item(tree.selection())['values'][0]
            prov_old = tree.item(tree.selection())['values'][1]
            cant_old = tree.item(tree.selection())['values'][2]
            prec_old = tree.item(tree.selection())['values'][3]
            ubic_old = tree.item(tree.selection())['values'][4]
            tota_old = tree.item(tree.selection())['values'][5]
            
            #Se elabora la query, se establecen los valores y se ejecuta la modificación.
            query = 'UPDATE registroprod SET producto = ?, proveedor = ?, cantidad = ?, precio = ?, ubicacion = ?, total = ? WHERE producto = ? AND proveedor = ? AND cantidad = ? AND precio = ? AND ubicacion = ? AND total = ?'
            parametros = (nd.get(), nv.get(), cp.get(), pp.get(), up.get(), vp.get(), prod_old, prov_old, cant_old, prec_old, ubic_old, tota_old)
            self.run_query(query, parametros)

            #Se actualiza la lista de productos en la aplicación.
            self.get_info(tree)
            
            #Se notifica al observador 2 sobre el registro modificado
            self.notificar_b(nd.get(), nv.get(), cp.get(), pp.get(), up.get(), vp.get())
            
            #Se blanquean las cajas de datos
            nd.set("")
            nv.set("")
            cp.set("")
            pp.set("")
            up.set("")
            vp.set("")

            return 'True'
        else:
            return 'False'

    #Se define una función para calcular el valor total invertido por producto.
    def multiplicar(self, cantp, precp, valop):

        #Se define una excepción que verifica si los valores ingresados son números.
        #Si alguno de los valores ingresados son letras, se ejecuta el except.
        try:
            c = int(cantp.get())
            p = float(precp.get())

            #Si los valores ingresados son menores o igual a cero, se lanza la excepción NumNoAceptado de manera intensional.
            #De lo contrario, se ejecuta la multiplicación de la cantidad de producto por su precio y se setea el resultado
            #en la caja de datos de la aplicación.
            if c <= 0 or p <= 0.0:

                try:
                    raise NumNoAceptado(276, "modelo.py")
            
                except NumNoAceptado as N:
                    N.logerror_num()
            
            else:

                resultado = c * p
                resultado = round(resultado, 1)
                resultado = str(resultado)

                valop.set(resultado)

        except:
            #Se copian los valores ingresados en las variables respectivas.
            cantp_l = cantp.get()
            precp_l = precp.get()

            #Si la long de cualquiera de los valores ingresado es distinto de cero, se lanza de manera intencional
            #la excepcion CarNoAceptado, especificando las líneas donde se identifica el error de ejecución del código
            #y el módulo donde se encuentra.
            if len(cantp_l) != 0 or len(precp_l) != 0:

                try:
                    raise CarNoAceptado(294, 295, "modelo.py")
                
                except CarNoAceptado as C:
                    C.logerror_car()
                    
    
    #El método retorna la ruta de acceso al subproceso server_chat.py
    def root_server(self, ):

        #Agrego ruta al servidor (server_chat.py)
        self.root_s = Path(__file__).resolve().parent
        self.server_path = os.path.join(self.root_s, 'chat', 'server_chat.py')

        return self.server_path
    

    #El método retorna la ruta de acceso al subproceso cliente_chat.py
    def root_client(self, ):

        #Agrego ruta al cliente (cliente_chat.py)
        self.root_c = Path(__file__).resolve().parent
        self.cliente_path = os.path.join(self.root_c, 'chat', 'cliente_chat.py')

        return self.cliente_path
    

    #Habilitamos los hilos de conexión y lanzamos los subprocesos
    def try_connection(self, ):

        #Verifico si los subprocesos están corriendo.
        if serverproc != '' and clientproc != '':

            #Detengo los subprocesos
            serverproc.kill()
            clientproc.kill()

            #Habilito los hilos de conexión y lanzo los subprocesos nuevamente
            threading.Thread(target = self.raise_server, args=(True, ), daemon=True).start()
            threading.Thread(target = self.raise_client, args=(True, ), daemon=True).start()

        else:
            #Habilito los hilos de conexión y lanzo los subprocesos por 1era vez
            threading.Thread(target = self.raise_server, args=(True, ), daemon=True).start()
            threading.Thread(target = self.raise_client, args=(True, ), daemon=True).start()


    #Permite lanzar el subproceso server_chat.py. La variable var = args=(True, )
    def raise_server(self, var):

        #Capturamos la ruta de acceso al subproceso
        self.server_p = self.root_server()

        if var == True:

            global serverproc

            serverproc = subprocess.Popen([sys.executable, self.server_p])
            serverproc.communicate()
        
        else:

            print("")
    

    #Permite lanzar el subproceso cliente_chat.py. La variable var = args=(True, )
    def raise_client(self, var):

        #Capturamos la ruta de acceso al subproceso
        self.client_p = self.root_client()

        if var == True:

            global clientproc

            clientproc = subprocess.Popen([sys.executable, self.client_p])
            clientproc.communicate()
        
        else:

            print("")


    #El método permite detener los subprocesos server_chat.py y cliente_chat.py
    def stop_server(self, ):

        global serverproc
        global clientproc

        if serverproc != '' and clientproc != '':
            
            serverproc.kill()
            clientproc.kill()


#Se define una clase de tipo excepción con el ánimo de identificar valores numéricos no aceptados.
#Si los valores a multiplicar son números menores o iguales a cero, no se ejecuta la operación.
#y el evento se registra en un log de errores.
class NumNoAceptado(Exception):

    def __init__(self, line, file):

        self.line = line
        self.file = file
    
    def logerror_num(self):

        #Se captura la fecha y ahora del evento o error.
        #Se define el nombre del fichero .log
        d_h = datetime.now()
        log_str = d_h.strftime('%Y%m%d_%H%M%S')
        archivo_log = f'log_error_{log_str}_num.log'

        #Si no existe el folder logs_errors, se crea.
        if not exists('logs_errors'):
            system('mkdir logs_errors')
        
        #Se abre el fichero .log y se escribe la fecha, hora y mensaje a mostrar.
        #Se notifica al usuario la ocurrencia del error.
        with open(f'logs_errors/{archivo_log}','w') as error:
            error.write(f'{datetime.now()}: '"Ocurrio un error en la linea %s, en file %s porque los numeros ingresados son menores o iguales a cero\n" %(self.line, self.file))

        showinfo('Error', 'Por favor, ingrese numeros mayores a cero en los campos Cantidad y Precio')

#Se define una clase de tipo excepción con el ánimo de identificar valores no aceptados (caracteres).
#Si los valores a multiplicar son caracteres, no se ejecuta la operación.
#y el evento se registra en un log de errores.
class CarNoAceptado(Exception):

    def __init__(self, line1, line2, file):

        self.line1 = line1
        self.line2 = line2
        self.file = file

    def logerror_car(self):

        #Se captura la fecha y ahora del evento o error.
        #Se define el nombre del fichero .log
        d_h2 = datetime.now()
        log_str2 = d_h2.strftime('%Y%m%d_%H%M%S')
        archivo_log2 = f'log_error_{log_str2}_car.log'

        #Si no existe el folder logs_errors, se crea.
        if not exists('logs_errors'):
            system('mkdir logs_errors')

        #Se abre el fichero .log y se escribe la fecha, hora y mensaje a mostrar.
        #Se notifica al usuario la ocurrencia del error.
        with open(f'logs_errors/{archivo_log2}','w') as error2:
            error2.write(f'{datetime.now()}: '"Ocurrio un error en la linea %s o en la linea %s, en el file %s porque el valor ingresado es un caracter (letra o simbolo)\n" %(self.line1, self.line2, self.file))

        showinfo('Error', 'Por favor, ingrese numeros en los campos Cantidad y Precio')