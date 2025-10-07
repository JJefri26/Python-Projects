# -*- coding: utf-8 -*-
"""
TRABAJO FINAL - PARTE 1

@author: Jefri Robles Hernández --------------------- U201718395
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import serial
import serial.tools.list_ports
import threading
import time

class SerialChat:
    def __init__(self, master):
        self.master = master
        self.PORT = "COM1"
        
        self.master.title("Serial Chat")
        self.master.geometry("+50+50")
        self.master.resizable(0, 0)
        self.master.config(bg = "#000000")
        
        self.texto_in = tk.StringVar()
        self.texto_in.set('')
        
        self.th1 = None
        self.Alive = threading.Event()
        
        # ---------------------- SERIAL PORT --------------------------
        self.ports = serial.tools.list_ports.comports()
        self.puertos = []
        for port in self.ports:
            self.puertos.append(port[0])
            
        self.ser = serial.Serial(port=self.PORT, baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        self.ser.close()
        
        self.texting = False
        
        # ------------------------ FRAMES -----------------------------
        frm1 = tk.LabelFrame(self.master, text="Conexion",bg = "#000000", fg = 'white')
        frm2 = tk.Frame(self.master, bg = "#000000")
        frm3 = tk.LabelFrame(self.master, text="Enviar mensaje" ,bg = "#000000", fg = 'white')
        
        frm1.pack(padx=5, pady=5, anchor=tk.W)
        frm2.pack(padx=5, pady=5, fill='y', expand=True)
        frm3.pack(padx=5, pady=5)
        
        # ------------------------ FRAME 1 ----------------------------
        self.lblCOM = tk.Label(frm1, text="Puerto COM:", bg = "#000000", fg="White") 
        self.cboPort = ttk.Combobox(frm1, state = 'readonly', values=self.puertos)
        self.lblSpace = tk.Label(frm1, text="", bg = '#000000')
        self.btnConnect = ttk.Button(frm1, text="Conectar", width=16, command = self.conectando)
        
        self.lblCOM.grid(row=0, column=0, padx=5, pady=5)
        self.cboPort.grid(row=0, column=1, padx=5, pady=5)
        self.lblSpace.grid(row=0,column=2, padx=30, pady=5)
        self.btnConnect.grid(row=0, column=3, padx=5, pady=5)
        
        # ------------------------ FRAME 2 ---------------------------
        self.txtChat = ScrolledText(frm2, height=25, width=50, wrap=tk.WORD, state='disable', bg = '#DCE2F5')
        self.txtChat.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
                
        # ------------------------ FRAME 3 --------------------------
        self.lblText = tk.Label(frm3, text="Texto:", bg = "#000000", fg="White")
        self.inText = tk.Entry(frm3, textvariable = self.texto_in, width=45, state='disable', bg="#e6e4d9")
        self.btnSend = ttk.Button(frm3, text="Enviar", width=12, state='disable', command = self.enviando2)
        
        self.lblText.grid(row=0, column=0, padx=5, pady=5)
        self.inText.grid(row=0, column=1, padx=5, pady=5)
        self.btnSend.grid(row=0, column=2, padx=5, pady=5)
        self.inText.bind('<Return>', self.enviando)
               
        # --------------------------- StatusBar -----------------------
        self.statusBar = tk.Label(self.master, text = 'Comunicacion Serial con Python',
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W, font='"MS Serif" 10',bg = "#000000", fg="White")
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)
            
        # ------------- Control del boton "X" de la ventana -----------
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar_puertos)
        
        # ------------- Lectura de datos ------------------------

    def leyendo(self):
        # Bucle para la lectura de datos
        while self.Alive.isSet() and self.ser.is_open:

                if self.ser.in_waiting > 0:
                    self.data2 = self.ser.readline()
                    self.string = self.data2.decode('utf-8')
                    
                    self.txtChat.tag_config('azulito', foreground='#2851DC')
                    self.txtChat.config(state = 'normal')
                    self.txtChat.insert(tk.INSERT,self.string, 'azulito')
                    self.txtChat.config(state = 'disable')
                    self.recibo_sms()
                    self.txtChat.yview_moveto(1)
                
                    
    def cerrar_puertos(self):
        # Se cierran los puertos COM y la ventana de tkinter
        try:
            self.stop_hilo()
            self.ser.close()
        except:
            pass
        self.master.destroy()
    
    def conectando(self):
        # Presiono el botón para conectar
        if not self.texting:
            try:
                self.ser.close()
                self.ser = serial.Serial(port = self.cboPort.get(), baudrate=9600, bytesize=8,
                                         timeout=2, stopbits=serial.STOPBITS_ONE)
                
                self.statusBar.config(text = f'Conectado al {self.cboPort.get()} a 9600')
                self.cboPort.config(state = 'disable')
                self.btnConnect.config(text = "Desconectar")
                self.btnSend.config(state = 'enable')
                self.inText.config(state = 'normal')
                self.texting = True
                
                self.inicio_hilo()
                
            except:
                self.stop_hilo()
                self.ser.close()
                self.statusBar.config(text = f'Error al conectarse a {self.cboPort.get()}')
        # Presiono boton desconectar
        else:
            self.stop_hilo()
            self.ser.close()
            self.cboPort.config(state = 'readonly')
            self.btnConnect.config(text = "Conect")
            self.btnSend.config(state = 'disable')
            self.inText.config(state = 'disable')
            self.statusBar.config(text = 'Comunicacion Serial con Python')
            self.texting = False
    
    def enviando(self, event):
        # Envio string con enter en el entry
        self.txtChat.tag_config('morado', foreground='#963BA1')
        data = f"{self.cboPort.get()}: {self.texto_in.get()}" + '\n'
        self.txtChat.config(state = 'normal')
        self.txtChat.insert(tk.INSERT,data, 'morado')
        self.txtChat.config(state = 'disable')
        self.ser.write(data.encode('utf-8'))
        self.texto_in.set('')
        self.txtChat.yview_moveto(1)
        
        # self.envio_sms()
        self.inicio_hilo2()
    
    def enviando2(self):
        # Envio string con boton de enviar en el entry
        self.txtChat.tag_config('morado', foreground='#963BA1')
        data = f"{self.cboPort.get()}: {self.texto_in.get()}" + '\n'
        self.txtChat.config(state = 'normal')
        self.txtChat.insert(tk.INSERT,data, 'morado')
        self.txtChat.config(state = 'disable')
        self.ser.write(data.encode('utf-8'))
        self.texto_in.set('')
        self.txtChat.yview_moveto(1)
        
        # self.envio_sms()
        self.inicio_hilo2()
        
    def inicio_hilo(self):
        # Primer hilo para la lectura de datos
        self.th1 = threading.Thread(target = self.leyendo, daemon = True)
        self.Alive.set()
        self.th1.start()
    
    def stop_hilo(self):
        # Paro el hilo ya que es un bucle infinito
        if self.th1 is not None:
            self.Alive.clear()
            self.th1.join()
            self.th1 = None
    
    def inicio_hilo2(self):
        # Segundo hilo para que se actualice el status bar
        self.th2 = threading.Thread(target = self.envio_sms, daemon = True)
        self.th2.start()
            
    def envio_sms(self):
        # Funcion para que actualice el status bar por 1 seg
        self.statusBar.config(text = 'Enviando mensaje ...')
        time.sleep(1)
        self.statusBar.config(text = f'Conectado al {self.cboPort.get()} a 9600')
        
    def recibo_sms(self):
        # Función para que se actualice el status bar por 1 seg
        self.statusBar.config(text = 'Recibiendo mensaje ...')
        time.sleep(1)
        self.statusBar.config(text = f'Conectado al {self.cboPort.get()} a 9600')
    
    
root = tk.Tk()
app = SerialChat(root)
root.mainloop()

