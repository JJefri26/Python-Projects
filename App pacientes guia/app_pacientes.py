# -*- coding: utf-8 -*-
#%%
# PREPARACION DE LOS DATOS Y LA DB
import sqlite3
from random import randint, uniform, choice

def random_data():
    N_PAC = 25
    
    dataset = set()
    nombres = ["Enzo", "Rosa", "Ruben", "Marcelo", "Ernesto", "Carlos",
               "Marcial", "Diana", "Carolina", "Eduardo", "Ricardo", "Ana"]
    apellidos = ["Ramirez", "Quispe", "Jimenez", "Perez", "Samame", 
                 "Vicente", "Rojas", "Quiroz", "Quevedo", "Martinez", 
                 "Vengas", "Ramos"]
    
    while len(dataset) < N_PAC:
        dataset.add((choice(nombres) + ' ' + choice(apellidos), 
                     randint(50, 120), 
                     round(uniform(1.50, 1.90), 2)))
    
    return list(dataset)
      
conn = sqlite3.connect("database.db")

with conn:
    cur = conn.cursor()
    
    try:
        cur.execute("DROP TABLE pacientes")
    except:
        pass
    
    cur.execute("""CREATE TABLE IF NOT EXISTS pacientes 
                        (id_pac INTEGER PRIMARY KEY, 
                         nombre TEXT NOT NULL, 
                         peso INTEGER NOT NULL, 
                         altura REAL NOT NULL)
                """)
    cur.executemany("""INSERT INTO pacientes 
                           (nombre, 
                            peso, 
                            altura) 
                        VALUES (?, ?, ?)""", random_data())

conn.close()

#%%
# APP REGISTRO DE PACIENTES
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import askyesno, showerror, showinfo
import sqlite3

class Database:
    datafile = "database.db"
    def __init__(self):
        self.conn = sqlite3.connect(Database.datafile)
        self.cur = self.conn.cursor()
        
    def __del__(self):
        self.conn.close()
        
    def info_pacientes(self):
        sql = "SELECT * FROM pacientes ORDER BY id_pac"
        return self.cur.execute(sql).fetchall()

    def add_record(self, nombre, peso, altura):
        try:
            sql = """INSERT INTO pacientes 
                          (nombre, peso, altura) 
                     VALUES (?, ?, ?)"""
            self.cur.execute(sql, (nombre, peso, altura))
            self.conn.commit()
        except:
            raise TypeError()
            

    def update_record(self, nombre, peso, altura, id_pac):
        try:
            sql = """UPDATE pacientes 
                     SET nombre = ?, peso = ?, altura = ? 
                     WHERE id_pac = ?"""
            self.cur.execute(sql, (nombre, peso, altura, id_pac))
            self.conn.commit()
        except:
            raise TypeError()


