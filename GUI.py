import tkinter as tk
from tkinter.constants import ACTIVE, DISABLED
from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np
import serial as sr
import time

Arduino=sr.Serial('COM3',9600)
time.sleep(2)

Ventana1=tk.Tk()
Ventana1.geometry("700x700")
Ventana1.resizable(0,0)
Ventana1.title("Proyecto")
Ventana1.configure(bg="Black")
Ventana1.iconbitmap("unfv.ico")
 

azulBajo = np.array([100,100,20],np.uint8)
azulAlto = np.array([125,255,255],np.uint8)

amarilloBajo = np.array([15,100,20],np.uint8)
amarilloAlto = np.array([45,255,255],np.uint8)

redBajo1 = np.array([0,100,20],np.uint8)
redAlto1 = np.array([5,255,255],np.uint8)

redBajo2 = np.array([175,100,20],np.uint8)
redAlto2 = np.array([179,255,255],np.uint8)

def iniciar():
    global cap
    global control
    global Estado
    global ColorAlto,ColorBajo,ColorE
    global Color
    global BordeColor

    cap1.release()
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    control=1
    Arduino.write(b'1')
    Estado.set("Faja Activada.")
    BotonFin.config(state=ACTIVE)
    BotonInicio.config(state=DISABLED)
    visualizar()

def detener():
    global cap1
    global control
    global Estado
    cap.release()
    control=0
    cap1 = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    Arduino.write(b'0')
    Estado.set("Faja Desactivada.")
    Color.set("Seleccionar Color")
    BotonInicio.config(state=ACTIVE)
    BotonFin.config(state=DISABLED)
    visualizar2()

def visualizar():
    global cap
    global control
    global ColorAlto,ColorBajo

    if cap is not None:
        ret,frame = cap.read()
        if ret == True:
            #frame = imutils.resize(frame)
            ColorAlto,ColorBajo,ColorE,BordeColor=CambioColor()
            if ColorE != "Seleccionar Color":
                frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(frameHSV,ColorBajo,ColorAlto)
                contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
                for c in contornos:               
                    area = cv2.contourArea(c)
                    if area > 3500:
                        M = cv2.moments(c)
                        if (M["m00"]==0): M["m00"]=1
                        x = int(M["m10"]/M["m00"])
                        y = int(M['m01']/M['m00'])
                        cv2.circle(frame, (x,y), 7, BordeColor, -1)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(frame, "{}".format(ColorE)+" Detectado",(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
                        nuevoContorno = cv2.convexHull(c)
                        cv2.drawContours(frame, [nuevoContorno], 0, BordeColor, 3)
                        control=0
                if control==1:
                        Arduino.write(b'1')
                        Estado.set("Faja Activada")
                elif control==0:
                        Estado.set("Faja Desactivada")
                        Arduino.write(b'0')
                        control=1
            #CambioControl(pre_control,control)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lbl_img.configure(image=img)
            lbl_img.image = img
            lbl_img.after(5, visualizar)
        else:
            lbl_img.image = ""
            cap.release()

def visualizar2():
    global cap1
    if cap1 is not None:
        ret,frame1 = cap1.read()
        if ret == True:
            #frame1 = imutils.resize(frame1)
            frame1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2RGB)
            im1 = Image.fromarray(frame1)
            img1 = ImageTk.PhotoImage(image=im1)
            lbl_img.configure(image=img1)
            lbl_img.image = img1
            lbl_img.after(10,visualizar2)
        else:
            lbl_img.image = ""
            cap1.release()

def CambioColor():

    global Color

    ColorE=Color.get()

    if ColorE == "Azul":
        ColorAlto=azulAlto
        ColorBajo=azulBajo
        BordeColor=(255,0,0)
    elif ColorE=="Rojo":
        ColorAlto=redAlto2
        ColorBajo=redBajo2
        BordeColor=(0,0,255)
    elif ColorE== "Amarillo":
        ColorAlto=amarilloAlto
        ColorBajo=amarilloBajo
        BordeColor=(0,255,255)
    else:
        ColorAlto=azulAlto
        ColorBajo=azulBajo
        BordeColor=(255,0,0)

    return ColorAlto,ColorBajo,ColorE,BordeColor


lista_colores=["Azul","Rojo","Amarillo"]

cap=cv2.VideoCapture(0,cv2.CAP_ANDROID)
cap1=cv2.VideoCapture(0,cv2.CAP_ANDROID)

BotonInicio=tk.Button(Ventana1,text="Iniciar",command=lambda:iniciar(),state=ACTIVE)
BotonInicio.place(x=150,y=90)

BotonFin=tk.Button(Ventana1,text="Detener",command=lambda:detener(),state=DISABLED)
BotonFin.place(x=300,y=90)

titulo=tk.Label(Ventana1,text="Control de Fajas \n por Vision Artificial",bg="Black",fg="White",font=("Courier",18))
titulo.place(x=190,y=10)

Color=tk.StringVar()
Color.set("Seleccionar Color")
barra_color=tk.OptionMenu(Ventana1,Color,*lista_colores)
barra_color.place(x=450,y=90)

lbl_img=tk.Label(Ventana1,image="",bg="Black")
lbl_img.place(x=30,y=120)

Estado=tk.StringVar()
Estado.set("Bienvenido.")
lbl_estado=tk.Label(Ventana1,textvariable=Estado,bg="White",fg="Black",width=100,anchor=tk.W)
lbl_estado.place(x=0,y=680)

Ventana1.mainloop()