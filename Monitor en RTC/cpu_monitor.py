# -*- coding: utf-8 -*-
"""
@author: Jaime Jefri Robles Hernandez ----- U201718395
"""

import datetime
import psutil
import tkinter as tk
import tkinter.ttk as ttk
#import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data1 = []
data2 = []


class App:
    global data1, data2
    
    def __init__(self, master):
        self.master = master
        self.master.title("Monitor de Recursos")
        self.master.geometry("620x320+100+100")
        self.master.resizable(0, 0)
        self.master.config(bg = "#000000")

        # Variables para los porcentajes
        self.var_Pusage_CPU = tk.DoubleVar()
        self.var_Pusage_Ram = tk.DoubleVar()
        self.var_Pusage_HDD = tk.DoubleVar()
        
        # Variables para los datos enteros
        self.var_usage_CPU = tk.IntVar()
        self.var_usage_Ram = tk.DoubleVar()
        self.var_usage_HDD = tk.DoubleVar()
        
        #Valores para la barra de estado
        self.var_in = tk.IntVar()
        self.var_out = tk.IntVar()
        self.var_fecha = tk.StringVar()
        self.var_espacio = tk.StringVar()
        
        # Para el Canva
        self.var_Datos = tk.IntVar(value=1)
        
        # ---------------------------------- Status Bar ------------------------------------------
        self.statusbar = tk.Label(self.master, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, font='"MS Serif" 10',bg = "#000000", fg="White")
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # ---------------------------------- Frames ------------------------------------------
        
        frmI = tk.Frame(self.master,bg = "#000000")
        frmD = tk.Frame(self.master,bg = "#000000")
        frmI.pack(side=tk.LEFT)
        frmD.pack(side=tk.LEFT)
        
        # ---------------------------------- Frame D ------------------------------------------
        # ---------------------------------- Canva ------------------------------------------
        
        
        self.fig, self.ax = plt.subplots(figsize=(5, 3), facecolor="#000000")
        self.line, = self.ax.plot([10],color='#FF0252')
        self.ax.grid(linestyle=":")
        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(0, 100)
        self.ax.set_title("CPU Usage [%]", color="white", font = '"MS Serif" 18')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set_xticklabels([""])
        self.ax.set_yticklabels([0,20,40,60,80,100], color = "white")
        self.ax.set_facecolor('#000000')
        self.ax.set_xlabel("Jefri Robles Hernandez", color = "white")
        
        self.graph = FigureCanvasTkAgg(self.fig, master=frmD)
        self.graph.get_tk_widget().pack(expand=True, fill=tk.X)
        
        
        # ---------------------------------- Frame I ------------------------------------------
        
        self.lblCPU_Usage = tk.Label(frmI, text="", font='"MS Serif" 12',bg = "#000000", fg="White")
        self.lblRam_Usage = tk.Label(frmI, text="", font='"MS Serif" 12',bg = "#000000", fg="White")
        self.lblHDD_Usage = tk.Label(frmI, text="", font='"MS Serif" 12',bg = "#000000", fg="White")
        
        self.s = ttk.Style()
        self.s.theme_use('alt')
        self.s.configure("red.Horizontal.TProgressbar", troughcolor='#EAEDF6', background='#FF0252',border = 5 )
        
        self.Barra1 = ttk.Progressbar(frmI,orient='horizontal', mode='determinate',length=270,style="red.Horizontal.TProgressbar")
        self.Barra2 = ttk.Progressbar(frmI,orient='horizontal', mode='determinate',length=270,style="red.Horizontal.TProgressbar")
        self.Barra3 = ttk.Progressbar(frmI,orient='horizontal', mode='determinate',length=270,style="red.Horizontal.TProgressbar")

        
        
        self.lblCPU_Usage.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.lblRam_Usage.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.lblHDD_Usage.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.Barra1.grid(row=2, column=0, columnspan=2, padx=10, pady=20, sticky=tk.W)
        self.Barra2.grid( row=4, column=0, columnspan=2, padx=10, pady=20, sticky=tk.W)
        self.Barra3.grid( row=6, column=0, columnspan=2, padx=10, pady=20, sticky=tk.W)
        

                
        self.read_psutil_data()
        
    
    def read_psutil_data(self):
        # Obtencion de datos del CPU
        
        self.var_usage_CPU.set(psutil.cpu_count(logical=False))
        self.var_Pusage_CPU.set(psutil.cpu_percent())
        
        # Obtencion de datos de la RAM
        self.var_usage_Ram.set(psutil.virtual_memory().total/1024/1024/1024)
        self.var_Pusage_Ram.set(psutil.virtual_memory().percent)
        
        # Obtencion de datos del Disco Madre
        self.var_usage_HDD.set(psutil.disk_usage("/").total/1024/1024/1024)
        self.var_Pusage_HDD.set(psutil.disk_usage("/").percent)
        
        # Obtencion de datos del internet
        self.var_in.set(psutil.net_io_counters().bytes_recv)
        self.var_out.set(psutil.net_io_counters().bytes_sent)
        
        # Obtencion de datos de la fecha
        self.var_fecha.set(datetime.datetime.now().strftime("%F %T"))
        self.var_espacio.set(" "*90)
        
        # Escribo lo que obtengo o reemplazo
        self.lblCPU_Usage.config(text=f"CPU Usage ({self.var_usage_CPU.get()} core): {self.var_Pusage_CPU.get()}%")
        self.lblRam_Usage.config(text=f"RAM Usage (Total: {self.var_usage_Ram.get():.2f} Gb): {self.var_Pusage_Ram.get()}%")
        self.lblHDD_Usage.config(text=f"HDD Usage (Total: {self.var_usage_HDD.get():.2f} Gb): {self.var_Pusage_HDD.get()}%")
        self.statusbar.config(text=f"Net info [in: {self.var_in.get():,}| out: {self.var_out.get():,}] {self.var_espacio.get()} {self.var_fecha.get():20}")
        
        # Escribo los valores de las barras
        self.Barra1['value'] = self.var_Pusage_CPU.get()
        self.Barra2['value'] = self.var_Pusage_Ram.get()
        self.Barra3['value'] = self.var_Pusage_HDD.get()
        
        data1.append(self.var_Pusage_CPU.get())
        data2 = [x for x in range(1,len(data1)+1)]
                
        self.line.set_ydata(data1)
        self.line.set_xdata(data2)
        self.graph.draw()
                
        self.master.after(1000, self.read_psutil_data)
    
    


root = tk.Tk()
app = App(root)
root.mainloop()
