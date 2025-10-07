# -*- coding: utf-8 -*-
"""
@author: Jefri Robles Hernández
TIU : U201718395
"""
## ------------------------------------------------------------------------------------ ##
# LABORATORIO CALIFICADO 3
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from datetime import datetime
cont = 0

class App(tk.Tk):
    global cont
    def __init__(self):
        super().__init__()
        self.title("Kiosko de fotos - Guiños")
        self.resizable(0, 0)
        self.config(bg = "#000000")
        self.protocol("WM_DELETE_WINDOW", self.close_app)
        
        self.cap = cv2.VideoCapture(0)
        self.width, self.height = 640, 480
        
        frm = tk.Frame(self, bg = "#000000")
        frm1 = tk.LabelFrame(frm, text="Preview",font = '"MS Serif" 12', bg = "#000000", fg='white')
        
        frm.pack(padx=10, pady=10)
        frm1.pack(padx=10, pady=10)
        
    
        # -------------------------- frm 1 ----------------------------------       
        self.canvas = tk.Canvas(frm1,  width=self.width, height=self.height, bg="#000000",highlightbackground = "#000000")
        self.canvas.pack()
        
        self.statusbar = tk.Label(self, text="Detectando rostro",font = '"MS Serif" 12', bd=1, relief=tk.SUNKEN, anchor=tk.W,bg = "#000000", fg="White")
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
        
        self.cam_loop()
        
    def cam_loop(self):
        ret, frame = self.cap.read()
        cont = 0
        if ret:
            self.statusbar.config(text = "Detectando rostro")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.width, self.height))
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(frame, (self.width, self.height))
            
            faces = self.face_cascade.detectMultiScale(gray, 1.2, 12)
            
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (223,54,120), 2)
                cv2.putText(frame, "Rostro Detectado", (x,y-12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (229,27,106), 2)
        
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                
                eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.12, 18)
                
                if len(eyes) == 0:
                    cont = cont + 1 
                
                if cont == 1:
                    self.after(50, self.take_pic())
                    
                    
                self.statusbar.config(text = "Rostro detectado")
                
                for ex, ey, ew, eh in eyes:
                    cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (38,136,238),2)
                    
            try:
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=photo, anchor='nw')
                self.canvas.image = photo
                
            except:
                pass
        
        self.after(20, self.cam_loop)
        
        
    def close_app(self):
        if self.cap.isOpened():
            self.cap.release()
            
        self.destroy()
        
        
    def take_pic(self):
        # Capturar un frame
        ret, frame = self.cap.read()
        filename = f"{datetime.strftime(datetime.now(), '%Y%m%d_%H%M')}.jpg"
        
        if ret:
            cv2.imwrite(filename, frame)
            PhotoWindow(filename)
            
        
class PhotoWindow(tk.Toplevel):
    def __init__(self, filename):
        super().__init__()
        self.title("Multimedia Kiosk - Photo Preview")
        self.resizable(0, 0)
        self.grab_set()
        self.focus()
        width, height = 640, 480
        
        canvas = tk.Canvas(self, width=width+20, height=height+20, 
                           borderwidth=1, relief=tk.SUNKEN,  bg="#000000",highlightbackground = "#000000")
        canvas.pack()
        
        self.statusbar = tk.Label(self, text="Imagen Capturada",font = '"MS Serif" 12', bd=1, relief=tk.SUNKEN, anchor=tk.W,bg="#000000", fg = 'white')
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        cv_img = cv2.imread(filename, cv2.IMREAD_COLOR)
        cv_img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        cv_img_re = cv2.resize(cv_img_rgb, (width, height))
        
        try:
            photo = ImageTk.PhotoImage(image=Image.fromarray(cv_img_re))
            canvas.create_image(width//2 + 13, height//2 + 13, image=photo)
            canvas.image = photo
        except:
            pass
        
App().mainloop()

    