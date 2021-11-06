import tkinter as tk
from tkinter.constants import ACTIVE, DISABLED
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import numpy as np
import serial as sr

Arduino=sr.Serial('COM3',9600)

Ventana1=tk.Tk()
Ventana1.geometry("700x700")
Ventana1.resizable(0,0)
Ventana1.title("Proyecto")
Ventana1.configure(bg="Black")
Ventana1.iconbitmap("unfv.ico")
 

azulBajo = np.array([100,100,20],np.uint8)
azulAlto = np.array([125,255,255],np.uint8)

rojoBajo=np.array([100,100,20],np.uint8)
rojoAlto=np.array([100,100,20],np.uint8)

def iniciar():
    global cap
    global control
    global Estado
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
    BotonInicio.config(state=ACTIVE)
    BotonFin.config(state=DISABLED)
    visualizar2()

def visualizar():
    global cap
    global control
    global pre_control
    pre_control=control
    if cap is not None:
        ret,frame = cap.read()
        if ret == True:
            #frame = imutils.resize(frame)
            frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(frameHSV,azulBajo,azulAlto)
            contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
            for c in contornos:               
                area = cv2.contourArea(c)
                if area > 3000:
                    M = cv2.moments(c)
                    if (M["m00"]==0): M["m00"]=1
                    x = int(M["m10"]/M["m00"])
                    y = int(M['m01']/M['m00'])
                    cv2.circle(frame, (x,y), 7, (0,255,0), -1)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, "AzulDetectado",(x+10,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)
                    nuevoContorno = cv2.convexHull(c)
                    cv2.drawContours(frame, [nuevoContorno], 0, (255,0,0), 3)
                    control=0
                    
                else:
                    control=1
            CambioControl(pre_control,control)
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

def CambioControl(Pre_control,Control):
    global Estado
    if Pre_control!=Control:
        if Control==0:
            Arduino.write(b'0')
            Estado.set("Faja Desactivada.")
        elif Control==1:
            Arduino.write(b'1')
            Estado.set("Faja Activada.")
        else:
            Arduino.write(b'0')
            Estado.set("Faja Detenida. Estado Desconocido.")


cap=cv2.VideoCapture(0,cv2.CAP_ANDROID)
cap1=cv2.VideoCapture(0,cv2.CAP_ANDROID)

BotonInicio=tk.Button(Ventana1,text="Iniciar",command=lambda:iniciar(),state=ACTIVE)
BotonInicio.place(x=250,y=90)

BotonFin=tk.Button(Ventana1,text="Detener",command=lambda:detener(),state=DISABLED)
BotonFin.place(x=400,y=90)

titulo=tk.Label(Ventana1,text="Control de Fajas \n por Vision Artificial",bg="Black",fg="White",font=("Courier",18))
titulo.place(x=190,y=10)

lbl_img=tk.Label(Ventana1,image="",bg="Black")
lbl_img.place(x=30,y=120)

Estado=tk.StringVar()
Estado.set("Bienvenido.")
lbl_estado=tk.Label(Ventana1,textvariable=Estado,bg="White",fg="Black",width=100,anchor=tk.W)
lbl_estado.place(x=0,y=680)

Ventana1.mainloop()