class App_Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Reg Pacientes")
        self.master.resizable(0, 0)
        self.master.protocol("WM_DELETE_WINDOW", self.close_app)
        
        style = ttk.Style()
        style.theme_use('default')
        style.map("Treeview", background = [('selected', 'blue')])
        
        self.db = Database()
        
        self.field_id = ""
        self.field_nombre = ""
        self.field_peso = ""
        self.field_altura = ""
        
        frm = tk.Frame(self.master)
        frm1 = tk.Frame(frm)
        frm2 = tk.Frame(frm)
        frm.pack(padx=10, pady=10)
        frm1.pack(padx=10, pady=10)
        frm2.pack(padx=10, pady=10, anchor=tk.E)
        
        self.statusbar = tk.Label(self.master, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # ------------------------- frm1 --------------------------
        self.scrY = tk.Scrollbar(frm1, orient='vertical')
        self.table = ttk.Treeview(frm1, columns=(1, 2, 3), yscrollcommand=self.scrY.set)
        self.scrY.config(command=self.table.yview)
        
        self.table.pack(side=tk.LEFT)
        self.scrY.pack(side=tk.LEFT, expand=True, fill=tk.Y)
        
        self.table.heading("#0", text="ID")
        self.table.heading("#1", text="NOMBRE")
        self.table.heading("#2", text="PESO")
        self.table.heading("#3", text="ALTURA")
        
        self.table.column("#0", width=40, minwidth=40, stretch=False)
        self.table.column("#1", width=120, minwidth=180, stretch=False)
        self.table.column("#2", width=80, minwidth=80, stretch=False, anchor=tk.E)
        self.table.column("#3", width=80, minwidth=80, stretch=False, anchor=tk.E)
        
        self.table.tag_configure("color", background="lightgray")
        
        for idx, item in enumerate(self.db.info_pacientes()):
            if idx % 2 == 0:
                self.table.insert("", tk.END, text=item[0], values=item[1:], tags=('color',))
            else:
                self.table.insert("", tk.END, text=item[0], values=item[1:])
        
        # Binds
        self.table.bind("<<TreeviewSelect>>", self.select_item)
        self.table.bind("<Enter>", lambda x: self.statusbar.config(text="Tabla de datos. Haga click en una fila para modificar..."))
        self.table.bind("<Leave>", lambda x: self.statusbar.config(text=""))
        
        # ------------------------- frm2 --------------------------
        self.btnModificar = ttk.Button(frm2, text="Modificar", state="disable",
                                       command=lambda:self.open_reg_window('update',
                                                                           self.field_id,
                                                                           self.field_nombre, 
                                                                           self.field_peso, 
                                                                           self.field_altura))
        self.btnInsertar = ttk.Button(frm2, text="Insertar", 
                                      command=lambda:self.open_reg_window('insert'))
        self.btnSalir = ttk.Button(frm2, text="Salir", command=self.close_app)
        
        self.btnModificar.grid(row=0, column=0, padx=5, pady=5)
        self.btnInsertar.grid(row=0, column=1, padx=5, pady=5)
        self.btnSalir.grid(row=0, column=2, padx=5, pady=5)

        # Binds
        self.btnModificar.bind("<Enter>", lambda x: self.statusbar.config(text="Modifica un registro"))
        self.btnModificar.bind("<Leave>", lambda x: self.statusbar.config(text=""))
        self.btnInsertar.bind("<Enter>", lambda x: self.statusbar.config(text="Agrega un registo"))
        self.btnInsertar.bind("<Leave>", lambda x: self.statusbar.config(text=""))
        self.btnSalir.bind("<Enter>", lambda x: self.statusbar.config(text="Salir de la aplicacion"))
        self.btnSalir.bind("<Leave>", lambda x: self.statusbar.config(text=""))        

    def select_item(self, event):
        self.btnModificar.config(state='normal')
        idx = self.table.selection()
        self.field_id = self.table.item(idx)['text']
        self.field_nombre, self.field_peso, self.field_altura = self.table.item(idx)['values']
        
    def open_reg_window(self, operation, id_="", nombre="", peso="", altura=""):
        window = tk.Toplevel()
        Reg_Window(window, operation, self.db, id_, nombre, peso, altura)        
        window.wait_window()
        
        self.table.delete(*self.table.get_children())
        for idx, item in enumerate(self.db.info_pacientes()):
            if idx % 2 == 0:
                self.table.insert("", tk.END, text=item[0], values=item[1:], tags=('color',))
            else:
                self.table.insert("", tk.END, text=item[0], values=item[1:])
        
        self.btnModificar.config(state='disable')
        
    def close_app(self):
        if askyesno("Salir", "Desea salir de la aplicacion?"):
            self.master.destroy()
        

class Reg_Window:
    def __init__(self, master, operation, db, item0=None, item1="", item2="", item3=""):
        self.master = master
        self.master.title("Data Pacientes")
        self.master.resizable(0, 0)
        self.master.focus()
        self.master.grab_set()
        self.db = db
        
        self.operation = operation
        self.field_id = item0
        self.field_nombre = tk.StringVar(value=item1)
        self.field_peso = tk.StringVar(value=item2)
        self.field_altura = tk.StringVar(value=item3)

        frm = tk.Frame(self.master)
        frm1 = tk.Frame(frm)
        frm2 = tk.Frame(frm)
        frm.pack(padx=10, pady=10)
        frm1.pack(padx=10, pady=10)
        frm2.pack(padx=10, pady=10)
        
        # ------------------------ frm1 --------------------------------
        self.lblNombre = tk.Label(frm1, text="Nombre")
        self.lblPeso = tk.Label(frm1, text="Peso")
        self.lblAltura = tk.Label(frm1, text="Altura")
        self.entNombre = tk.Entry(frm1, width=25, textvariable=self.field_nombre)
        self.entPeso = tk.Entry(frm1, width=8, textvariable=self.field_peso)
        self.entAltura = tk.Entry(frm1, width=8, textvariable=self.field_altura)
        
        self.lblNombre.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.lblPeso.grid(row=1, column=0,  padx=5, pady=5, sticky=tk.E)
        self.lblAltura.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.entNombre.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.entPeso.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.entAltura.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # ------------------------ frm2 --------------------------------
        self.btnAceptar = ttk.Button(frm2, text="Aceptar", command=self.operate_table)
        self.btnSalir = ttk.Button(frm2, text="Salir", command=self.master.destroy)
        
        self.btnAceptar.grid(row=0, column=0, padx=5, pady=5)
        self.btnSalir.grid(row=0, column=1, padx=5, pady=5)
        
        
    def operate_table(self):
        if self.operation == "insert":
            try:
                self.db.add_record(self.field_nombre.get(), 
                                   int(self.field_peso.get()), 
                                   float(self.field_altura.get()))
                showinfo("Registro", "Los campos se registraron con exito", 
                         parent=self.master)
                self.master.destroy()
            except:
                showerror("Error", "Los campos no tienen información correcta", 
                          parent=self.master)
                
        elif self.operation == "update":
            try:
                self.db.update_record(self.field_nombre.get(), 
                                   int(self.field_peso.get()), 
                                   float(self.field_altura.get()), 
                                   self.field_id)
                showinfo("Registro", "Los campos se modificaron con exito", 
                         parent=self.master)
                self.master.destroy()
            except:
                showerror("Error", "Los campos no tienen información correcta", 
                          parent=self.master)
                


root = tk.Tk()
app = App_Main(root)
root.mainloop()

