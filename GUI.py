import tkinter as tk
from Reconocimiento import *
from PIL import ImageTk,Image

Ventana1=tk.Tk()
Ventana1.geometry("500x500")
Ventana1.resizable(0,0)
Ventana1.title("Proyecto")
Ventana1.configure(bg="Black")


def Limpiar():

    lbl_img.place_forget()

def Mostrar():

    lbl_img.place(x=100,y=100)

BotonInicio=tk.Button(Ventana1,text="Iniciar",command=lambda:Mostrar())
BotonInicio.place(x=135,y=70)

BotonFin=tk.Button(Ventana1,text="Detener",command=lambda:Limpiar())
BotonFin.place(x=290,y=70)

titulo=tk.Label(Ventana1,text="Control de Fajas \n por Vision Artificial",bg="Black",fg="White",font=("Courier",18))
titulo.place(x=90,y=0)

lbl_img=tk.Label(Ventana1)
imagen=Image.fromarray(Reconocer("HSF.png"))
imagen=ImageTk.PhotoImage(image=imagen)
lbl_img.configure(image=imagen)

Ventana1.mainloop()