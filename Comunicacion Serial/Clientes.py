# -*- coding: utf-8 -*-
"""
TRABAJO FINAL PARTE - 2

@author: Jefri Robles Hernández ---------------------------- U201718395
"""
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 5000
HEADER_SIZE = 10


class Chat:
    def __init__(self, master):
        self.master = master
        
        # self.PORT = "COM1"
        
        self.master.title("Chat Grupal")
        self.master.geometry("+50+50")
        self.master.resizable(0, 0)
        self.master.config(bg = "#000000")
        
        self.texto_in = tk.StringVar()
        self.texto_in.set('')
        
        self.texto_in1 = tk.StringVar()
        self.texto_in1.set('127.0.0.1')
        
        self.texto_in2 = tk.StringVar()
        self.texto_in2.set('5000')
        
        self.username = tk.StringVar()
        self.username.set('Chat_User')
        
        self.th1 = None
        self.Alive = threading.Event()
        
        # ---------------------- Comunicacion --------------------------
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST,PORT))
        self.sock.close()
        self.texting = False
        
        # ------------------------ FRAMES -----------------------------
        frm1 = tk.LabelFrame(self.master, text="Conexion",bg = "#000000", fg = 'white')
        frm2 = tk.Frame(self.master, bg = "#000000")
        frm3 = tk.LabelFrame(self.master, text="Enviar mensaje" ,bg = "#000000", fg = 'white')
        
        frm1.pack(padx=5, pady=5, anchor=tk.W)
        frm2.pack(padx=5, pady=5, fill='y', expand=True)
        frm3.pack(padx=5, pady=5)
        
        # ------------------------ FRAME 1 ----------------------------
        self.lblIP = tk.Label(frm1, text="IP:", bg = "#000000", fg="White") 
        self.lblPort = tk.Label(frm1, text="PORT:", bg = "#000000", fg="White")
        self.lblUser = tk.Label(frm1, text="Username:", bg = "#000000", fg="White")
        self.inIP = ttk.Entry(frm1,textvariable = self.texto_in1, width = 20)
        self.inPort = ttk.Entry(frm1, textvariable = self.texto_in2, width = 20)
        self.inUser = ttk.Entry(frm1, textvariable = self.username, width = 20)
        self.lblSpace = tk.Label(frm1, text="", bg = '#000000')
        self.btnConnect = ttk.Button(frm1, text="Conectar", width=16, command = self.conectando)
        
        self.lblIP.grid(row=0, column=0, padx=5, pady=5)
        self.lblPort.grid(row=1, column=0, padx=5, pady=5)
        self.lblUser.grid(row=0, column=3, padx=5, pady=5)
        self.inIP.grid(row=0, column=1, padx=5, pady=5)
        self.inPort.grid(row=1, column=1, padx=5, pady=5)
        self.inUser.grid(row=0, column=4, padx=5, pady=5)
        self.lblSpace.grid(row=0,column=2, padx=11, pady=5)
        self.btnConnect.grid(row=1, column=4, padx=5, pady=5, sticky = 'E')
        
        
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
        self.inText.bind('<KeyRelease>', self.escribiendo)
               
        # --------------------------- StatusBar -----------------------
        self.statusBar = tk.Label(self.master, text = 'Comunicacion Multiple con Python',
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W, font='"MS Serif" 10',bg = "#000000", fg="White")
        self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)
            
        # ------------- Control del boton "X" de la ventana -----------
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar_puertos)
        
        # ------------- Lectura de datos ------------------------

    def sendMsg(self):
        # Bucle para la escritura de datos
        try:
            while self.Alive.isSet() :
                data_header = self.sock.recv(HEADER_SIZE)
                if not data_header:
                    self.Alive.clear()
                
                data = self.sock.recv(int(data_header)).decode('utf-8') + '\n'
                
                self.txtChat.tag_config('azulito', foreground='#2851DC')
                self.txtChat.config(state = 'normal')
                self.txtChat.insert(tk.INSERT,data, 'azulito')
                self.txtChat.config(state = 'disable')
                self.recibo_sms()
                self.txtChat.yview_moveto(1)
        except:
            pass
                
                    
    def cerrar_puertos(self):
        # Se cierran la comunicacion y la ventana de tkinter
        try:
            self.sock.close()
            self.stop_hilo()
        except:
            pass
        self.master.destroy()
    
    def conectando(self):
        # Presiono el botón para conectar
        if not self.texting and self.texto_in1.get() != '' and self.texto_in2.get() != '':
            if int(self.texto_in2.get()) > 1024:
                
                try:
                    
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.connect((self.texto_in1.get(), int(self.texto_in2.get())))
                    
                    self.ingreso = f'{self.username.get()} acaba de conectarse al chat' + '\n'
                    self.txtChat.tag_config('verde', foreground='#21C703')
                    self.txtChat.config(state = 'normal')
                    self.txtChat.insert(tk.INSERT,self.ingreso, 'verde')
                    self.txtChat.config(state = 'disable')
                    self.statusBar.config(text = f'Conectado al chat grupal como {self.username.get()}')
                    self.inIP.config(state = 'disable')
                    self.inPort.config(state = 'disable')
                    self.inUser.config(state = 'disable')
                    self.btnConnect.config(text = "Desconectar")
                    # self.btnSend.config(state = 'enable')
                    self.inText.config(state = 'normal')
                    self.texting = True
                    
                    self.inicio_hilo()
                    
                except:
                    self.stop_hilo()
                    self.sock.close()
                    self.statusBar.config(text = f'Error al conectarse a la ip {self.texto_in1.get()}')
            else:
                self.statusBar.config(text = 'El puerto debe ser mayor a 1023')
        # Presiono boton desconectar
        else:
            self.sock.close()
            self.stop_hilo()
            
            self.ingreso = f'{self.username.get()} acaba de salir del chat'+ '\n'
            self.txtChat.tag_config('rojito', foreground='#E60B3D')
            self.txtChat.config(state = 'normal')
            self.txtChat.insert(tk.INSERT,self.ingreso, 'rojito')
            self.txtChat.config(state = 'disable')
            self.inIP.config(state = 'normal')
            self.inPort.config(state = 'normal')
            self.inUser.config(state = 'normal')
            self.btnConnect.config(text = "Conectar")
            self.btnSend.config(state = 'disable')
            self.inText.config(state = 'disable')
            self.statusBar.config(text = 'Comunicacion Multiple con Python')
            self.texto_in.set('')
            self.texting = False
    
    def enviando(self, event):
        # Envio string con enter en el entry
        if len(self.inText.get()) > 0:
            self.txtChat.tag_config('morado', foreground='#963BA1')
            strData = self.texto_in.get()
            data_len = len(strData + self.username.get() + "> ") 
            self.string = f"{self.username.get()}> {strData}" + '\n'
            self.string2 = f"{data_len:<{HEADER_SIZE}}{self.username.get()}> {strData}"
            self.sock.send(self.string2.encode('utf-8'))
        
            self.txtChat.config(state = 'normal')
            self.txtChat.insert(tk.INSERT,self.string, 'morado')
            self.txtChat.config(state = 'disable')
            self.texto_in.set('')
            self.txtChat.yview_moveto(1)
        else:
            pass
    
    def enviando2(self):
        # Envio string con boton de enviar en el entry
        if len(self.inText.get()) > 0:
            self.txtChat.tag_config('morado', foreground='#963BA1')
            strData = self.texto_in.get()
            data_len = len(strData + self.username.get() + "> ") 
            self.string = f"{self.username.get()}> {strData}" + '\n'
            self.string2 = f"{data_len:<{HEADER_SIZE}}{self.username.get()}> {strData}"
            self.sock.send(self.string2.encode('utf-8'))
            
            self.txtChat.config(state = 'normal')
            self.txtChat.insert(tk.INSERT,self.string, 'morado')
            self.txtChat.config(state = 'disable')
            self.texto_in.set('')
            self.txtChat.yview_moveto(1)
        else:
            pass
        
        # self.inicio_hilo2()
        
    def inicio_hilo(self):
        # Primer hilo para la lectura de datos
        
        self.th1 = threading.Thread(target = self.sendMsg, daemon = True)
        self.Alive.set()
        self.th1.start()
    
    def stop_hilo(self):
        # Paro el hilo ya que es un bucle infinito
        if self.th1 is not None:
            
            self.Alive.clear()
            self.th1.join()
            self.th1 = None
        
    def recibo_sms(self):
        # Función para que se actualice el status bar por 1 seg
        
        self.statusBar.config(text = 'Recibiendo mensaje ...')
        time.sleep(0.5)
        self.statusBar.config(text = f'Conectado al chat grupal como {self.username.get()}')
    
    def escribiendo(self, event):
        if len(self.inText.get()) > 0:
            self.btnSend.config(state = 'normal')
            self.statusBar.config(text = 'Escribiendo....')
        else:
            self.btnSend.config(state = 'disable')
            self.statusBar.config(text = f'Conectado al chat grupal como {self.username.get()}')
    
    
root = tk.Tk()
app = Chat(root)
root.mainloop()
