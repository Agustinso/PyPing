try:
    from tkinter import *
except ImportError:
    raise ImportError("Se requiere el modulo tkinter")
import subprocess
import sys
import os


app = Tk()

host = StringVar()
host.set("localhost")
perdidos = 0
paquetes = 0
acuLatencia = 0
texto_latencia = StringVar()
texto_perdidos = StringVar()
fuente = ("DejaVu", "12", "bold")

color_fondo = "#282C3D"
color_fondoWidgets = "#2c3144"
color_texto = "#82AAFD"
color_resaltado = "#82AAFD"
color_sutil = "#595E80"
color_correcto = "#41860A"
color_cuidado = "#A46558"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def mostrar(ventana):
    ventana.deiconify()


def ocultar(ventana):
    ventana.withdraw()


def tecla(event):
    if event.widget == entrada_host:
        ocultar(app)
        mostrar(ventana_ping)


def pingLoop():
    global host
    global perdidos
    global paquetes
    global acuLatencia
    global texto_latencia
    global texto_perdidos

    CREATE_NO_WINDOW = 0x08000000  # no muestra consola
    pingProcess = subprocess.Popen(['ping', '-n', '1', host], stdout=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
    pingProcess.wait()
    salida = str(pingProcess.stdout.read())
    codigo = pingProcess.poll()
    paquetes = paquetes + 1
    if codigo == 0:
        start = salida.find("Media = ") + 8
        end = salida.find('ms\\r\\n', start)
        latencia = int(salida[start:end])
        acuLatencia = acuLatencia + latencia
        perdPorCien = round(perdidos / paquetes * 100, 1)
        if host != "localhost":
            prom = "(" + str(int(acuLatencia / (paquetes - perdidos))) + ")"
            texto_latencia.set("Latencia: " + str(latencia) + prom)
            texto_perdidos.set("Perdidos: " + str(perdidos) + " (" + str(perdPorCien) + "%)")
        sys.stdout.write("\rLatencia: " + str(latencia) + "      ")
        sys.stdout.flush()
    else:
        # sys.stdout.write("error\n")
        perdidos = perdidos + 1
    app.after(1000, pingLoop)


app.title('PyPing')
app.config(bg=color_fondo)
app.iconbitmap(resource_path("icono.ico"))

entrada_host = Entry(app, textvariable=host)
entrada_host.delete(0, END)
entrada_host.insert(0, "8.8.8.8")
host.set("8.8.8.8")
entrada_host.config(justify="center", bg=color_fondo, fg=color_texto, font=fuente)
entrada_host.bind("<Return>", tecla)
entrada_host.grid(row=1, column=1)


ventana_ping = Toplevel(app)
ventana_ping.config(bg=color_fondo)
ventana_ping.protocol("WM_DELETE_WINDOW", app.destroy)

etiqueta_latencia = Label(ventana_ping, textvariable=texto_latencia)
etiqueta_latencia.config(bg=color_fondo, fg=color_texto, font=fuente)
etiqueta_latencia.grid(row=1, column=1)

etiqueta_perdidos = Label(ventana_ping, textvariable=texto_perdidos)
etiqueta_perdidos.config(bg=color_fondo, fg=color_cuidado, font=fuente)
etiqueta_perdidos.grid(row=2, column=1)

ventana_ping.withdraw()

app.after(20, pingLoop)
app.mainloop()
