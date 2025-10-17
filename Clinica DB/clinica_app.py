# -*- coding: utf-8 -*-
# Alumno: Jaime Jefri Robles Hernández

import tkinter as tk
import tkinter.ttk as ttk
from db_clinica import Database
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as mticker


class MainWindow:
    def __init__(self, master):
        # Definicion de la Ventana Principal
        
        self.master = master
        self.master.title("Clinica Peso Feliz")
        self.master.resizable(0, 0)
        
        self.db = Database()
        
        style = ttk.Style()
        style.theme_use('default')
        
        style.configure("Treeview",)
        style.map("Treeview", background=[('selected', '#FF0252')])
        
        frm = tk.Frame(self.master)
        frm.pack(padx=10, pady=10)
        
        frm1 = tk.LabelFrame(frm, text="Medicos")
        frm1.pack(side=tk.LEFT, padx=10, pady=10)
        frm2 = tk.LabelFrame(frm, text="Data Pacientes")
        frm2.pack(side=tk.LEFT, padx=10, pady=10)
        
        # -------------------------- frm1 ------------------------------
        # Tabla para el registro de los Medicos
        self.tabMedicos = ttk.Treeview(frm1, columns=[1, 2])
        self.tabMedicos.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        self.tabMedicos.heading("#0", text="ID")
        self.tabMedicos.heading("#1", text="Nombre")
        self.tabMedicos.heading("#2", text="Apellido")
        
        self.tabMedicos.column('#0', width=100, minwidth=100, stretch=tk.NO)
        self.tabMedicos.column('#1', width=100, minwidth=100, stretch=tk.NO)
        self.tabMedicos.column('#2', width=100, minwidth=100, stretch=tk.NO)
        
        self.tabMedicos.tag_configure('even', background='#e6f7b2')
        self.tabMedicos.tag_configure('odd', background='#f4fae1')
        
        for idx, medico in enumerate(self.db.listar_medicos()):            
            if idx % 2:
                self.tabMedicos.insert("", tk.END, text=medico[0], values=medico[1:], tags='even')
            else:
                self.tabMedicos.insert("", tk.END, text=medico[0], values=medico[1:], tags='odd')
        
        self.tabMedicos.bind("<<TreeviewSelect>>", self.update_data_patients)
                
        # NOTA: Al hacer click a un medico debe llamar al metodo self.update_data_patients
        
        # -------------------------- frm2 ------------------------------ 
        # Tabla con el registro de los Pacientes + Scrollbar Vertical
        self.scrY = tk.Scrollbar(frm2, orient='vertical')
        self.tabPacientes = ttk.Treeview(frm2, columns=(1, 2, 3, 4, 5), 
                                         yscrollcommand=self.scrY.set,
                                         selectmode='browse')
        self.scrY.configure(command=self.tabPacientes.yview)
        
        self.tabPacientes.pack(side=tk.LEFT, padx=5, pady=5)
        self.scrY.pack(side=tk.LEFT, expand=True, fill=tk.Y)
        
        self.tabPacientes.heading("#0", text="ID")
        self.tabPacientes.heading("#1", text="Apellido")
        self.tabPacientes.heading("#2", text="Nombre")
        self.tabPacientes.heading("#3", text="Altura")
        self.tabPacientes.heading("#4", text="Edad")
        self.tabPacientes.heading("#5", text="Sexo")
        
        self.tabPacientes.column('#0', width=100, minwidth=100, stretch=tk.NO)
        self.tabPacientes.column('#1', width=100, minwidth=100, stretch=tk.NO)
        self.tabPacientes.column('#2', width=100, minwidth=100, stretch=tk.NO)
        self.tabPacientes.column('#3', width=80, minwidth=80, stretch=tk.NO)
        self.tabPacientes.column('#4', width=80, minwidth=80, stretch=tk.NO)
        self.tabPacientes.column('#5', width=80, minwidth=80, stretch=tk.NO)
        
        self.tabPacientes.tag_configure('even',background='#e6f7b2')
        self.tabPacientes.tag_configure('odd', background='#f4fae1')
        
        self.tabPacientes.bind("<<TreeviewSelect>>", self.open_graph_window)
        
        
        # NOTA: Al hacer click a un paciente debe llamar a self.open_graph_window
        
        # ------------------------ statusbar ---------------------------
        self.statusbar = tk.Label(self.master, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tabMedicos.bind("<Enter>", lambda x: self.update_statusbar("Haga click para ver los pacientes asigandos al medico"))
        self.tabMedicos.bind("<Leave>", lambda x: self.update_statusbar(""))
        self.tabPacientes.bind("<Enter>", lambda x: self.update_statusbar("Haga click para ver el registro de peso del paciente"))
        self.tabPacientes.bind("<Leave>", lambda x: self.update_statusbar(""))


    def update_statusbar(self, message):
        # Actualiza los mensajes en el statusbar
        self.statusbar.config(text=message)
        
        
    def update_data_patients(self, event):
        # Carga con datos la tabla de pacientes al seleccionar un medico
        idx = self.tabMedicos.selection()
        pacient = self.tabMedicos.item(idx)['text']
        
        self.tabPacientes.delete(*self.tabPacientes.get_children())
        
        for idx,paciente in enumerate(self.db.listar_pacientes_medico(pacient)):
            if idx % 2:
                self.tabPacientes.insert("", tk.END, text=paciente[0], values=paciente[1:], tags = 'even')
            else:
                self.tabPacientes.insert("", tk.END, text=paciente[0], values=paciente[1:], tags = 'odd')
    
    def open_graph_window(self, event):
        # Abre la ventana secundaria con el grafico de peso
        
        idx = self.tabPacientes.selection()
        if not idx:
            return
        
        id_pac = self.tabPacientes.item(idx)['text']
        
        window = tk.Toplevel(self.master)
        GraphWindow(window, id_pac)
    
    
    
class GraphWindow:
    def __init__(self, master, id_pac):
        # Definicion de la ventana grafica
        # (requiere id_pac para cargar los datos de un paciente)
        self.master = master
        self.master.title("Details Window")
        self.master.geometry("550x400+50+50")
        self.master.grab_set()
        self.master.focus()
        self.master.config(bg = "#000000")
        self.master.resizable(0, 0)
        
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.db = Database()
        
        frm = tk.Frame(self.master,bg = "#000000")
        frm.pack()
        
        self.var_name = self.db.nombre_paciente(id_pac)
        self.var_pesos = self.db.data_peso(id_pac)
        self.var_pesos_min = round(min(self.var_pesos)-5)
        self.var_pesos_max = round(min(self.var_pesos)+5)
        
        # ------------------ Canva ----------------------------------
        label_format = '{:,.0f}'
        self.fig, self.ax = plt.subplots(figsize=(6, 4), facecolor="#000000")
        self.line, = self.ax.plot(self.var_pesos,'-s',color='#FF0252',markersize=5)
        self.ax.grid(linestyle=":")
        self.ax.set_ylim(min(self.var_pesos)-5, max(self.var_pesos)+5)
        self.ax.set_xlim(0, len(self.var_pesos)+2)
        self.ax.set_title(f"Paciente - {self.var_name[0]} {self.var_name[1]}", color="white")
        #self.ax.spines['top'].set_visible(False)
        #self.ax.spines['right'].set_visible(False)
        ticks_locy = self.ax.get_yticks().tolist()
        ticks_locx = self.ax.get_xticks().tolist()
        self.ax.yaxis.set_major_locator(mticker.FixedLocator(ticks_locy))
        self.ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_locx))
        #self.ax.set_xticklabels([0,2,4,6,8,10,12,14,16,18], color = "white")
        self.ax.set_xticklabels([label_format.format(x) for x in ticks_locx], color = "white")
        #self.ax.set_yticklabels([i for i in range(self.var_pesos_min,self.var_pesos_max)], color = "white")
        self.ax.set_yticklabels([label_format.format(x) for x in ticks_locy], color = "white")
        self.ax.set_facecolor('#000000')
        self.ax.set_xlabel("Semana", color = "white")
        self.ax.set_ylabel("Peso [Kg]", color = "white")
        
        self.graph = FigureCanvasTkAgg(self.fig, master=frm)
        self.graph.get_tk_widget().pack(expand=True, fill=tk.X)
        
    def on_close(self):
        
        plt.close(self.fig)  # <-- Cierra la figura para liberar memoria
        self.master.destroy()
        

root = tk.Tk()
app = MainWindow(root)
root.mainloop()
