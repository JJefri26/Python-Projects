# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 04:11:32 2021

@author: Jefri
"""

import sqlite3
import requests
import zipfile
import os

#%%
URL = r"https://cdn.sqlitetutorial.net/wp-content/uploads/2018/03/chinook.zip"
HOME_PATH = os.getcwd()
PATH = os.path.join(HOME_PATH, "datafile")
filename = URL.split("/")[-1]
r = requests.get(URL)

try:
    print(f"Descargando {filename} de {URL}... ", end='')
    with open(filename, mode='wb') as file:
        file.write(r.content) #extrae contenido o lo descarga
    print("Hecho")  
    
    print(f"Descomprimiendo archivo {filename}... ", end='')
    with zipfile.ZipFile(filename, mode='r') as zip_ref:
        zip_ref.extractall(".//datafile")
    print("Hecho")
except:
    print(f"No se puede obtener el archivo {filename}")
    

#%%
database_file = ".//datafile//chinook.db"
conn = sqlite3.connect(database_file)

#%%
with conn:
    cur = conn.cursor()
    results = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    
    print(f"Tablas en {database_file}")
    print("----------" + "-" * len(database_file))
    for item in results:
        print(item)
conn.close()

#%%
import sqlite3
datafile = "datafile//chinook.db"

with sqlite3.connect(datafile) as conn:
    cur = conn.cursor()
    
    parameters = "Metallica"
    sql = "SELECT * FROM artists WHERE Name = ?"
    #cur.execute(sql, (parameters,))
    
    for item in cur.execute(sql, (parameters,)):
        print(item)
    

conn.close()

#%% Consultar los albums del artista
import sqlite3
datafile = "datafile//chinook.db"

with sqlite3.connect(datafile) as conn:
    cur = conn.cursor()
    
    parameters = "Metallica"
    sql = """SELECT Title
             FROM albums JOIN artists
             ON albums.ArtistId = artists.ArtistId
             Where artists.Name = ?"""

    data = cur.execute(sql, (parameters,)).fetchall()
    
    for idx, item in enumerate(data,start=1):
        print(f"{idx:2}. {item[0]}")
    
    sql = """SELECT COUNT(albums.Title)
             FROM albums JOIN artists
             ON albums.ArtistId = artists.ArtistId
             Where artists.Name = ?"""

    num_albums = cur.execute(sql, (parameters,)).fetchone()[0]
    print(f"\nHay {num_albums} albums registrados en la tienda")
    

conn.close()

#%% Listado de albums y tracks
import sqlite3
datafile = "datafile//chinook.db"

with sqlite3.connect(datafile) as conn:
    cur = conn.cursor()
    
    parameters = "Metallica"
    sql = """SELECT albums.AlbumId, albums.Title
             FROM albums JOIN artists
             ON albums.ArtistId = artists.ArtistId
             Where artists.Name = ?
             ORDER BY albums.Title"""
    
    albums_data = cur.execute(sql, (parameters,)).fetchall()
    
    for album_id, album_title in albums_data:
        sql = """SELECT Name, UnitPrice FROM tracks WHERE AlbumId = ?"""
        tracks = cur.execute(sql, (album_id,)).fetchall()
        print(f"{album_title}")
        for track in tracks:
            print(f"\t- {track[0]} ({track[1]} USD)")
        else:
            print()
    

conn.close()

#%%
import sqlite3
datafile = "datafile//chinook.db"

with sqlite3.connect(datafile) as conn:
    cur = conn.cursor()
    
    parameters = "Metallica"
    sql = """SELECT albums.Title, 
                    SUM(tracks.UnitPrice),
                    COUNT(tracks.UnitPrice)
             FROM artists
                 JOIN albums
                 JOIN tracks
            ON artists.ArtistId = albums.ArtistId
                AND albums.AlbumId = tracks.AlbumId
            Where artists.Name = ?
            GROUP BY albums.Title
            ORDER BY SUM(tracks.UnitPrice)"""
    
    for item in cur.execute(sql, (parameters,)):
        print(f"* {item[0]:25} {item[1]:5.2f} USD   No. Tracks: {item[2]}")
    

conn.close()

#%% Paises que consumen más
import sqlite3
datafile = "datafile//chinook.db"

with sqlite3.connect(datafile) as conn:
    cur = conn.cursor()
    
    parameters = "Metallica"
    sql = """SELECT customers.Country, 
                    SUM(invoice_items.UnitPrice),
                    COUNT(invoice_items.UnitPrice)
             FROM artists
                 JOIN albums
                 JOIN tracks
                 JOIN invoice_items
                 JOIN invoices
                 JOIN customers
            ON artists.ArtistId = albums.ArtistId
                AND albums.AlbumId = tracks.AlbumId
                AND tracks.TrackId = invoice_items.TrackId
                AND invoice_items.InvoiceId = invoices.InvoiceId
                AND invoices.CustomerId = customers.CustomerId
            Where artists.Name = ?
            GROUP BY customers.Country
            ORDER BY SUM(invoice_items.UnitPrice) DESC
            LIMIT 5"""
    
    for item in cur.execute(sql, (parameters,)):
        print(f"{item[0]:25} ({item[1]:5.2f} USD) - Tracks: {item[2]}")
    

conn.close()

#%%
import sqlite3
datafile = "datafile//chinook.db"

with sqlite3.connect(datafile) as conn:
    cur = conn.cursor()
    
    #parameters = "Metallica"
    sql = """SELECT employees.EmployeeId, 
                    employees.LastName,
                    employees.FirstName,
                    SUM(invoices.Total)
             FROM artists
                 JOIN albums
                 JOIN tracks
                 JOIN invoice_items
                 JOIN invoices
                 JOIN customers
                 JOIN employees
            ON artists.ArtistId = albums.ArtistId
                AND albums.AlbumId = tracks.AlbumId
                AND tracks.TrackId = invoice_items.TrackId
                AND invoice_items.InvoiceId = invoices.InvoiceId
                AND invoices.CustomerId = customers.CustomerId
                AND customers.SupportRepId = employees.EmployeeId
            GROUP BY employees.EmployeeId,
                     employees.LastName,
                     employees.FirstName
            ORDER BY SUM(invoice_items.UnitPrice) DESC
            LIMIT 1"""
    
    for item in cur.execute(sql):
        print(f"ID:{item[0]} Name: {item[1] + ',' + item[2]:15} Total Invoiced: {item[3]:,.2f} USD")
    

conn.close()
#%%
import sqlite3
datafile = "datafile//chinook.db"

with sqlite3.connect(datafile) as conn:
    cur = conn.cursor()
    
    #parameters = "Metallica"
    sql = """SELECT employees.EmployeeId, 
                    employees.LastName,
                    employees.FirstName,
                    SUM(invoices.Total)
             FROM artists
                 JOIN invoices
                 JOIN customers
                 JOIN employees
            ON invoices.CustomerId = customers.CustomerId
               AND customers.SupportRepId = employees.EmployeeId
            GROUP BY employees.EmployeeId,
                     employees.LastName,
                     employees.FirstName
            ORDER BY SUM(invoices.Total) DESC
            LIMIT 1"""
    
    for item in cur.execute(sql):
        print(f"ID:{item[0]} Name: {item[1] + ',' + item[2]:15} Total Invoiced: {item[3]:,.2f} USD")
    

conn.close()
#%%

#%%
with conn:
    tabla = "invoices"
    cur = conn.cursor()
    results = cur.execute(f"SELECT * FROM {tabla}")
    
    print(f"Columnas en {tabla}")
    print("-----------" + "-" * len(tabla))
    for item in results.description:
        print(item)
conn.close()
#%%
# SCRIPT DE INSPECCION DE UNA BASE DE DATOS
database_file = ".//datafile//chinook.db"
conn = sqlite3.connect(database_file)

with conn:
    cur = conn.cursor()
    results = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    
    tablas_dict = {}
    
    print(f"Tablas en {database_file.upper()}")
    print("----------" + "-" * len(database_file))
    for idx, item in enumerate(results, start=1):
        print(f"[{idx}]: {item[0].upper()}")
        tablas_dict[idx] = item[0]
    else:
        tab_idx = int(input("Seleccione la tabla a inspeccionar: "))
        
        if tab_idx in tablas_dict:
            tabla = tablas_dict[tab_idx]
            #results = cur.execute(f"SELECT * FROM {tabla}")   Utilizando: results.description
            results = cur.execute(f"PRAGMA table_info ({tabla})")
             
            print(f"\nColumnas en {tabla.upper()}")
            print("-----------" + "-" * len(tabla))
            for item in results:
                # print(f"  * {item[0]}")
                print(f" * {item[1]}: ({item[2]})")
                
        else:
            print("Opcion invalida")
    

#%%
# METALLICA ESTA EN LA BASE DE DATOS?
database_file = ".//datafile//chinook.db"
conn = sqlite3.connect(database_file)

with conn:
    cur = conn.cursor()
    sql = """SELECT ArtistId, name FROM artists WHERE name LIKE '%metallica%' ORDER BY name"""
    results = cur.execute(sql)
    
    for item in results:
        print(f"{item[0]}: {item[1]}")

#%%
# QUE Y CUANTOS ALBUMS TIENE METALLICA EN LA TIENDA
database_file = ".//datafile//chinook.db"
conn = sqlite3.connect(database_file)

with conn:
    cur = conn.cursor()
    parameters = "Metallica"
    
    sql = """SELECT artists.name, COUNT(albums.title) 
             FROM artists JOIN albums 
             ON artists.ArtistId = albums.ArtistId 
             WHERE artists.name = ?"""
    results = cur.execute(sql, (parameters,))
    item = results.fetchone()
    print(f"Albums Registrados de {item[0]}: {item[1]}")
    
    sql = """SELECT artists.name, albums.title
             FROM artists JOIN albums 
             ON artists.ArtistId = albums.ArtistId 
             WHERE artists.name = ?"""
    results = cur.execute(sql, (parameters,))
    
    for item in results:
        print(f"  - {item[0]}: {item[1]}")

#%%
# LISTADO DE ALBUMS Y TRACKS DE METALLICA
database_file = ".//datafile//chinook.db"
conn = sqlite3.connect(database_file)

with conn:
    cur = conn.cursor()
    parameters = "Metallica"
    
    sql = """SELECT albums.AlbumId, albums.Title
             FROM artists JOIN albums 
             ON artists.ArtistId = albums.ArtistId 
             WHERE artists.name = ?"""
    results = cur.execute(sql, (parameters,))
    albums_id = [(item[0], item[1]) for item in results]
    
    for title in albums_id:
        parameters = title[0]
        sql = "SELECT Name, UnitPrice FROM tracks WHERE AlbumId = ?"
        results = cur.execute(sql, (parameters,))
        
        print(title[1])
        for idx, track in enumerate(results, start=1):
            print(f"  {idx:2}: {track[0]} - (${track[1]:.2f})")
        else:
            print()

#%%
# CUAL ES LA FACTURACION DE METALLICA EN LA TIENDA
database_file = ".//datafile//chinook.db"
conn = sqlite3.connect(database_file)

with conn:
    cur = conn.cursor()
    parameters = "Metallica"
    sql = """SELECT artists.Name, AVG(invoices.Total), SUM(invoices.Total)
             FROM artists 
                 JOIN albums 
                 JOIN tracks
                 JOIN invoice_items
                 JOIN invoices
             ON artists.ArtistId = albums.ArtistId 
                 AND albums.AlbumId = tracks.AlbumId
                 AND tracks.TrackId = invoice_items.TrackId
                 AND invoice_items.invoiceId = invoices.invoiceId
             WHERE artists.name = ?"""
    results = cur.execute(sql, (parameters,))
    
    for item in results:
        print(f"{item[0]} :    Fact. Prom: {item[1]:.2f}USD    Total: {item[2]:.2f}USD")

#%%
# QUE PAISES SON LOS QUEMAS CONSUMEN PRODUCTOS DE METALLICA
database_file = ".//datafile//chinook.db"
conn = sqlite3.connect(database_file)

with conn:
    cur = conn.cursor()
    parameters = "Metallica"
    sql = """SELECT customers.Country, SUM(invoices.Total) , AVG(invoices.Total)
             FROM artists 
                 JOIN albums 
                 JOIN tracks
                 JOIN invoice_items
                 JOIN invoices
                 JOIN customers
             ON artists.ArtistId = albums.ArtistId 
                 AND albums.AlbumId = tracks.AlbumId
                 AND tracks.TrackId = invoice_items.TrackId
                 AND invoice_items.invoiceId = invoices.invoiceId
                 AND invoices.CustomerId = customers.CustomerId
             WHERE artists.name = ?
             GROUP BY customers.Country
             ORDER BY SUM(invoices.Total) DESC
             LIMIT 5"""
    results = cur.execute(sql, (parameters,))
    
    for item in results:
        print(f"{item[0]}: {item[1]:.2f} USD   {item[2]:.2f} USD")

#%%
# CUALES SON LOS TRACKS MAS POPULARES DE METALLICA
database_file = ".//datafile//chinook.db"
conn = sqlite3.connect(database_file)

with conn:
    cur = conn.cursor()
    parameters = "Metallica"
    sql = """SELECT tracks.name, SUM(invoice_items.Quantity)
             FROM artists 
                 JOIN albums 
                 JOIN tracks
                 JOIN invoice_items
             ON artists.ArtistId = albums.ArtistId 
                 AND albums.AlbumId = tracks.AlbumId
                 AND tracks.TrackId = invoice_items.TrackId
             WHERE artists.name = ?
             GROUP BY tracks.name 
             ORDER BY SUM(invoice_items.Quantity) DESC
             LIMIT 10"""
    results = cur.execute(sql, (parameters,))
    
    for item in results:
        print(f"{item[0]}: {item[1]}")
#%%
# CUALES SON LOS ARTISTAS MAS REPRESENTATIVOS POR CADA GENERO MUSICAL

#%%
# MOSTRAR LOS TOP 20 DE LAS CANCIONES MAS VENDIDAS

#%%
# CUALES SON LAS TOP 10 CANCIONES MAS LARGAS DE LA TIENDA (BARRAS)

#%%
# CUALES SON LOS TOP 25 CLIENTES DE LA TIENDA (PIE)

#%%
import sqlite3
import tkinter as tk

class Database:
    datafile = "datafile/chinook.db"
    
    def __init__(self):
        self.conn = sqlite3.connect(Database.datafile)
        self.cur = self.conn.cursor()
        
    def __del__(self):
        self.conn.close()
        
    def get_genres(self):
        sql = "SELECT Name FROM genres ORDER BY Name"
        return [item[0] for item in self.cur.execute(sql)]
    
    def get_artists_by_genre(self, genre_name):
        sql = """SELECT DISTINCT(artists.Name)
                 FROM artists
                     JOIN albums
                     JOIN tracks
                     JOIN genres
                 ON artists.ArtistId = albums.ArtistId
                     AND albums.AlbumId = tracks.AlbumId
                     AND tracks.GenreId = genres.GenreId
                 WHERE genres.Name = ?
                 ORDER BY artists.Name"""
        return [item[0] for item in self.cur.execute(sql,(genre_name,))]

    
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Tkinter Chinook Store")
        self.master.resizable(0,0)
        
        self.dB = Database()
        
        frm = tk.Frame(self.master)
        frm.pack(padx=10, pady=10)
        
        frm1 = tk.LabelFrame(frm, text="Genres")
        frm1.pack(side=tk.LEFT, padx=10, pady=10)
        frm2 = tk.LabelFrame(frm, text="Artists")
        frm2.pack(side=tk.LEFT, padx=10, pady=10)
        
        # ---------------------------- frm1 ---------------------------
        self.scrY1 = tk.Scrollbar(frm1, orient ='vertical')
        self.lstGenres = tk.Listbox(frm1, height=8, yscrollcommand = self.scrY1.set)
        self.scrY1.config(command = self.lstGenres.yview)
        
        self.lstGenres.pack(side=tk.LEFT)
        self.scrY1.pack(side=tk.LEFT, expand=True, fill = tk.Y)
        self.lstGenres.bind("<<ListboxSelect>>", self.genres_selected)
        
                
        for genre in self.dB.get_genres():
            self.lstGenres.insert(tk.END, genre)
        
        # ---------------------------- frm2 ---------------------------
        
        self.scrY2 = tk.Scrollbar(frm2, orient ='vertical')
        self.lstArtists = tk.Listbox(frm2, height=8, yscrollcommand = self.scrY2.set)
        self.scrY2.config(command = self.lstArtists.yview)
        
        self.lstArtists.pack(side=tk.LEFT)
        self.scrY2.pack(side=tk.LEFT, expand=True, fill = tk.Y)
        
        
    def genres_selected(self, event):
        try:
            genre_name = self.lstGenres.get(self.lstGenres.curselection())
            
            self.lstArtists.delete(0,tk.END)
            for artist in self.dB.get_artists_by_genre(genre_name):
                self.lstArtists.insert(tk.END, artist)
        except:
            pass
root = tk.Tk()
app = App(root)
root.mainloop()




































