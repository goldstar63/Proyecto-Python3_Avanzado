#El módulo vista.py permite incorporar la parte visual de la aplicación. Para ello se utilizó el módulo Tkinter.

#Importamos del módulo tkinter, todas las clases de interés.
#Importamos del módulo modelo, la clase Imeb, la cual nos permite crear un objeto que instancie la clase y mediante él,
#accedemos a los métodos encargados de las operaciones de ingresar, modificar, eliminar, buscar registros.
from tkinter import ttk
from tkinter import *
from tkinter import LabelFrame
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import Menu
from tkinter import StringVar
from modelo import Imeb


# ##############################
#VISTA
# ##############################

class Ventana():

    def __init__(self, win):

        self.windows = win

        self.windows.title("ALMACEN CENTRAL")

        #Creamos un objeto del tipo Imeb para accesar los metodos definidos en la clase.
        #Este objeto sera observado, mediante la clase ConcreteObserverA, del modulo observador
        self.funcion_imeb = Imeb()

        #Creamos el Frame Container Datos del Producto:

        self.frame = LabelFrame(self.windows, text='Datos del Producto')
        self.frame.grid(row=0, column=0, columnspan=3, pady=20)

        #Creamos el Frame Container para Insertar el Producto:

        #Definimos variables de tkinter para pasar valores por parametro al método msg_insert.
        nprod = StringVar()
        nprov = StringVar()
        cantp = StringVar()
        precp = StringVar()
        ubicp = StringVar()
        valop = StringVar()

        Label(self.frame, text="Nombre del Producto").grid(row=1, column=0)
        self.nprod1_entry = Entry(self.frame, textvariable=nprod)
        self.nprod1_entry.focus()
        self.nprod1_entry.grid(row=1, column=1)
        self.nprod1_entry.focus()

        Label(self.frame, text="Nombre del Proveedor").grid(row=1, column=2)
        self.nprov1_entry = Entry(self.frame, textvariable=nprov)
        self.nprov1_entry.grid(row=1, column=3)

        Label(self.frame, text="Cantidad del Producto").grid(row=2, column=0)
        self.cantpr1_entry = Entry(self.frame, textvariable=cantp)
        self.cantpr1_entry.grid(row=2, column=1)

        Label(self.frame, text="Precio del Producto").grid(row=2, column=2)
        self.precpr1_entry = Entry(self.frame, textvariable=precp)
        self.precpr1_entry.grid(row=2, column=3)

        Label(self.frame, text="Ubicacion del Producto").grid(row=3, column=0)
        self.ubicpr1_entry = Entry(self.frame, textvariable=ubicp)
        self.ubicpr1_entry.grid(row=3, column=1)

        Label(self.frame, text="Valor Total de la Inversion").grid(row=3, column=2)
        self.valtot1_entry = Entry(self.frame, textvariable=valop)
        self.valtot1_entry.grid(row=3, column=3)

        self.boton_insert = Button(self.frame, text="Insertar", command=lambda: self.funcion_imeb.func_insertar(self.tree, nprod, nprov, cantp, precp, ubicp, valop))
        self.boton_insert.grid(row=4, column=0, sticky = W)
        
        self.boton_calcular = Button(self.frame, text="Calcular Valor Total", command=lambda: self.funcion_imeb.multiplicar(cantp, precp, valop))
        self.boton_calcular.grid(row=4, column=3, sticky = E)


        #Creamos el Frame Container para Modificar el Producto:

        #Definimos variables de tkinter para pasar valores por parametro al método msg_update.
        nd = StringVar()
        nv = StringVar()
        cp = StringVar()
        pp = StringVar()
        up = StringVar()
        vp = StringVar()

        self.frame2 = LabelFrame(self.windows, text='Modificar Datos del Producto')
        self.frame2.grid(row=5, column=0, columnspan=3, pady=20)

        Label(self.frame2, text="Nuevo Nombre").grid(row=5, column=0)
        self.nomb_nuevo = Entry(self.frame2, textvariable=nd)
        self.nomb_nuevo.grid(row=5, column=1)

        Label(self.frame2, text="Nuevo Proveedor").grid(row=5, column=2)
        self.prov_nuevo = Entry(self.frame2, textvariable=nv)
        self.prov_nuevo.grid(row=5, column=3)

        Label(self.frame2, text="Nueva Cantidad").grid(row=6, column=0)
        self.cant_nueva = Entry(self.frame2, textvariable=cp)
        self.cant_nueva.grid(row=6, column=1)

        Label(self.frame2, text="Nuevo Precio").grid(row=6, column=2)
        self.prec_nuevo = Entry(self.frame2, textvariable=pp)
        self.prec_nuevo.grid(row=6, column=3)

        Label(self.frame2, text="Nueva Ubicacion").grid(row=7, column=0)
        self.ubic_nueva = Entry(self.frame2, textvariable=up)
        self.ubic_nueva.grid(row=7, column=1)

        Label(self.frame2, text="Nuevo Total").grid(row=7, column=2)
        self.tot_nuevo = Entry(self.frame2, textvariable=vp)
        self.tot_nuevo.grid(row=7, column=3)

        self.boton_modificar = Button(self.frame2, text="Modificar", command=lambda: self.funcion_imeb.func_modificar(self.tree, nd, nv, cp, pp, up, vp))
        self.boton_modificar.grid(row=8, column=0, sticky = W)

        self.boton_calcular2 = Button(self.frame2, text="Calcular Valor Total", command=lambda: self.funcion_imeb.multiplicar(cp, pp, vp))
        self.boton_calcular2.grid(row=8, column=3, sticky = E)


        #Creamos el Frame Container para Busquedas:

        #Definimos variable de tkinter para pasar valor por parametro al método func_buscar.
        busc = StringVar()

        self.frame3 = LabelFrame(self.windows, text='Busqueda de Productos')
        self.frame3.grid(row=9, column=0, columnspan=3, pady=20)

        Label(self.frame3, text="Nombre del Producto").grid(row=10, column=0)
        self.nomb_busc = Entry(self.frame3, textvariable=busc)
        self.nomb_busc.grid(row=10, column=1)

        self.boton_buscar = Button(self.frame3, text="Buscar", command=lambda: self.funcion_imeb.func_buscar(busc, self.tree))
        self.boton_buscar.grid(row=10, column=2)

        #Creamos la Tabla con TreeView.

        self.tree = ttk.Treeview(self.windows)
        self.tree["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")
        self.tree.column("#0", width=50, minwidth=50, anchor="w")
        self.tree.column("col1", width=80, minwidth=80, anchor="w")
        self.tree.column("col2", width=80, minwidth=80, anchor="w")
        self.tree.column("col3", width=80, minwidth=80, anchor="w")
        self.tree.column("col4", width=80, minwidth=80, anchor="w")
        self.tree.column("col5", width=80, minwidth=80, anchor="w")
        self.tree.column("col6", width=80, minwidth=80, anchor="w")

        #Definimos el nombre de los campos y su alineación.

        self.tree.grid(column=0, row=12, columnspan=3)
        self.tree.heading("#0", text="Id", anchor="center")
        self.tree.heading("#1", text="Producto", anchor="center")
        self.tree.heading("#2", text="Proveedor", anchor="center")
        self.tree.heading("#3", text="Cantidad", anchor="center")
        self.tree.heading("#4", text="Precio", anchor="center")
        self.tree.heading("#5", text="Ubicacion", anchor="center")
        self.tree.heading("#6", text="Total_Inver", anchor="center")

        #Definimos el boton Eliminar a lo largo de la ventana.

        self.boton_eliminar = Button(self.windows, text="Eliminar", command=lambda: self.funcion_imeb.func_eliminar(self.tree))
        self.boton_eliminar.grid(row=13, columnspan=4, sticky = W + E)

        #Definimos la barra de menu, con opciones de Listar y Salir de la app.
        self.menu_bar = Menu(self.windows)

        self.menu_quit = Menu(self.menu_bar, tearoff=0)
        self.menu_quit.add_command(label="Salir", command=self.windows.quit)
        self.menu_bar.add_cascade(label="Salir", menu=self.menu_quit)

        self.menu_listar = Menu(self.menu_bar, tearoff=0)
        self.menu_listar.add_command(label="Listar", command=lambda: self.funcion_imeb.get_info(self.tree))
        self.menu_bar.add_cascade(label="Listar", menu=self.menu_listar)

        self.menu_server = Menu(self.menu_bar, tearoff=0)
        self.menu_server.add_command(label="Iniciar", command=lambda: self.funcion_imeb.try_connection())
        self.menu_server.add_command(label="Finalizar", command=lambda: self.funcion_imeb.stop_server())
        self.menu_bar.add_cascade(label="Chat", menu=self.menu_server)

        self.windows.config(menu=self.menu_bar)