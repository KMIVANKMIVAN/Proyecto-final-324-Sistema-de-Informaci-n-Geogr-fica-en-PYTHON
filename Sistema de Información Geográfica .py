# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 10:15:08 2021

@author: van
"""
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import numpy as np

def elegir_imagen():
    # Especificar los tipos de archivos, para elegir solo a las imágenes
    path_image = filedialog.askopenfilename(filetypes = [
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg")])

    if len(path_image) > 0:
        global image

        # Leer la imagen de entrada y la redimensionamos
        image = cv2.imread(path_image)
        image= imutils.resize(image, height=380)

        # Para visualizar la imagen de entrada en la GUI
        imageToShow= imutils.resize(image, width=480)
        imageToShow = cv2.cvtColor(imageToShow, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(imageToShow )
        img = ImageTk.PhotoImage(image=im)

        lblInputImage.configure(image=img)
        lblInputImage.image = img

        # Label IMAGEN DE ENTRADA
        lblInfo1 = Label(root, text="IMAGEN DE ENTRADA:")
        lblInfo1.grid(column=0, row=1, padx=5, pady=5)

        # Al momento que leemos la imagen de entrada, vaciamos
        # la iamgen de salida y se limpia la selección de los
        # radiobutton
        lblOutputImage.image = ""
        selected.set(0)

def deteccion_color():
    global image
    if selected.get() == 1:
        # Rojo
        rangoBajo1 = np.array([0, 140, 90], np.uint8)
        rangoAlto1 = np.array([8, 255, 255], np.uint8)
        rangoBajo2 = np.array([160, 140, 90], np.uint8)
        rangoAlto2 = np.array([180, 255, 255], np.uint8)

    if selected.get() == 2:
        # VEGETACION
        rangoBajo = np.array([40, 15, 20], np.uint8)
        rangoAlto = np.array([87, 255, 255], np.uint8)

    if selected.get() == 3:
        # LAGO TITICACA
        rangoBajo = np.array([86, 37, 0], np.uint8)
        rangoAlto = np.array([109, 255, 255], np.uint8)
        
    if selected.get() == 4:
        # LAGOS CONGELADOS O NEVADOS
        rangoBajo = np.array([55, 0, 186], np.uint8)
        rangoAlto = np.array([163, 255, 255], np.uint8)
        
    if selected.get() == 5:
        # OCEANO
        rangoBajo = np.array([62, 82, 105], np.uint8)
        rangoAlto = np.array([179, 255, 255], np.uint8)
        
    if selected.get() == 6:
        # ARENA
        rangoBajo = np.array([9, 5, 182], np.uint8)
        rangoAlto = np.array([179, 255, 255], np.uint8)
    
    if selected.get() == 7:
        # ARENA
        rangoBajo = np.array([8, 55, 139], np.uint8)
        rangoAlto = np.array([34, 255, 255], np.uint8)
        
    if selected.get() == 8:
        # ZONAS MONTAÑOSAS
        rangoBajo = np.array([21, 0, 101], np.uint8)
        rangoAlto = np.array([27, 255, 255], np.uint8)
    
    if selected.get() == 9:
        # ZONAS MONTAÑOSAS
        rangoBajo = np.array([28, 61, 132], np.uint8)
        rangoAlto = np.array([78, 255, 255], np.uint8)
        
    if selected.get() == 10:
        # ZONAS MONTAÑOSAS
        rangoBajo = np.array([35, 105, 35], np.uint8)
        rangoAlto = np.array([78, 255, 255], np.uint8)
        
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageGray = cv2.cvtColor(imageGray, cv2.COLOR_GRAY2BGR)
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    if selected.get() == 1:
        # Detectamos el color rojo
        maskRojo1 = cv2.inRange(imageHSV, rangoBajo1, rangoAlto1)
        maskRojo2 = cv2.inRange(imageHSV, rangoBajo2, rangoAlto2)
        mask = cv2.add(maskRojo1, maskRojo2)
    else:
        # Detección para el color Amarillo y Azul celeste
        mask = cv2.inRange(imageHSV, rangoBajo, rangoAlto)

    mask = cv2.medianBlur(mask, 7)
    colorDetected = cv2.bitwise_and(image, image, mask=mask)

    # Fondo en grises
    invMask = cv2.bitwise_not(mask)
    bgGray = cv2.bitwise_and(imageGray, imageGray, mask=invMask)

    # Sumamos bgGray y colorDetected
    finalImage = cv2.add(bgGray, colorDetected)
    imageToShowOutput = cv2.cvtColor(finalImage, cv2.COLOR_BGR2RGB)

    # Para visualizar la imagen en lblOutputImage en la GUI
    im = Image.fromarray(imageToShowOutput)
    img = ImageTk.PhotoImage(image=im)
    lblOutputImage.configure(image=img)
    lblOutputImage.image = img

    # Label IMAGEN DE SALIDA
    lblInfo3 = Label(root, text="IMAGEN DE SALIDA:", font="bold")
    lblInfo3.grid(column=1, row=0, padx=5, pady=50)
    
# Creamos la ventana principal
root = Tk()

# Label donde se presentará la imagen de entrada
lblInputImage = Label(root)
lblInputImage.grid(column=0, row=2)

# Label donde se presentará la imagen de salida
lblOutputImage = Label(root)
lblOutputImage.grid(column=1, row=1, rowspan=6)

# Label ¿Qué color te gustaría resaltar?
lblInfo2 = Label(root, text="ZONAS GEOGRAFICAS", width=25)
lblInfo2.grid(column=0, row=3, padx=5, pady=5)

# Creamos los radio buttons y la ubicación que estos ocuparán
selected = IntVar()
#rad1 = Radiobutton(root, text='Rojo', width=25,value=1, variable=selected, command= deteccion_color)
rad2 = Radiobutton(root, text='LLANOS CON VEGETACION',width=25, value=2, variable=selected, command= deteccion_color)
rad3 = Radiobutton(root, text='LAGOS',width=25, value=3, variable=selected, command= deteccion_color)
rad4 = Radiobutton(root, text='LAGOS CONGELADOS O NEVADOS',width=25, value=4, variable=selected, command= deteccion_color)
rad5 = Radiobutton(root, text='OCEANO',width=25, value=5, variable=selected, command= deteccion_color)
rad6 = Radiobutton(root, text='ARENA',width=25, value=6, variable=selected, command= deteccion_color)
rad7 = Radiobutton(root, text='PLANICIES ALTAS',width=25, value=7, variable=selected, command= deteccion_color)
rad8 = Radiobutton(root, text='ZONAS MONTAÑOSAS',width=25, value=8, variable=selected, command= deteccion_color)
rad9 = Radiobutton(root, text='LAGOS CON ALGAS',width=25, value=9, variable=selected, command= deteccion_color)
rad10 = Radiobutton(root, text='ZELBA DENZA',width=25, value=10, variable=selected, command= deteccion_color)

#rad1.grid(column=0, row=4)
rad2.grid(column=0, row=5)
rad3.grid(column=0, row=6)
rad4.grid(column=0, row=7)
rad5.grid(column=0, row=8)
rad6.grid(column=0, row=9)
rad7.grid(column=0, row=10)
rad8.grid(column=0, row=11)
rad9.grid(column=0, row=12)
rad10.grid(column=0, row=13)

# Creamos el botón para elegir la imagen de entrada
btn = Button(root, text="Elegir imagen", width=45, command=elegir_imagen)
btn.grid(column=0, row=0, padx=5, pady=5)

root.mainloop()