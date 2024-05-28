from tkinter import *
from socket import *
import _thread
from datetime import datetime
from os.path import exists
from os import system

#Iniciamos conexion al server
def initialize_server():

    #Inicializamos el socket del server
    s = socket(AF_INET, SOCK_STREAM)
    
    #Configuramos los detalles para la conexion del server
    host='localhost'
    port=1234

    #Iniciamos la conexion del server
    s.bind((host, port))

    #Definimos la cantidad de clientes
    s.listen(1)

    #Aceptamos la conexion desde el cliente
    conn, addr = s.accept()

    return conn


#Funcion para actualizar chat log
def update_chat(msg, state):

    global chatlog

    chatlog.config(state=NORMAL)

    #Actualizamos el mensaje en la seccion chatlog
    if state==0:
        chatlog.insert(END, 'ADMIN: ' + msg)
    
    else:
        chatlog.insert(END, 'CLIENT: ' + msg)
    
    chatlog.config(state=DISABLED)

    #Mostramos el ultimo mensaje
    chatlog.yview(END)


#Funcion para enviar mensaje
def send():

    global textbox

    #Obtenemos el mensaje y lo guardamos en msg
    msg = textbox.get("0.0", END)

    #Almacenamos el mensaje en un log
    d_t = datetime.now()
    admin_str = d_t.strftime('%Y%m%d_%H%M%S')
    file_admin = f'admin{admin_str}_msg.log'

    #Si no existe el folder chat_log, se crea.
    if not exists('chat_log'):
        system('mkdir chat_log')

    #Se abre el log y se guarda el msg enviado por el admin.
    with open(f'chat_log/{file_admin}','w') as admin_1:
        admin_1.write(f'{datetime.now()}: '"ADMIN: %s\n" %msg)

    #Actualizamos el espacio de chat(chatlog)
    update_chat(msg, 0)

    #Enviamos el mensaje
    conn.send(msg.encode('ascii'))
    
    textbox.delete("0.0", END)



#Funcion para recibir mensaje
def receive():
    
    while 1:

        try:

            data = conn.recv(1024)
            msg = data.decode('ascii')

            if msg != "":
                update_chat(msg, 1)
        
        except:
            pass


#GUI para el Admin
def GUIADMIN():

    global chatlog
    global textbox

    #Iniciamos la ventana de chat
    gui = Tk()

    #Configuramos la ventana principal del chat
    gui.title("Admin Chat")
    gui.geometry("380x430")

    #Definimos espacio para el texto del chat
    chatlog = Text(gui, bg='white')
    chatlog.config(state=DISABLED)

    #Definimos el boton para enviar mensaje
    sendbutton = Button(gui, bg='blue', fg='white', text='Enviar', command=send)

    #Definimos la caja de texto para escribir el mensaje
    textbox = Text(gui, bg='white')

    #Definimos la ubicacion de los elementos en la ventana
    chatlog.place(x=6, y=6, width=370 , height=386)
    textbox.place(x=6, y=401, width=265 , height=20)
    sendbutton.place(x=300, y=401, width=50 , height=20)

    #Creamos thread para capturar mensaje continuamente
    _thread.start_new_thread(receive, ())

    #Finalizamos la ventana
    gui.mainloop()




if __name__ == '__main__':
    chatlog = texbox = None
    conn = initialize_server()
    GUIADMIN()