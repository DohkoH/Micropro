import tkinter as tk

Ventana1=tk.Tk()
Ventana1.geometry("600x600")
Ventana1.resizable(0,0)
Ventana1.title("Control por Vision Artificial")


BotonInicio=tk.Button(text="Iniciar")
BotonInicio.place(x=250,y=250)


BotonFin=tk.Button(text="Detener")
BotonFin.place(x=300,y=250)

Ventana1.mainloop()